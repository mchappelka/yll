#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 19:28:39 2020

@author: mchappelka
"""


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
in_path = os.path.join(prog_path, "data/input")
out_path = os.path.join(prog_path, "data/output") 

##############################################################################
#                                                                            #
#               Read in life expectancy data                                 #
#                                                                            #
##############################################################################
le_df = pd.read_csv(os.path.join(in_path, 
                                 'Additional Measure Data-Table 1.csv'), 
                    header = 1)


# rename column
cols_to_keep = ["State",
                "County",
                "Life Expectancy",
                'Life Expectancy (AIAN)',
                "Life Expectancy (Asian)", 
                "Life Expectancy (Black)", 
                "Life Expectancy (Hispanic)", 
                "Life Expectancy (White)"]

le_df_subset = le_df[cols_to_keep]



# there's one row where the County value is missing - the values here are the
# state-level values. 
le_df_subset = le_df_subset.dropna(subset=['County'])


##############################################################################
#                                                                            #
#                           Read in death data                               #
#                                                                            #
##############################################################################

gadph_df = pd.read_csv(os.path.join(in_path, 
                                    "GA Race Age Deaths - Paste CSV here.csv"))


    
#rename columns
gadph_df = gadph_df.rename({'https://dph.georgia.gov/covid-19-daily-status-report' : 'age',
                            'county': 'County'}, axis=1)
cols_to_keep = ['ethnicity', 'race', 'sex', 'County', 'age']

gadph_df_subset = gadph_df[cols_to_keep]

# drop rows where age is . 
gadph_df_subset = gadph_df_subset[gadph_df_subset.age != "." ]
gadph_df_subset = gadph_df_subset[gadph_df_subset.age != "We haven't run out of rows yet" ]
#gadph_df_subset = gadph_df_subset[gadph_df_subset.race != "Unknown" ]
#gadph_df_subset = gadph_df_subset[gadph_df_subset.race != "Other" ]

#convert age to numeric
gadph_df_subset["age"] = pd.to_numeric(gadph_df_subset["age"])

# drop rows where every value is missing
gadph_df_subset2 = gadph_df_subset.dropna(how='all')

##############################################################################
#                                                                            #
#                          Examine the data                                  #
#                                                                            #
##############################################################################

# Summary of life expectancy values
le_summary = le_df_subset[["Life Expectancy", 'Life Expectancy (AIAN)',
       'Life Expectancy (Asian)', 'Life Expectancy (Black)',
       'Life Expectancy (Hispanic)', 'Life Expectancy (White)']].describe().round(1)

# Examine counties where black life expectancy > white life expectancy
ledf_sub_bw =  le_df_subset[le_df_subset["Life Expectancy (Black)"] > le_df_subset["Life Expectancy (White)"]]

# Examine counties where hispanic life expectancy > 90
ledf_sub_hisp =  le_df_subset[le_df_subset["Life Expectancy (Hispanic)"] > 90]

# Frequency of race and ethnicity variables
gadph_df_subset2.groupby(['ethnicity'], as_index=False).size()
gadph_df_subset2.groupby(['race'], as_index=False).size()
gadph_df_subset2.groupby(['ethnicity', 'race'], as_index=False).size()

##############################################################################
#                                                                            #
#                 Create a common race variable                              #
#                                                                            #
##############################################################################

''' RWJF groups people as AIAN, Asian, Black, Hispanic, White

 GADPH groups people as 'African-American/ Black', 
                         'White', 
                         'Other',
                         'American Indian/ Alaska Native', 
                         'Unknown', 
                         'Asian',
                         'Native Hawaiian/ Pacific Islander
                         
                         and includes their ethnicicty (hispanic/not)'''
                         

# Hispanic/Latino ethnicity any race is one category. Then Black, White, AIAN, 
# Asian, are all defined as non-Hispanic Black, non-Hispanic White, etc.


gadph_df_subset2["new_race"] = gadph_df_subset2.apply(
    lambda x: x['ethnicity'] if x['ethnicity']=='Hispanic/ Latino' 
    else x['race'], axis=1
    )

# Check new race variable
gadph_df_subset2.groupby(['ethnicity', 'race', 'new_race'], as_index=False).size()

# delete if new_race is AIAN or NHPI
gadph_df_subset2 = gadph_df_subset2[gadph_df_subset2.new_race != "American Indian/ Alaska Native" ]
gadph_df_subset2 = gadph_df_subset2[gadph_df_subset2.new_race != "Native Hawaiian/ Pacific Islander" ]
gadph_df_subset2 = gadph_df_subset2[gadph_df_subset2.new_race != "Other" ]
gadph_df_subset2 = gadph_df_subset2[gadph_df_subset2.new_race != "Unknown" ]

##############################################################################
#                                                                            #
#                                Merge datasets                              #
#                                                                            #
##############################################################################

# Merge by county 
merged_df = pd.merge(gadph_df_subset2, le_df_subset, how='left', on = ['County'])

##############################################################################
#                                                                            #
#                   Calculate years of life lost                             #
#                                                                            #
##############################################################################

# Calculate life expectancy based on the life expectancy for their race and county
# Native Hawaiian/Pacific Islander is excluded because it's not a category in the RWJF data
merged_df["YLL"] = merged_df.apply(
    lambda x:
        x['Life Expectancy (Black)'] - x['age'] if x['new_race']=='African-American/ Black' 
        else (x['Life Expectancy (Asian)'] - x['age'] if x['new_race']=='Asian' 
        else (x['Life Expectancy (White)'] - x['age'] if x['new_race']=='White' 
        else (x['Life Expectancy (Hispanic)'] - x['age'] if x['new_race']=='Hispanic/ Latino' 
        else np.nan))), 
                                                              axis=1
    )
    
 
# add id values
merged_df['id'] = range(1, len(merged_df) + 1)

merged_df.loc[merged_df.YLL < 0, "YLL"] = 0  
 

# Calculate life expectancy based on the life expectancy for their county (not stratified by race)

merged_df["YLL_county"] =  merged_df['Life Expectancy'] - merged_df['age']


merged_df.loc[merged_df.YLL_county < 0, "YLL_county"] = 0  

##############################################################################
#                                                                            #
#                      Calculate summary statistics                          #
#                                                                            #
##############################################################################

merged_df.groupby(["new_race"])[["YLL"]].describe().round(1)



merged_df.groupby(["new_race"])["age"].mean().round(1)



#fill na with 0
merged_df.YLL = merged_df.YLL.fillna(0)



merged_df.groupby(["new_race"])["YLL"].sum()
merged_df.groupby(["new_race"])["YLL"].mean().round(1)
merged_df.groupby(["new_race"])["YLL"].count()




# why is american indian/ alaska native not showing up? 
# because the counties for which we have AI/AN life expectancy data had no AI/AN deaths






pd.value_counts(merged_df.new_race)

##############################################################################
#                                                                            #
#                                Output data                                 #
#                                                                            #
##############################################################################



