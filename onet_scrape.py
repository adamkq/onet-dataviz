# ONET dataviz

import sys
import requests
import pandas as pd
from bs4 import BeautifulSoup

import onet_helper

print("="*17 + " O*NET Dataviz " + "="*17)
pre_message = """
Step 1: Collection/Scraping

This step scrapes data from the following websites:
1. https://www.onetonline.org
2. https://willrobotstakemyjob.com/

This process may take several minutes. To continue, press Enter.
To exit, press N, then press Enter.
"""
print(pre_message)
YorN = input()
if "N" in YorN or "n" in YorN:
	sys.exit()

scrape = False
if "-s" in sys.argv:
	scrape = True

# URLs
onet_url = "https://www.onetonline.org/find/family?f=0&g=Go"
onet_summary = "https://www.onetonline.org/link/summary/"
robots_url = "https://willrobotstakemyjob.com/"

print("Getting O*NET data...")
response = requests.get(onet_url)
if not (200 <= response.status_code < 300):
	print("An error occurred when trying to fetch data from the O*NET website. Python Exiting.")
	sys.exit()
else:
	print("Response OK")

print("Tabulating Basic Data...")
soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table", border="0")
table2 = table.find_all("tr")

columnNames = ["SOC Code", "Job Name", "Job Family", "isBright", "isGreen"]
jobFamilySkip = ["Military Specific"] # skip these for now; these are missing data
rows = onet_helper.tabulateONETData(table2, jobFamilySkip)

jobData = pd.DataFrame(rows, columns = columnNames)

jobData.insert(jobData.shape[1], "Job Zone", 1)
jobData.insert(jobData.shape[1], "Avg Salary", 0)
jobData.insert(jobData.shape[1], "Job Forecast", 0)
jobData.insert(jobData.shape[1], "ChanceAuto", 0.1)
jobData.insert(jobData.shape[1], "WageGroup","")

print(f"{jobData.shape[0]} jobs found.")
print("Scraping O*NET data for each job...")
for index, row in jobData.iterrows():
	SOC_code = row["SOC Code"]
	jobName = row["Job Name"]
	# format for O*NET
	link_onet = onet_summary + SOC_code
	# format for this website
	link_robots = robots_url + SOC_code[:-3] + "-" + jobName.lower().replace(",","").replace(" ","-")
	
	jobSummary = onet_helper.getONETSummary(link_onet) # return [Job Zone, Salary, Growth]
	jobData.loc[index, "Job Zone"] = jobSummary[0]
	jobData.loc[index, "Avg Salary"] = jobSummary[1]
	jobData.loc[index, "Job Forecast"] = jobSummary[2]
	jobData.loc[index, "WageGroup"] = jobSummary[3]

print("Scraping 'willrobotstakemyjob' data for each job...")
for index, row in jobData.iterrows():
	chanceAuto = onet_helper.getRobots(link_robots) # return [Chance Auto]
	jobData.loc[index, "ChanceAuto"] = chanceAuto[0]

if False:
	jobData.to_csv('jobData.csv',index=False)

print("Script Complete. Press Enter to quit.")
input() # Press Enter to quit

