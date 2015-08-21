import fuzzy

f_ssets = [ [ # error
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

io_ranges = [ # range of e
              [-10,10],
               # range of d_e
              [-10,10],
               # range of u
              [-10,10]
            ]

mf_types = ['trimf','trimf','trimf']

def main():
  x = fuzzy.Fuzzy(mf_types, f_ssets)
  x.error = 7.5
  x.delta_e = 5 
  x.io_ranges = io_ranges
  x.run() 

if __name__ == '__main__':
  main()
