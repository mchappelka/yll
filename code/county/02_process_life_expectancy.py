
import sys 
sys.path.insert(1, "C:/Users/hpfla/OneDrive/Documents/Covid_Tracking_Project/life_expectancy/yll/code")
import functions
##############################################################################
#                                                                            #
#               Create a table of county-level life expectancy data          #
#                                              (only for Ga)                 #
#                                                                            #
##############################################################################

functions.process_le(is_county=True, outfilename='county_life_expectancy.csv')