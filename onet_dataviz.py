# ONET dataviz

import os, sys
import matplotlib, requests 
import pandas as pd
from bs4 import BeautifulSoup
from googlesearch import search

import onet_helper

scrape = False
if "-s" in sys.argv:
	scrape = True
onet_url = "https://www.onetonline.org/find/family?f=0&g=Go"

print("="*17 + " O*NET Dataviz " + "="*17)
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

	jobData = onet_helper.tabulateONETData(table2)
	jobData.to_csv('jobData.csv',index=False)

else:
	print("Loading data from file...")
	jobData = pd.read_csv('jobData.csv')

for index, row in jobData.iterrows():
	if not scrape:
		break
	SOC_code = row["SOC Code"]
	jobName = row["Job Name"]
	# format for O*NET
	link_onet = "https://www.onetonline.org/link/summary/" + SOC_code
	# format for this website
	link_robots = "https://willrobotstakemyjob.com/" + SOC_code[:-3] + "-" + jobName.lower().replace(",","").replace(" ","-")
	
	jobSummary = onet_helper.getONETSummary(link_onet) # return [Job Zone, Salary, Growth]
	jobData.loc[index, "Job Zone"] = jobSummary[0]
	jobData.loc[index, "Avg Salary"] = jobSummary[1]
	jobData.loc[index, "Job Forecast"] = jobSummary[2]
	chanceAuto = onet_helper.getRobots(link_robots) # return [Chance Auto]
	jobData.loc[index, "ChanceAuto"] = chanceAuto[0]

print("High Payers")
print(jobData.loc[(jobData["Avg Salary"] > 110000)].sort_values(by = ["Avg Salary"], ascending=False))
print("Low Payers")
print(jobData.loc[(jobData["Avg Salary"] < 30000)].sort_values(by = ["Avg Salary"]))
print("High Growth")
print(jobData.loc[(jobData["Job Forecast"] > 100000)].sort_values(by = ["Job Forecast"], ascending=False))
print("Low Growth")
print(jobData.loc[(jobData["Job Forecast"] < 1000)].sort_values(by = ["Job Forecast"]))
#jobData.to_csv('jobData.csv',index=False)


print("Script Complete. Press Enter to quit.")
input() # Press Enter to quit

