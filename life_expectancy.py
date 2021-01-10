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

isNewData = False

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
                "Life Expectancy (AIAN)",
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
if (isNewData):
    gadph_df = pd.read_csv(os.path.join(in_path, 
                                    "GA Race Age Deaths - Paste CSV here.csv"))

if (not isNewData):
    gadph_df = pd.read_csv(os.path.join(in_path, 
                                    "previous -- GA Race Age Deaths - Paste CSV here_old.csv"))
    
#rename columns
gadph_df = gadph_df.rename({'https://dph.georgia.gov/covid-19-daily-status-report' : 'age',
                            'county': 'County'}, axis=1)
cols_to_keep = ['ethnicity', 'race', 'sex', 'County', 'age']

gadph_df_subset = gadph_df[cols_to_keep]

# drop rows where age is . 
gadph_df_subset = gadph_df_subset[gadph_df_subset.age != "." ]
gadph_df_subset = gadph_df_subset[gadph_df_subset.age != "We haven't run out of rows yet" ]
gadph_df_subset = gadph_df_subset[gadph_df_subset.race != "Unknown" ]
gadph_df_subset = gadph_df_subset[gadph_df_subset.race != "Other" ]

#convert age to numeric
gadph_df_subset["age"] = pd.to_numeric(gadph_df_subset["age"])

# drop rows where every value is missing
gadph_df_subset2 = gadph_df_subset.dropna(how='all')
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
                         
le_df_subset.columns
gadph_df_subset.race.unique()
gadph_df_subset.ethnicity.unique()
# Hispanic/Latino ethnicity any race is one category. Then Black, White, AIAN, 
# Asian, are all defined as non-Hispanic Black, non-Hispanic White, etc.


gadph_df_subset2["new_race"] = gadph_df_subset2.apply(
    lambda x: x['ethnicity'] if x['ethnicity']=='Hispanic/ Latino' 
    else x['race'], axis=1
    )

gadph_df_subset2.new_race.unique()


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
merged_df["YLL"] = merged_df.apply(
    lambda x:
        x['Life Expectancy (Black)'] - x['age'] if x['new_race']=='African-American/ Black' 
        else (x['Life Expectancy (Asian)'] - x['age'] if x['new_race']=='Asian' 
        else (x['Life Expectancy (White)'] - x['age'] if x['new_race']=='White' 
        else (x['Life Expectancy (Hispanic)'] - x['age'] if x['new_race']=='Hispanic/ Latino' 
        else (x['Life Expectancy (AIAN)'] - x['age'] if x['new_race'] == 'American Indian/ Alaska Native' else np.nan)))), 
                                                              axis=1
    )
    
merged_df.loc[merged_df.YLL < 0, "YLL"] = 0  
 

# Calculate life expectancy based on the life expectancy for their county 
merged_df["YLL_county"] = merged_df.apply(
    lambda x:
        x['Life Expectancy'] - x['age'] if x['new_race']=='African-American/ Black' 
        else (x['Life Expectancy'] - x['age'] if x['new_race']=='Asian' 
        else (x['Life Expectancy'] - x['age'] if x['new_race']=='White' 
        else (x['Life Expectancy'] - x['age'] if x['new_race']=='Hispanic/ Latino' 
        else (x['Life Expectancy'] - x['age'] if x['new_race'] == 'American Indian/ Alaska Native' else np.nan)))), 
                                                              axis=1
    )
# merged_df.loc[merged_df.YLL_county < 0, "YLL"] = 0  

##############################################################################
#                                                                            #
#                      Calculate summary statistics                          #
#                                                                            #
##############################################################################

descriptive_stats = merged_df.groupby(["new_race"])[["YLL"]].describe()
descriptive_stats_county = merged_df.groupby(["new_race"])[["YLL_county"]].describe()

merged_df[merged_df["new_race"] == "African-American/ Black"].YLL.hist()
merged_df[merged_df["new_race"] == "Asian"].YLL.hist()
merged_df[merged_df["new_race"] == "White"].YLL.hist()
merged_df[merged_df["new_race"] == "Hispanic/ Latino"].YLL.hist()

merged_df.groupby(["new_race"])["age"].mean()
merged_df.groupby(["new_race"])["YLL_county"].sum()


#fill na with 0
merged_df.YLL = merged_df.YLL.fillna(0)
merged_df.groupby(["new_race"])["YLL"].sum()


# calculate for native hawaiian/pi

# why is american indian/ alaska native not showing up? 
# because the counties for which we have AI/AN life expectancy data had no AI/AN deaths

# Compare life expectancy by county 
if (isNewData):
    new_data = merged_df[["County", "Life Expectancy (Hispanic)"]].drop_duplicates()

if (not isNewData):
   old_data = merged_df[["County", "Life Expectancy (Hispanic)"]].drop_duplicates()








