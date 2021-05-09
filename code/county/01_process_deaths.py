
import sys 
import pandas as pd
import os

sys.path.insert(1, "C:/Users/hpfla/OneDrive/Documents/Covid_Tracking_Project/life_expectancy/yll/code")
import functions
import params
##############################################################################
#                                                                            #
#                           Read in Georgia death data                       #
#                                                                            #
##############################################################################

df = pd.read_csv(os.path.join(params.RAW_DATA_PATH, 
                                    'deaths',
                                    "GA Race Age Deaths.csv"))
 


#rename columns
df = df.rename({'county': 'County'}, axis=1)
cols_to_keep = ['ethnicity', 'race', 'sex', 'County', 'age']

df_subset = df[cols_to_keep]

# drop rows where the age column doesn't have an age value 
df_subset = df_subset[df_subset.age != "." ]
df_subset = df_subset[df_subset.age != "We haven't run out of rows yet" ]

#convert age to numeric
df_subset["age"] = pd.to_numeric(df_subset["age"])

# drop rows where every value is missing
df_subset2 = df_subset.dropna(how='all')

# Check county values
df_subset2["County"].unique()

# how often do non county values occur
df_subset2[df_subset2.County == "Non-GA Resident/Unknown State"].count()
df_subset2[df_subset2.County == "Unknown"].count()

# drop non-county values
df_subset2 = df_subset2[df_subset2.County != "Non-GA Resident/Unknown State"]
df_subset2 = df_subset2[df_subset2.County != "Unknown"]

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

df_subset2["new_race"] = df_subset2.apply(
    lambda x: "Hispanic" if x['ethnicity']=='Hispanic/ Latino' 
        else ("Black" if x["race"] == "African-American/ Black"
            else x['race']), axis=1
    )

# Check new race variable
df_subset2.groupby(['ethnicity', 'race', 'new_race'], as_index=False).size()



# delete if new_race is AIAN, NHPI, other, or unknown
df_subset2 = df_subset2[df_subset2.new_race != "American Indian/ Alaska Native" ]
df_subset2 = df_subset2[df_subset2.new_race != "Native Hawaiian/ Pacific Islander" ]
df_subset2 = df_subset2[df_subset2.new_race != "Other" ]
df_subset2 = df_subset2[df_subset2.new_race != "Unknown" ]

# drop old race variable
df_subset2 = df_subset2.drop(columns=['race'])
# rename columns
df_subset2 = df_subset2.rename(columns = {"new_race":"Race"})


# create a deaths column. This is to have the data in the same format as the state data
# and to use for aggregating
df_subset2["Deaths"] = 1

# output data ##############################################################################
df_subset2.to_csv(os.path.join(params.CLEAN_DATA_PATH, "county_deaths.csv"), index=False)