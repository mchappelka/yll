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
le_df = pd.read_csv(os.path.join(in_path, 'Additional Measure Data-Table 1.csv'), 
                    header = 1)

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

# drop rows where the age column doesn't have an age value 
gadph_df_subset = gadph_df_subset[gadph_df_subset.age != "." ]
gadph_df_subset = gadph_df_subset[gadph_df_subset.age != "We haven't run out of rows yet" ]

#convert age to numeric
gadph_df_subset["age"] = pd.to_numeric(gadph_df_subset["age"])

# drop rows where every value is missing
gadph_df_subset2 = gadph_df_subset.dropna(how='all')

# Check county values
gadph_df_subset2["County"].unique()

# how often do non county values occur
gadph_df_subset2[gadph_df_subset2.County == "Non-GA Resident/Unknown State"].count()
gadph_df_subset2[gadph_df_subset2.County == "Unknown"].count()

# drop non-county values
gadph_df_subset2 = gadph_df_subset2[gadph_df_subset2.County != "Non-GA Resident/Unknown State"]
gadph_df_subset2 = gadph_df_subset2[gadph_df_subset2.County != "Unknown"]

##############################################################################
#                                                                            #
#                   Read in county demographic data                          #
#                                                                            #
##############################################################################

demo_df = pd.read_csv(os.path.join(in_path, "ga_county_demographics.csv"))

# drop rows we're not interested in
demo_df2 = demo_df[demo_df.AGEGRP == 0]  #agrgp of 0 is the total for all age groups
demo_df2 = demo_df2[demo_df2.YEAR == 12]  # year 12 is the 2019 estimate (most recent)

cols_to_keep = ["CTYNAME",  "TOT_POP", "WA_MALE", "WA_FEMALE", "BA_MALE", 
                "BA_FEMALE", "AA_MALE", "AA_FEMALE", "NH_MALE", "NH_FEMALE",
                "H_MALE", "H_FEMALE"]

demo_subset = demo_df2[cols_to_keep]

for race in ["WA", "BA", "AA", "NH", "H"]:
    demo_subset[race + "_TOT"] = demo_subset[race + "_FEMALE"]  + demo_subset[race + "_MALE"] 
    demo_subset[race + "_pct"] = demo_subset[race + "_TOT"] / demo_subset["TOT_POP"]

# Remove "County" from the county names so that it is in same format as county
# names in our other datasets
demo_subset["County"] = demo_subset["CTYNAME"].str.rstrip('County').str.strip()

cols_to_keep = ["County", "TOT_POP", "WA_TOT", "BA_TOT", "AA_TOT", "NH_TOT",
                "H_TOT", "WA_pct", "BA_pct", "AA_pct", "NH_pct", "H_pct"]

demo_subset2 = demo_subset[cols_to_keep]

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

gadph_df_subset2["County"].unique()

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

# delete if new_race is AIAN, NHPI, other, or unknown
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
merged_df = pd.merge(merged_df, demo_subset2, how='left', on = ['County'])

##############################################################################
#                                                                            #
#                   Calculate years of life lost                             #
#                                                                            #
##############################################################################

# Calculate life expectancy based on the life expectancy for their race and county
# Native Hawaiian/Pacific Islander is excluded because it's not a category in the RWJF data
merged_df["YLL_racecounty"] = merged_df.apply(
    lambda x:
        x['Life Expectancy (Black)'] - x['age'] if x['new_race']=='African-American/ Black' 
        else (x['Life Expectancy (Asian)'] - x['age'] if x['new_race']=='Asian' 
        else (x['Life Expectancy (White)'] - x['age'] if x['new_race']=='White' 
        else (x['Life Expectancy (Hispanic)'] - x['age'] if x['new_race']=='Hispanic/ Latino' 
        else np.nan))),  axis=1 )
 
merged_df.loc[merged_df.YLL_racecounty < 0, "YLL_racecounty"] = 0  

# Calculate life expectancy based on the life expectancy for their county (not stratified by race)
merged_df["YLL_county"] =  merged_df['Life Expectancy'] - merged_df['age']
merged_df.loc[merged_df.YLL_county < 0, "YLL_county"] = 0  

##############################################################################
#                                                                            #
#                      Calculate summary statistics                          #
#                                                                            #
##############################################################################

yll_dist = merged_df.groupby(["new_race"])[["YLL_county", "YLL_racecounty"]].describe().round(1)
mean_age = merged_df.groupby(["new_race"])["age"].mean().round(1)
total_yll = merged_df.groupby(["new_race"])[["YLL_county", "YLL_racecounty"]].sum()
mean_yll = merged_df.groupby(["new_race"])[["YLL_county", "YLL_racecounty"]].mean().round(1)
num_deaths = pd.value_counts(merged_df.new_race)


# Examine counties where black life expectancy > white life expectancy
bw_df = merged_df[merged_df["Life Expectancy (Black)"] > merged_df["Life Expectancy (White)"]]
bw_df = bw_df[["County", "Life Expectancy (Black)", "Life Expectancy (White)", "TOT_POP", "WA_TOT", "BA_TOT", "AA_TOT", "WA_pct", "BA_pct", "AA_pct" ]]
bw_df = bw_df.drop_duplicates()

# Examine counties where hispanic life expectancy > 90
hisp_df =  merged_df[merged_df["Life Expectancy (Hispanic)"] > 90]
hisp_df = hisp_df[["County", "Life Expectancy (Hispanic)", "TOT_POP", "NH_TOT", "H_TOT", "NH_pct", "H_pct" ]]
hisp_df = hisp_df.drop_duplicates()

##############################################################################
#                                                                            #
#                                Output data                                 #
#                                                                            #
##############################################################################

# CSV
yll_dist.to_csv(os.path.join(out_path, "dist_yll.csv"))
mean_age.to_csv(os.path.join(out_path,"mean_death_age.csv"))
total_yll.to_csv(os.path.join(out_path,"sum_yll.csv"))
mean_yll.to_csv(os.path.join(out_path,"mean_yll.csv"))
num_deaths.to_csv(os.path.join(out_path,"num_deaths.csv"))

bw_df.to_csv(os.path.join(out_path, "black_le_over_white.csv"))
hisp_df.to_csv(os.path.join(out_path, "hispanic_le_over90.csv"))

# EXCEL
with pd.ExcelWriter(os.path.join(out_path,"yll.xlsx")) as writer:  
    num_deaths.to_excel(writer, sheet_name='num_deaths') 
    mean_age.to_excel(writer, sheet_name='mean_death_age')
    yll_dist.to_excel(writer, sheet_name='dist_yll')
    total_yll.to_excel(writer, sheet_name='sum_yll')
    mean_yll.to_excel(writer, sheet_name='mean_yll')
    bw_df.to_excel(writer, sheet_name='black_le_over_white')
    hisp_df.to_excel(writer, sheet_name='hispanic_le_over90') 
    










