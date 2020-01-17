# onet-dataviz
A project to scrape, tabulate, and display job data from the O*NET website, and possibly other websites. Non-commercial. 

Intended Method:
1. Create a pandas table with the following headings:
	SOC code (6 digits, unique, e.g. for Nuclear Engineers: 17-2161), Job Name, Job Family, Job Zone, Avg Salary, Jobs Forecast, Chance of Automation
2. Go to all occupations page: https://www.onetonline.org/find/zone?z=0&s=0
3. For each job, follow the link provided and get the following:
		Number of New Jobs Forecasted, Avg Salary, Job Zone, SOC code 
4. Format this data into the pandas table.
5. For each job, go to google and type in "site:https://willrobotstakemyjob.com/ <SOC code>"
6. Follow the first result link (only one should appear)
7. Obtain the chance of automation
8. Add that chance to the corresponding column in the table
9. Determine summary data:
- Average wage non-college (Job Zones 1-3)
- Average wage college (Job Zones 4-5)
- Average ChanceAuto, non-college
- Average ChanceAuto, college
10. Format the raw data and summary data into a chart using matplotlib
