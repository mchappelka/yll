import pandas as pd
import os

##############################################################################
#                                                                            #
#               Set programming variables                                    #
#                                                                            #
##############################################################################

base_path = "C:/Users/hpfla/OneDrive/Documents"
prog_path = os.path.join(base_path, "Covid_Tracking_Project/life_expectancy")
in_path = os.path.join(prog_path, "data/100_cleaned_data") 
out_path = os.path.join(prog_path, "data/output") 
##############################################################################
#                                                                            #
#               Read in life expectancy data                                 #
#                                                                            #
##############################################################################
le_df = pd.read_csv(os.path.join(in_path, 'ga_life_expectancy.csv'))

##############################################################################
#                                                                            #
#                          Examine the data                                  #
#                                                                            #
##############################################################################

# Summary of life expectancy values
le_summary = le_df[['County Life Expectancy', 'County Life Expectancy (AIAN)',
       'County Life Expectancy (Asian)', 'County Life Expectancy (Black)',
       'County Life Expectancy (Hispanic)', 'County Life Expectancy (White)']].describe().round(1)

# Examine counties where black life expectancy > white life expectancy
ledf_sub_bw =  le_df[le_df["County Life Expectancy (Black)"] > le_df["County Life Expectancy (White)"]]

# Examine counties where hispanic life expectancy > 90
ledf_sub_hisp =  le_df[le_df["County Life Expectancy (Hispanic)"] > 90]

##############################################################################
#                                                                            #
#                           Read in death data                               #
#                                                                            #
##############################################################################

deaths_df = pd.read_csv(os.path.join(in_path, 'ga_covid_deaths.csv'))

# Frequency of race and ethnicity variables
deaths_df.groupby(['ethnicity'], as_index=False).size()
deaths_df.groupby(['race'], as_index=False).size()
deaths_df.groupby(['ethnicity', 'race'], as_index=False).size()

deaths_df["County"].unique()

##############################################################################
#                                                                            #
#                           Read in analytic file                     #
#                                                                            #
##############################################################################
analytic_df = pd.read_csv(os.path.join(out_path, 'analytic_file.csv'))
##############################################################################
#                                                                            #
#                      Calculate summary statistics                          #
#                                                                            #
##############################################################################

yll_dist = analytic_df.groupby(["new_race"])[["YLL_county", "YLL_racecounty"]].describe().round(1)
mean_age = analytic_df.groupby(["new_race"])["age"].mean().round(1)
total_yll = analytic_df.groupby(["new_race"])[["YLL_county", "YLL_racecounty"]].sum()
mean_yll = analytic_df.groupby(["new_race"])[["YLL_county", "YLL_racecounty"]].mean().round(1)
num_deaths = pd.value_counts(analytic_df.new_race)


# Examine counties where black life expectancy > white life expectancy
bw_df = analytic_df[analytic_df["County Life Expectancy (Black)"] > analytic_df["County Life Expectancy (White)"]]
bw_df = bw_df[["County", "County Life Expectancy (Black)", "County Life Expectancy (White)", "TOT_POP", "WA_TOT", "BA_TOT", "AA_TOT", "WA_pct", "BA_pct", "AA_pct" ]]
bw_df = bw_df.drop_duplicates()

# Examine counties where hispanic life expectancy > 90
hisp_df =  analytic_df[analytic_df["County Life Expectancy (Hispanic)"] > 90]
hisp_df = hisp_df[["County", "County Life Expectancy (Hispanic)", "TOT_POP", "NH_TOT", "H_TOT", "NH_pct", "H_pct" ]]
hisp_df = hisp_df.drop_duplicates()

with pd.ExcelWriter(os.path.join(out_path,"exploratory_analysis.xlsx")) as writer: 
    num_deaths.to_excel(writer, sheet_name='num_deaths') 
    mean_age.to_excel(writer, sheet_name='mean_death_age')
    yll_dist.to_excel(writer, sheet_name='dist_yll')
    total_yll.to_excel(writer, sheet_name='sum_yll')
    mean_yll.to_excel(writer, sheet_name='mean_yll')
    bw_df.to_excel(writer, sheet_name='black_le_over_white')
    hisp_df.to_excel(writer, sheet_name='hispanic_le_over90') 
