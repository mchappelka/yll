# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 14:21:09 2021

@author: hpfla
"""

import os
LOCAL_PATH = "C:/Users/hpfla/OneDrive/Documents/Covid_Tracking_Project/life_expectancy"
REPO_PATH = os.path.join(LOCAL_PATH, "yll")

PROG_PATH = os.path.join(REPO_PATH, "code")

RAW_DATA_PATH = os.path.join(LOCAL_PATH, "data", "000_raw_data")
OUT_PATH = os.path.join(REPO_PATH, "data\output")
CLEAN_DATA_PATH = os.path.join(OUT_PATH, "intermediate_cleaned")
ANALYTIC_PATH = os.path.join(OUT_PATH, "final_analytic")

STATES = ["Michigan", 
          "California", 
          "Illinois", 
          "New Mexico", 
          "South Dakota"]

COUNTY_STATES = ["Georgia"]