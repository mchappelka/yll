# -*- coding: utf-8 -*-
import pandas as pd
import sys
import os

sys.path.insert(1, "C:/Users/hpfla/OneDrive/Documents/Covid_Tracking_Project/life_expectancy/yll/code")
import params
##############################################################################
#                                                                            #
#                   Read in Georgia county demographic data                          #
#                                                                            #
##############################################################################

demo_df = pd.read_csv(os.path.join(params.RAW_DATA_PATH, "demographics", "ga_county_demographics.csv"))

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

demo_subset2.to_csv(os.path.join(params.CLEAN_DATA_PATH, 'ga_demographics.csv'), index=False)