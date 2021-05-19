# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 21:20:21 2021

@author: hpfla
"""
import sys

sys.path.insert(0, "C:/Users/hpfla/OneDrive/Documents/Covid_Tracking_Project/life_expectancy/yll/code")
import params
import functions
import pandas as pd
import os

# life expectancy for state by race
le = pd.read_csv(os.path.join(params.CLEAN_DATA_PATH, 'state_life_expectancy.csv'))

# deaths for state
deaths = pd.read_csv(os.path.join(params.CLEAN_DATA_PATH, 'state_deaths.csv'))

# merge datasets together
df = deaths.merge(le, how="left", on =["State", "Race"])

df = functions.calc_yll(df = df
                        ,yllname="YLL (based on age bracket median)"
                        ,le="Life Expectancy"
                        ,age="Bracket_Median_Age"
                        )

df = functions.calc_yll(df = df
                        ,yllname="YLL (based on age bracket weighted mean)"
                        ,le="Life Expectancy"
                        ,age="Bracket_Mean_Age"
                        )

df = functions.calc_yll(df = df
                        ,yllname="YLL (based on upper age in bracket)"
                        ,le="Life Expectancy"
                        ,age="Age_Upper"
                        )

##############################################################################
#                                                                            #
#                   Calculate total YLL for race and state, all ages         #
#                                                                            #
##############################################################################

record_level_cols = ["State"]
sum_cols = ['Deaths'] + [col for col in df.columns if 'YLL' in col]
keep_cols = record_level_cols + sum_cols

state_df = df[keep_cols].groupby(record_level_cols).sum().reset_index()
state_df["Age_Bracket"] = "All"

df = df.append(state_df)

##############################################################################
#                                                                            #
#                                    Output                                  #
#                                                                            #
##############################################################################
 
df.to_csv(os.path.join(params.ANALYTIC_PATH, 'state_yll.csv'), index=False)

