# Overview
We seek to quantify the years of life lost due to COVID-19 in California, Georgia, Illinois, Michigan, New Mexico and South Dakota using race and geography specific (county or state) life expectancy. 

# Data sources used
* Life expectancy data: https://www.countyhealthrankings.org/app/georgia/2021/downloads
* GA race and population demographic data: https://www.census.gov/data/tables/time-series/demo/popest/2010s-counties-detail.html 
* Georgia person-level death data: https://docs.google.com/spreadsheets/d/1naiRW57-uPggIPpDN5OFKwcBfCokiyxh0YgW1iCdLD0/edit#gid=0 
* State level death data: https://docs.google.com/spreadsheets/d/1e4jogN9bryY8Odb2AaIavLNN-MnMU3hsdeQTWeVhCRo/edit#gid=1019753044

# Notes
* High Hispanic life expectancy in some counties might be due to the Hispanic mortality paradox, small populations within counties, and/or right-censoring of the data. 
* in the state_yll.xlsx, weighted mean age was calculated using the 2000 US standard age distribution

# Limitations
* The life expectancy data we used was county or state-level. This may obscure variation occuring within those geographic units. 
* Life expectancy data is subject to right-censoring (https://www.nature.com/articles/palcomms201549) which may result in overestimates, especially in small counties. 
* Although it is standard to recode race and ethnicity as we did, these assignments may not match how individuals identify or how they experience the world.
* In the death data from Georgia, anyone over 90 was categorized as being 90 years old. For groups whose life expectancy was over 90, this could result in overestimating years of potential life lost, because the deaths of anyone 91 or older will be categorized as occuring when they were younger (90). 

# References 
Abraído-Lanza, A F et al. “The Latino mortality paradox: a test of the "salmon bias" and healthy migrant hypotheses.” American journal of public health vol. 89,10 (1999): 1543-8. doi:10.2105/ajph.89.10.1543 <br/><br/>
Boing, Antonio Fernando, et al. “Quantifying and Explaining Variation in Life Expectancy at Census Tract, County, and State Levels in the United States.” PNAS, National Academy of Sciences, 28 July 2020, www.pnas.org/content/117/30/17688. <br/><br/>
Luy M, Di Giulio P, Di Lego V, Lazarevič P, Sauerberg M: Life Expectancy: Frequently Used, but Hardly Understood. Gerontology 2020;66:95-104. doi: 10.1159/000500955 <br/><br/>
Goldstein, Joshua R., and Ronald D. Lee. “Demographic Perspectives on Mortality of Covid-19 and Other Epidemics.” NBER, 27 Apr. 2020, www.nber.org/papers/w27043. <br/><br/>
Turra CM, Elo IT. The Impact of Salmon Bias on the Hispanic Mortality Advantage: New Evidence from Social Security Data. Popul Res Policy Rev. 2008;27(5):515-530. doi: 10.1007/s11113-008-9087-4. PMID: 19122882; PMCID: PMC2546603.

# Contributors 
Miriam Chappelka <br/>
Charlotte Minsky <br/>
Alice Goldfarb <br/>
