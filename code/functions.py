# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 14:27:51 2021

@author: hpfla
"""
import params
import pandas as pd
import os

def process_le(is_county, outfilename):
    '''
    processess state or county level life expectancy data
    
    is_county -- a boolean that indicates the data is county level
    outfilename -- a string, the name of the output file
    
    reads in and cleans the data. returns the processed data'''

    # set up
    cols_to_keep = ["State",
                "Life Expectancy",
                'Life Expectancy (AIAN)',
                "Life Expectancy (Asian)", 
                "Life Expectancy (Black)", 
                "Life Expectancy (Hispanic)", 
                "Life Expectancy (White)"]
    if is_county:
        cols_to_keep = cols_to_keep + ["County"]
        id_vars = ["State", "County"]
        states = params.COUNTY_STATES
    else:
        id_vars = ["State"]
        states=params.STATES

    # read in
    df = pd.DataFrame()
    for state in states:
        file = os.path.join(params.RAW_DATA_PATH, 
                            'life_expectancy',
                            '2021 County Health Rankings {} Data.xlsx'.format(state))
        curr_df = pd.read_excel(file, sheet_name='Additional Measure Data')
            
        # make the top row the column names
        curr_df = curr_df.rename(columns=curr_df.iloc[0]).drop(curr_df.index[0])
        df = df.append(curr_df)


    if is_county:
        df2 = df[~df['County'].isna()]
    else:
        df2 = df[df['County'].isna()]

    # subset to columns of interest
    df3 = df2[cols_to_keep]  

    # rename columns
    df4 = df3.rename(columns = {"Life Expectancy":"Life Expectancy (Total)"})

    # transform from wide to long
    df_long = pd.melt(df4, id_vars = id_vars
                    ,var_name="Race"
                    ,value_name="Life Expectancy")

    # Just keep the value within the parens
    df_long["Race"] = df_long['Race'].str.extract(r"\((.*?)\)", expand=False)

    if is_county:
        total_df = df_long[df_long.Race == "Total"]
        total_df = total_df[["State", "County", "Life Expectancy"]]
        total_df = total_df.rename(columns = {"Life Expectancy":"County Life Expectancy"})
        df_long = df_long[~(df_long.Race == "Total")]
        df_long = df_long.rename(columns = {"Life Expectancy": "Race-County Life Expectancy"})
        df_long = pd.merge(df_long, total_df, how="left", on=["State", "County"])

    df_long.to_csv(os.path.join(params.CLEAN_DATA_PATH, outfilename), index=False)

def calc_yll(df, yllname, le, age):
    '''Calculate years of life lost

    Keyword arguments:
    df -- the dataframe
    yllname -- the name of the resulting variable
    le - the life expectacny variable
    age - the age variable

    returns a dataframe with an additional column: years of life lost
    """
    if imag == 0.0 and real == 0.0:
        return complex_zero
    '''
    df[yllname] = (df[le] - df[age]) * df["Deaths"]
    df.loc[df[yllname] < 0, yllname] = 0
    return df
