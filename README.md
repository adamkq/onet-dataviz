# onet-dataviz
A project to scrape, tabulate, and display job data from the O*NET website, and possibly other websites. Non-commercial. 

Jobs are indexed by their SOC Code, a unique idetifier (e.g. 35-3022.01 for Baristas)

Scraper does the following:
1. Create a pandas dataframe with the following headings:
        SOC code, Job Name, Job Family
2. Go to O*NET all occupations page and extract the relevant HTML from the main table element on that page.
3. Fill in the appropriate data into the columns in step 1.
4. Extend the table with columns:
        Job Zone, Avg Salary, Jobs Forecast, Chance of Automation, WageGroup
5. For each existing row, query the O*NET website to get the associated summary data for that job. Extract the values for the columns listed in step 4, except "Chance of Automation', and write it to the dataframe. If the data does not exist, use a default value that is outside the domain of possible valid values.
6. For each existing row, query the website 'https://willrobotstakemyjob.com' and find the value for 'Chance of Automation'. Write it to the dataframe. If the data does not exist, use a default value that is outside the domain of possible valid values.
7. Write the dataframe to an external file.

Analysis does the following:
1. Read in an existing jobData dataframe from an external file. No scraping or requests in this script.
2. Clean up data that is missing or inconsistently formatted. For example, a few jobs have hourly wages listed instead of salaries. These should be converted, e.g. assuming 2000 hours/yr of work. 
3. Group jobs based on "WageGroup" category, if they have one. Such jobs source their wage data from a larger overall employment category.
- If the "WageGroup" category exists as its own job, then this field should not yet have a job Zone value. Write the most common job Zone value among all jobs in the WageGroup category to the corresponding row. If there is a tie, choose the higher one. The "ChanceAuto" value should already exist. 
- If the value does not exist, create it and do the same. The "ChanceAuto" value shall be taken as the weighted sum of all ChanceAuto values in the category, based on "Job Forecast" value.
- Remove all rows from the table which have a "WageGroup" category.
4. Determine summary data which could reveal useful trends or benchmarks. Some examples include:
- Median wage non-college (Job Zones 1-3)
- Median wage college (Job Zones 4-5)
- Average ChanceAuto, non-college
- Average ChanceAuto, college
5. Format the raw data and summary data into a chart using matplotlib.
