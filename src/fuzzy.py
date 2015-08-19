import pid
import skfuzzy as fuzz
import numpy as np
import matplotlib.pyplot as plt
import visualize

class Fuzzy(pid.PID):

    """  Fuzzy pid contains 3 variables , 2 input variables (error and delta_e) and one output variable
         mu - list storing type of mf for each of the variables (list of size 3)
         d_mu - list containing details of each mf of each of the variables, i.e, say for error value of end points of each triangle. (size = 3,5,3)
         first 3 - three variables, second 5 - five fuzzy_set variables, last 3 - 3 parameters required to define a triangle 
         var_ranges - error, delta_e and control_output ranges not values
         e and delta_e - input parameters(variables) required for fuzzy pid control
         This class is compatible of receiving different mf for each variables, and receiving different no. of fuzzy_set variables for each variables and each 
         all possible different range.
         fuzzy_set - 
    """
         
    def __init__(self, mu, d_mu):
            self.error   = 0
            self.delta_e = 0
            self.mu      = mu       
            self.d_mu    = d_mu     
            self.var_ranges = []    
        
    def run(self):

            """ inputs[0] =  ERROR AXIS          ., so stores all possible error values
                inputs[1] =  DEL_ERROR AXIS      .,     ,,
                inputs[2] =  CONTROL_OUTPUT AXIS .,     ,,
                    
                ERROR                  DEL_ERROR               CONTROL_OUTPUT         m_value for crisp e and delta_e values

                b[0][0] -ve Medium  || b[1][0] -ve Medium  ||  b[2][0] -ve Medium   ..        f[0] |  f_d[0] 
                b[0][1] -ve small   || b[1][1] -ve small   ||  b[2][1] -ve small    ..        f[1] |  f_d[1]
                b[0][2] zero        || b[1][2] zero        ||  b[2][2] zero         ..        f[2] |  f_d[2]
                b[0][3] +ve small   || b[1][3] +ve small   ||  b[2][3] +ve small    ..        f[3] |  f_d[3]
                b[0][4] +ve Medium  || b[1][4] +ve Medium  ||  b[2][4] +_ve Medium  ..        f[4] |  f_d[4] 
                
                f_mat is fuzzy fuzzy_matrix
            """
            inputs = [ np.arange(var[0], var[1]+1, 1) for var in self.var_ranges] #step size  = 1, third dimension of b matrix. As of now, an assumption.
            b  = []
            output = [0,0,0,0,0]
            out_final = []
            for i in range(3) :
                    b.append( [membership_f(self.mu[i], inputs[i], a) for a in self.d_mu[i] ])
            # To visualize the membership func. call .. [ visualize_mf(b,inputs)  ]
            
            f ,f_d = error_fuzzify(inputs, b, self.error, self.delta_e)            
            f_mat = fuzzy_matrix(f,f_d)
            output = rule_base(b, f_mat, output)
            print 'output : ', output
            aggregated = np.fmax(output[0], np.fmax(output[1],np.fmax(output[2], np.fmax(output[3], output[4]))))
            out_final = fuzz.defuzz(inputs[2], aggregated, 'centroid')
            out_activation = fuzz.interp_membership(inputs[2], aggregated, out_final)  # for plot
            visualize.visualize_mf(b,inputs,output, out_final, out_activation, aggregated)
            visualize.visualize_output(b, inputs, out_final, out_activation, aggregated)
            plt.show()

