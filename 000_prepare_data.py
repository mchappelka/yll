import pandas as pd
import os
import params
import functions


##############################################################################
#                                                                            #
#               Read in life expectancy data for all states                  #
#                                                                            #
##############################################################################
df = pd.DataFrame()
for state in params.STATES:
    file = os.path.join(params.RAW_DATA_PATH, 
                        'life_expectancy',
                        '2020 County Health Rankings {} Data.xlsx'.format(state))
    curr_df = pd.read_excel(file, sheet_name='Additional Measure Data')
        
    # make the top row the column names
    curr_df = curr_df.rename(columns=curr_df.iloc[0]).drop(curr_df.index[0])
    df = df.append(curr_df)


cols_to_keep = ["State",
                "County",
                "Life Expectancy",
                'Life Expectancy (AIAN)',
                "Life Expectancy (Asian)", 
                "Life Expectancy (Black)", 
                "Life Expectancy (Hispanic)", 
                "Life Expectancy (White)"]
    
df_subset = df[cols_to_keep]
    
# there's one row where the County value is missing - the values here are the
# state-level values. 
df_subset = df_subset.dropna(subset=['County'])
    
# rename columns
df_subset.columns = df_subset.columns.str.replace("Life Expectancy", "County Life Expectancy")


df_subset.to_csv(os.path.join(params.CLEAN_DATA_PATH, 'life_expectancy.csv'))

##############################################################################
#                                                                            #
#                           Read in Georgia death data                       #
#                                                                            #
##############################################################################

gadph_df = pd.read_csv(os.path.join(params.RAW_DATA_PATH, 
                                    'deaths',
                                    "GA Race Age Deaths.csv"))
 
#rename columns
gadph_df = gadph_df.rename({'county': 'County'}, axis=1)
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
#                           Read in death data                      #
#                                                                            #
##############################################################################

# read in the CTP death data here
file = os.path.join(params.RAW_DATA_PATH, 
                        'deaths',
                        'Race + Age Data Archive.xlsx')

df = pd.read_excel(file, sheet_name='Public')

df = df.rename(columns=df.iloc[0]).drop(df.index[0])

cols_to_keep = ['State', 
                'Age_Bracket', 
                'Age_Lower', 
                'Age_Upper'] + [x for x in df.columns if 'Deaths' in x]

df = df[cols_to_keep]

# subset to states

##############################################################################                                                                       #
#                 Create a common race variable                              #
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

gadph_df_subset2.to_csv(os.path.join(out_path, 'ga_covid_deaths.csv'))
##############################################################################
#                                                                            #
#                   Read in Georgia county demographic data                          #
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

demo_subset2.to_csv(os.path.join(out_path, 'ga_demographics.csv'))

