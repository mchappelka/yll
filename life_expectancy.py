import pandas as pd
import numpy as np
import os

##############################################################################
#                                                                            #
#               Set programming variables                                    #
#                                                                            #
##############################################################################

base_path = "C:/Users/hpfla/OneDrive/Documents"
prog_path = os.path.join(base_path, "Covid_Tracking_Project/life_expectancy")
in_path = os.path.join(prog_path, "data/100_cleaned_data") 
out_path = os.path.join(prog_path, "data/output") 

##############################################################################
#                                                                            #
#               Read in life expectancy data                                 #
#                                                                            #
##############################################################################
le_df = pd.read_csv(os.path.join(in_path, 'ga_life_expectancy.csv'))

##############################################################################
#                                                                            #
#                           Read in death data                               #
#                                                                            #
##############################################################################

deaths_df = pd.read_csv(os.path.join(in_path, 'ga_covid_deaths.csv'))

##############################################################################
#                                                                            #
#                   Read in county demographic data                          #
#                                                                            #
##############################################################################

demo_df = pd.read_csv(os.path.join(in_path, 'ga_demographics.csv'))


##############################################################################
#                                                                            #
#                                Merge datasets                              #
#                                                                            #
##############################################################################

merged_df = pd.merge(deaths_df, le_df, how='left', on = ['County'])
merged_df = pd.merge(merged_df, demo_df, how='left', on = ['County'])

##############################################################################
#                                                                            #
#                   Calculate years of life lost                             #
#                                                                            #
##############################################################################

# County Race Life Expectancy variable 
merged_df["County Race Life Expectancy"] = merged_df.apply(
    lambda x:
        x['County Life Expectancy (Black)']  if x['new_race']=='African-American/ Black' 
        else (x['County Life Expectancy (Asian)']  if x['new_race']=='Asian' 
        else (x['County Life Expectancy (White)'] if x['new_race']=='White' 
        else (x['County Life Expectancy (Hispanic)']  if x['new_race']=='Hispanic/ Latino' 
        else np.nan))),  axis=1 )

merged_df["YLL_racecounty"] = merged_df["County Race Life Expectancy"] - merged_df["age"]

# drop the race specific county life expectancy variables since that information is now contained in 
# the County Race Life Expectancy variable
merged_df.columns

merged_df = merged_df.drop(['County Life Expectancy (AIAN)',
       'County Life Expectancy (Asian)', 'County Life Expectancy (Black)',
       'County Life Expectancy (Hispanic)', 'County Life Expectancy (White)'], axis=1)  

merged_df.loc[merged_df.YLL_racecounty < 0, "YLL_racecounty"] = 0  
 
# Calculate life expectancy based on the life expectancy for their county (not stratified by race)
merged_df["YLL_county"] =  merged_df['County Life Expectancy'] - merged_df['age']
merged_df.loc[merged_df.YLL_county < 0, "YLL_county"] = 0  


##############################################################################
#                                                                            #
#                                Output data                                 #
#                                                                            #
##############################################################################

merged_df.to_csv(os.path.join(out_path, 'analytic_file.csv'))
