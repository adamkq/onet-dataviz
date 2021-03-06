# onet-dataviz
A project to scrape and analyze job/labor data from multiple websites. Non-commercial. 

Jobs are uniquely identified by their SOC Code (e.g. 35-3022.01 for Baristas)

Scraper does the following:
1. Create a pandas dataframe with the following headings:
        SOC code, Job Name, Job Family
2. Go to O*NET all occupations page and extract the relevant HTML from the main table element on that page.
3. Fill in the appropriate data into the columns in step 1.
4. Extend the table with columns:
        Job Zone, Avg Salary, Jobs Forecast, Chance of Automation, WageGroup
5. For each existing row, query the O*NET website to get the associated summary data for that job. Extract the values for the columns listed in step 4, except "Chance of Automation', and write it to the dataframe. If the data does not exist, use a default value that is outside the domain of possible valid values.
6. For each existing row, query the website willrobotstakemyjob.com and find the value for 'Chance of Automation'. Write it to the dataframe. If the data does not exist, use a default value that is outside the domain of possible valid values.
7. Write the dataframe to an external file.

Analysis does the following:
1. Read in an existing jobData dataframe from an external file. No scraping or requests in this script.
2. Clean up data that is missing or inconsistently formatted.
3. Reduce the data.
4. Determine summary data which could reveal useful trends or benchmarks.
5. Format the data into a chart.

Note: The default value for chance of automation is '-1'. Jobs may have this value for one or more reasons:
1. The job is not present in the willrobotstakemyjob.com database.
2. The URL is formatted inconsistently, so onet_scrape.py can't find it. 
3. The job has a different name between O*NET and willrobotstakemyjob.com.