def membership_f(mf, x, abc = [0,0,0], a = 1, b = 2, c = 3, d = 4, abcd = [0,0,0,0]):

        return {
            'trimf'   : fuzz.trimf(x, abc),                                 # trimf(x, abc)
            'dsigmf'  : fuzz.dsigmf(x, a, b, c, d),                         # dsigmf(x, b1, c1, b2, c2)
            'gauss2mf': fuzz.gauss2mf(x, a, b, c, d),                       # gauss2mf(x, mean1, sigma1, mean2, sigma2)
            'gaussmf' : fuzz.gaussmf(x, a, b),                              # gaussmf(x, mean, sigma)
            'gbellmf' : fuzz.gbellmf(x, a, b, c),                           # gbellmf(x, a, b, c)
            'piecemf' : fuzz.piecemf(x, abc),                               # piecemf(x, abc)
            'pimf'    : fuzz.pimf(x, a, b, c, d),                           # pimf(x, a, b, c, d)
            'psigmf'  : fuzz.psigmf(x, a, b, c, d),                         # psigmf(x, b1, c1, b2, c2)
            'sigmf'   : fuzz.sigmf(x, a, b),                                # sigmf(x, b, c)
            'smf'     : fuzz.smf(x, a, b),                                  # smf(x, a, b)
            'trapmf'  : fuzz.trapmf(x, abcd),                               # trapmf(x, abcd)
            'zmf'     : fuzz.zmf(x, a, b),                                  # zmf(x, a, b)
                }[mf]

def error_fuzzify(inputs, b, error, delta_e):
    f   = [fuzz.interp_membership(inputs[0], fuzzy_set, error) for fuzzy_set in b[0]] #f : mu-value corresponding to error on fuzzy set.
    f_d = [fuzz.interp_membership(inputs[1], fuzzy_set, delta_e) for fuzzy_set in b[1]]# f_d : mu-value corresponding to delta_e on fuzzy set.
    return (f, f_d)

def fuzzy_matrix(f, f_d): #fuzzy_matrix function returns array of rule strengths
    print "f:",f
    print "f_d:",f_d
    return np.array([ [min(a,b) for a in f] for b in f_d])

#b= y-values of trimf corresponding to each input and output variables in range var.ranges[]
def rule_base(b, f_mat, output):
    """
    ERROR/ DEL_ERROR | -ve Medium              ||  -ve small              ||        zero               ||   +ve small              ||    +ve Medium         
                    ------------------------------------------------------------------------------------------------------------------------------------------                      
      -ve Medium     | f_mat[0][0] -ve Medium  || f_mat[1][0] -ve Medium  ||  f_mat[2][0] -ve Medium   || f_mat[3][0] -ve Medium   || f_mat[4][0] -ve Medium   
      -ve small      | f_mat[0][1] -ve small   || f_mat[1][1] -ve small   ||  f_mat[2][1] -ve small    || f_mat[3][1] -ve small    || f_mat[4][1] -ve small    
      zero           | f_mat[0][2] zero        || f_mat[1][2] zero        ||  f_mat[2][2] zero         || f_mat[3][2] zero         || f_mat[4][2] zero         
      +ve small      | f_mat[0][3] +ve small   || f_mat[1][3] +ve small   ||  f_mat[2][3] +ve small    || f_mat[3][3] +ve small    || f_mat[4][3] +ve small    
      +ve Medium     | f_mat[0][4] +ve Medium  || f_mat[1][4] +ve Medium  ||  f_mat[2][4] +_ve Medium  || f_mat[3][4] +_ve Medium  || f_mat[4][4] +_ve Medium 

    """
    control_Nmed   = max(f_mat[0][0], f_mat[0][1], f_mat[1][0], f_mat[1][1], f_mat[2][0], f_mat[3][0])
    output[0] = np.fmin(control_Nmed,b[2][0])
    control_Nsmall = max(f_mat[0][2], f_mat[1][2], f_mat[2][2], f_mat[3][2], f_mat[4][0])
    output[1] = np.fmin(control_Nsmall, b[2][1])
    control_zero   = max(f_mat[0][3], f_mat[2][2], f_mat[4][1])
    output[2] = np.fmin(control_zero, b[2][2])
    control_Psmall = max(f_mat[0][4], f_mat[1][3], f_mat[2][3], f_mat[3][2], f_mat[4][2])
    output[3] = np.fmin(control_Psmall, b[2][3])
    control_Pmed   = max(f_mat[1][4], f_mat[2][4], f_mat[3][4], f_mat[3][3], f_mat[4][3], f_mat[4][4])
    output[4] = np.fmin(control_Pmed, b[2][4])
    
    return output