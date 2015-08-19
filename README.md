#Fuzzy Control README
New code for the fuzzy control module.
##Pre-req before running this code:
1. python's numpy should be installed.
2. Scipy should be installed
3. Scipy's skfuzzy toolbox should be installed.

Description of files:
##main.py
Main file containing the call to fuzzy class which controls the fuzzy output corresponding to a control input
##fuzzy.py
Fuzzy class is contained in this file. Descriptions of functions : 
###Fuzzy.run()
Imports standardized values from main.py and runs the other routines defined in fuzzy.py. Passes the results to visualize.py for results plotting.
###Fuzzy.membership_f()
Fuzzifies the inputs[] array into b[][] 3D array.
