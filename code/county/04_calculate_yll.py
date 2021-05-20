import pandas as pd
import numpy as np
import os
import sys

sys.path.insert(1, "C:/Users/hpfla/OneDrive/Documents/Covid_Tracking_Project/life_expectancy/yll/code")
import params
import functions
    
##############################################################################
#                                                                            #
#               Read in  life expectancy data                                 #
#                                                                            #
##############################################################################
le_df = pd.read_csv(os.path.join(params.CLEAN_DATA_PATH, 'county_life_expectancy.csv'))

##############################################################################
#                                                                            #
#            read in               death data                               #
#                                                                            #
##############################################################################

deaths_df = pd.read_csv(os.path.join(params.CLEAN_DATA_PATH, 'county_deaths.csv'))

##############################################################################
#                                                                            #
#                   Read in county demographic data                          #
#                                                                            #
##############################################################################

demo_df = pd.read_csv(os.path.join(params.CLEAN_DATA_PATH, 'ga_demographics.csv'))


##############################################################################
#                                                                            #
#                                Merge datasets                              #
#                                                                            #
##############################################################################

merged_df = pd.merge(deaths_df, le_df, how='left', on = ['County', 'Race'])


##############################################################################
#                                                                            #
#                   Calculate years of life lost                             #
#                                                                            #
##############################################################################

merged_df = functions.calc_yll(df=merged_df
                        ,yllname="YLL_racecounty"
                        ,le="Race-County Life Expectancy"
                        ,age="age"
                        )

merged_df = functions.calc_yll(df=merged_df,
                        yllname="YLL_county"
                        ,le="County Life Expectancy"
                        ,age="age"
                        )
merged_df = functions.calc_yll(df=merged_df,
                        yllname="YLL_racestate"
                        ,le="Race-State Life Expectancy"
                        ,age="age"
                        ) 
##############################################################################
#                                                                            #
#                   Calculate total YLL for race and state, all ages         #
#                                                                            #
##############################################################################

record_level_cols = ["State", "Race", "Race-State Life Expectancy"]
sum_cols = ["YLL_racestate"]
keep_cols = record_level_cols + sum_cols

state_df = merged_df[keep_cols].groupby(record_level_cols).sum().reset_index()
state_df["age"] = "All"
state_df["County"] = "All"

merged_df = merged_df.append(state_df)

##############################################################################
#                                                                            #
#                                Output data                                 #
#                                                                            #
##############################################################################

merged_df.to_csv(os.path.join(params.ANALYTIC_PATH, 'county_yll.csv'), index=False)

merged_df = pd.merge(merged_df, demo_df, how='left', on = ['County'])
merged_df.to_csv(os.path.join(params.ANALYTIC_PATH, 'county_analytic_file.csv'), index=False)
