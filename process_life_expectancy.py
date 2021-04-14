##############################################################################
#                                                                            #
#               Create a table of state-level life expectancy data           #
#                                                                            #
##############################################################################
import pandas as pd
import os
import params
import us



df = pd.DataFrame()
for state in params.STATES:
    file = os.path.join(params.RAW_DATA_PATH, 
                        'life_expectancy',
                        '2021 County Health Rankings {} Data.xlsx'.format(state))
    curr_df = pd.read_excel(file, sheet_name='Additional Measure Data')
        
    # make the top row the column names
    curr_df = curr_df.rename(columns=curr_df.iloc[0]).drop(curr_df.index[0])
    df = df.append(curr_df)


df = df[df['County'].isna()]

cols_to_keep = ["State",
                "Life Expectancy",
                'Life Expectancy (AIAN)',
                "Life Expectancy (Asian)", 
                "Life Expectancy (Black)", 
                "Life Expectancy (Hispanic)", 
                "Life Expectancy (White)"]
    
df = df[cols_to_keep]  
# rename columns
df = df.rename(columns = {"Life Expectancy":"Life Expectancy (Total)"})

# transform from wide to long
df_long = pd.melt(df, id_vars =['State']
                ,var_name="Race"
                ,value_name="Life Expectancy")

# Just keep the value within the parens
df_long["Race"] = df_long['Race'].str.extract(r"\((.*?)\)", expand=False)

df_long.to_csv(os.path.join(params.CLEAN_DATA_PATH, 'state_life_expectancy.csv'), index=False)


