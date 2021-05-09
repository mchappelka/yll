import pandas as pd
import sys
import os

sys.path.insert(1, "C:/Users/hpfla/OneDrive/Documents/Covid_Tracking_Project/life_expectancy/yll/code")
import params


##############################################################################
#                                                                            #
#               Read in life expectancy data                                 #
#                                                                            #
##############################################################################
le_df = pd.read_csv(os.path.join(params.CLEAN_DATA_PATH, 'county_life_expectancy.csv'))



##############################################################################
#                                                                            #
#                           Read in death data                               #
#                                                                            #
##############################################################################

deaths_df = pd.read_csv(os.path.join(params.CLEAN_DATA_PATH, 'county_deaths.csv'))

# Frequency of race and ethnicity variables
deaths_df.groupby(['ethnicity'], as_index=False).size()
deaths_df.groupby(['Race'], as_index=False).size()
deaths_df.groupby(['ethnicity', 'Race'], as_index=False).size()

deaths_df["County"].unique()

##############################################################################
#                                                                            #
#                           Read in analytic file                     #
#                                                                            #
##############################################################################
analytic_df = pd.read_csv(os.path.join(params.ANALYTIC_PATH, 'county_analytic_file.csv'))
##############################################################################
#                                                                            #
#                      Calculate summary statistics                          #
#                                                                            #
##############################################################################

yll_dist = analytic_df.groupby(["Race"])[["YLL_county", "YLL_racecounty"]].describe().round(1)
mean_age = analytic_df.groupby(["Race"])["age"].mean().round(1)
total_yll = analytic_df.groupby(["Race"])[["YLL_county", "YLL_racecounty"]].sum()
mean_yll = analytic_df.groupby(["Race"])[["YLL_county", "YLL_racecounty"]].mean().round(1)
num_deaths = pd.value_counts(analytic_df.Race)


with pd.ExcelWriter(os.path.join(params.ANALYTIC_PATH,"county_exploratory_analysis.xlsx")) as writer: 
    num_deaths.to_excel(writer, sheet_name='num_deaths') 
    mean_age.to_excel(writer, sheet_name='mean_death_age')
    yll_dist.to_excel(writer, sheet_name='dist_yll')
    total_yll.to_excel(writer, sheet_name='sum_yll')
    mean_yll.to_excel(writer, sheet_name='mean_yll')
