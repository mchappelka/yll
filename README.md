# Overview
We seek to quantify the years of life lost due to COVID in Georgia, using race and county specific life expectancy.  

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
* Create a common race variable

# Contributors
Miriam Chappelka <br/>
Charlotte Minsky <br/>
Alice Goldfarb <br/>
