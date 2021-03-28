# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 14:27:51 2021

@author: hpfla
"""
import params
import pandas as pd
import os

def read_in_le():
    df = pd.DataFrame()
    for state in params.STATES:
        print(state)
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
    return le_df_subset