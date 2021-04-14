# this is for the deaths in the following states: 
# these states have the following structure for their data: 
import params
import os
import pandas as pd
import us
##############################################################################
#                                                                            #
#                           Read in death data                               #
#                                                                            #
##############################################################################

file = os.path.join(params.RAW_DATA_PATH, 
                            'deaths',
                            'Race + Age Data Archive.xlsx')
    
df = pd.read_excel(file, sheet_name='Public', engine="openpyxl")
    
df = df.rename(columns=df.iloc[0]).drop(df.index[0])
    
cols_to_keep = ['State', "Date_Update", 
                    'Age_Bracket', 
                    'Age_Lower', 
                    'Age_Upper',
                    'Deaths_Total', 'Deaths_White', 'Deaths_Black', 'Deaths_Latinx',
       'Deaths_Asian', 'Deaths_AIAN']

df = df[cols_to_keep]

# Recode states as long name
df["State"] = df.State.replace(us.states.mapping('abbr', 'name'))


# subset to just the most recent data on cumulative deaths for each state

max_df = df.groupby(['State']).agg({ 'Date_Update': max}).reset_index().rename(columns={"Date_Update": "Max Date"})
df = df.merge(max_df, how="left", on="State")
df = df[df["Date_Update"] == df["Max Date"]]
# drop intermediate column
df = df.drop(['Max Date', "Date_Update"], axis=1)  


# drop unknown age since we can't use them to calculate YLL
df = df[df.Age_Bracket != "Unknown_Reported"]

# Transform from long to wide
df = pd.melt(df ,id_vars =['State', "Age_Bracket", "Age_Lower", "Age_Upper"]
                ,var_name="Race"
                ,value_name="Deaths")

# drop "Deaths_" from race
df["Race"] = df.Race.str.replace("Deaths_", "")
df["Race"] = df.Race.str.replace("Latinx", "Hispanic")

# Convert values numeric
cols = ['Age_Lower', 'Age_Upper', 'Deaths']
df[cols] = df[cols].apply(pd.to_numeric, errors='coerce', axis=1)
df["Bracket_Median_Age"] = df[["Age_Lower", "Age_Upper"]].mean(axis=1)

# df["Bracket_Weighted_Mean_Age"] = #TODO read in Charlottes' data

 
df.to_csv(os.path.join(params.CLEAN_DATA_PATH, 'deaths_cleaned.csv'), index=False)
    

