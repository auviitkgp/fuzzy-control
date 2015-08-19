import fuzzy

d_mf = [ [ # error
          [-10,-10,-5],  # -ve medium   
          [-10,-5 , 0],  # -ve small
          [-5 , 0 , 5],  # zero
          [ 0 , 5 , 10], # +ve small
          [ 5 ,10 , 10], # +ve medium
         ],        
           # delta_error
         [          
          [-10,-10,-5],  # -ve medium
          [-10,-5 , 0],  # -ve small
          [-5 , 0 , 5],  # zero
          [ 0 , 5 , 10], # +ve small
          [ 5 ,10 , 10], # +ve medium
         ],              
            # u
         [                 
          [-10,-10,-5],  # -ve medium
          [-10,-5 , 0],  # -ve small
          [-5 , 0 , 5],  # zero
          [ 0 , 5 , 10], # +ve small
          [ 5 ,10 , 10], # +ve medium
         ]                 
      ] 

bong = [ # range of e
        [-10,10],
         # range of d_e
        [-10,10],
         # range of u
        [-10,10]
       ]

mf = ['trimf','trimf','trimf']

def main():
  x = fuzzy.Fuzzy(mf, d_mf)
  x.target = 5
  x.error = -4
  x.delta_e = -10 
  x.var_ranges = bong
  x.run() 

if __name__ == '__main__':
  main()
