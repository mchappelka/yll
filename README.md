# Overview
We seek to quantify the years of life lost due to COVID-19 in Georgia, using race and county specific life expectancy. Georgia was chosen because the race, age, and county is reported for each recorded COVID-19 death. 

# Data sources
* GA county life expectancy by race: https://www.countyhealthrankings.org/app/georgia/2020/measure/outcomes/147/data 
* GA race and population demographic data: https://www.census.gov/data/tables/time-series/demo/popest/2010s-counties-detail.html 
* Death data: https://docs.google.com/spreadsheets/d/1naiRW57-uPggIPpDN5OFKwcBfCokiyxh0YgW1iCdLD0/edit#gid=0  

# Specifications
* Read in the death data.  
    * Drop observations where the county of residence is not Georgia (will say "Non-GA Resident/Unknown State" or "Unknown") 
* Read in GA demographic data. This will help us give us the racial demographics of each county as well as the county population, which can help us understand if small population sizes might be contributing to extreme life expectancy values.  <br/>
    * Filter the dataset to include only the most recent population estimates (from 2019). 
        * These will have a YEAR value of 12. (This comes from the Census' file layout document : https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2010-2019/cc-est2019-agesex.pdf)
    * Filter the data to include only the county level total (as opposed to age-county level total)
        * These will have an AGEGRP value of 0. (also comes from Census' file layout document)
    * This file has total population by race and gender for each county, but not total population by race for all genders. Sum the male and female columns from each race to calculate the total population for each race. 
* Read in life expectancy data
* Create a new race variable in the death data. The County Health Rankings life expectancy data categorizes people as AIAN (American Indian/Alaska Native), Asian, Black, Hispanic, and White. The Georgia Department of Public Health death data categorizes people as African-American/Black, White, Other, American Indian/Alaska Native, Unknown, Asian, Native Hawaiian/ Pacific Islander, and separately tracks their ethnicity (whether they are Hispanic or not). In order to combine these datasets, we need to have a common definition of race/ethnicity
    * Anyone who has Hispanic ethnicity will be categorized as Hispanic, regardless of race. 
    * Everyone without Hispanic ethnicity will be categorized based on their race. 
    * Since we have too little data for people of these races, drop anyone categorized as: American Indian/ Alaska Native, Native Hawaiian/ Pacific Islander, Other, Unknown
 * Merge data sets together
     * Left join death data with life expectancy data, using County as the merge variable.
     * Left join the resulting data set with demographic data, using County as the merge variable.
 * Calculate years of potential life lost due to COVID-19 (YLL), 
     * YLL, stratified by race and county
         * Calculate years of life lost by subtracting the life expectancy (based on race and county) from age at death
         * If the age at death is greater than life expectany, set YLL to 0.
     * YLL, stratified by county; not stratified by race
         * Calculate years of life lost by subtracting the life expectancy (based on county) from the age of death
         * If the age at death is greater than life expectany, set YLL to 0.
 * Analyze the data
     * Mean age at death, by race
     * Number of deaths, by race
     * For both YLL calculations (race-county and just county), output the following:
         * Distribution (min, 25th percentile, median, 75Th percentile, max, mean standard deviation) of YLL by race
         * Sum of YLL, by race 
         * Mean YLL, by race

# Notes
# Limitations       
# References 
# Contributors
From the COVID Tracking Project:
Miriam Chappelka <br/>
Charlotte Minsky <br/>
Alice Goldfarb <br/>
