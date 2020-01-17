# ONET dataviz

import os, sys, time
import matplotlib, csv, json, requests 
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

def tabulateData(table):
	'''
	Returns a pandas dataframe given a suitable bs4 object
	'''
	jobFamilySkip = ["Military Specific"] # skip these for now; these are missing data
	columnNames = ["SOC Code", "Job Name", "Job Family", "isBright", "isGreen"] # iterate to get: Job Zone, Avg Salary, Jobs Forecast, 
	rows = []

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
		if jobFamily in jobFamilySkip:
			continue

		if len(allContents) > 4: # may be bright or green
			for item in allContents:
				if 'Tag' in str(type(item)):
					if "Bright Outlook" in item.attrs.values():
						isBright = True
					if "Green" in item.attrs.values():
						isGreen = True
					
		rows.append([SOC_code, jobName, jobFamily, isBright, isGreen])


	jobData = pd.DataFrame(rows, columns = columnNames)
	jobData.insert(jobData.shape[1], "Job Zone", 1)
	jobData.insert(jobData.shape[1], "Avg Salary", 0)
	jobData.insert(jobData.shape[1], "Job Forecast", 0)
	jobData.insert(jobData.shape[1], "ChanceAuto", 0.1)
	return jobData

print("="*10, "O*NET Dataviz", "="*10)
scrape = False
onet_url = "https://www.onetonline.org/find/family?f=0&g=Go"

if (scrape):
	print("Getting O*NET data...")
	response = requests.get(onet_url)
	if not (200 <= response.status_code < 300):
		print("An error occurred when trying to fetch data from the O*NET website. Python Exiting.")
		sys.exit()
	else:
		print("Response OK")

	soup = BeautifulSoup(response.text, "html.parser")
	table = soup.find("table", border="0")
	table2 = table.find_all("tr")

	jobData = tabulateData(table2)
	jobData.to_csv('jobData.csv',index=False)

else:
	print("Loading data from file...")
	jobData = pd.read_csv('jobData.csv')

for index, row in jobData.iterrows():
	link = "https://www.onetonline.org/link/summary/" + row["SOC Code"]
	# row = getSummaryData(link)
	print(link)
	if index == 4:
		break

input() # Press Enter to quit

