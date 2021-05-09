
import sys 
sys.path.insert(1, "C:/Users/hpfla/OneDrive/Documents/Covid_Tracking_Project/life_expectancy/yll/code")
import functions
##############################################################################
#                                                                            #
#               Create a file of state-level life expectancy data           #
#                                                                            #
##############################################################################

functions.process_le(is_county=False, outfilename = 'state_life_expectancy.csv')