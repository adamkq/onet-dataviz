# ONET dataviz

import os, sys, time
import matplotlib, csv, json, requests 
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup



'''
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
'''

onet_url = "https://www.onetonline.org/find/family?f=0&g=Go"
response = requests.get(onet_url)
if not (200 <= response.status_code < 300):
	print("An error occurred when trying to fetch data from the O*NET website. Python Exiting.")
	sys.exit()
else:
	print("Response OK")

soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table", border="0")
table2 = table.find_all("tr")
columnNames = ["SOC Code", "Job Name", "Job Family", "isBright", "isGreen"] # iterate to get: Job Zone, Avg Salary, Jobs Forecast, 
rows = []

# get the column Names listed above
# There is an option to download CSV data for this, but it does not include Bright/Green data
for i, element in enumerate(table2):
	if i == 0: # first entry is the table header, which is formatted differently
		continue
	tags = element.find_all("td")
	allContents = []
	for tag in tags:
		allContents.extend(tag)

	isBright = False # Occupation has 'bright outlook' designation
	isGreen = False # Occupation has 'green' designation
	SOC_code = str(allContents[0])
	jobName = str(allContents[1].contents[0])
	jobFamily = str(allContents[-1])
	if jobFamily == "Military Specific": # skip these for now; these are missing data
		continue

	if len(allContents) > 4: # may be bright or green
		for index, j in enumerate(allContents):
			if 'Tag' in str(type(j)):
				if "Bright Outlook" in j.attrs.values():
					isBright = True
				if "Green" in j.attrs.values():
					isGreen = True
				
	rows.append([SOC_code, jobName, jobFamily, isBright, isGreen])


jobData = pd.DataFrame(rows, columns = columnNames)
print(jobData.shape)
jobData.insert(jobData.shape[1], "Job Zone", 1)
jobData.insert(jobData.shape[1], "Avg Salary", 0)
jobData.insert(jobData.shape[1], "Job Forecast", 0)
jobData.insert(jobData.shape[1], "ChanceAuto", 0.1)
print(jobData)

for index, row in jobData.iterrows():
	link = "https://www.onetonline.org/link/summary/" +row["SOC Code"
	# row = getSummaryData(link)
	print(link)
	if index == 4:
		break

