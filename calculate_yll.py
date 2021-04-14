# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 21:20:21 2021

@author: hpfla
"""

# read in life expectancy

import params
import pandas as pd
import os

# life expectancy for state by race
le = pd.read_csv(os.path.join(params.CLEAN_DATA_PATH, 'state_life_expectancy.csv'))

# deaths for state
deaths = pd.read_csv(os.path.join(params.CLEAN_DATA_PATH, 'deaths_cleaned.csv'))

# merge datasets together
df = deaths.merge(le, how="left", on =["State", "Race"])
# TODO examine why result of merge has more observations

df["YLL (based on age bracket median)"] = df["Life Expectancy"] - df["Bracket_Median_Age"]
df["YLL (based on upper age in bracket)"]  = df["Life Expectancy"] - df["Age_Upper"]
# TODO add weighted mean age calc

# TODO determine why some states are missing data

x=1
