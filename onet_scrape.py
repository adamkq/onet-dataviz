# ONET dataviz

import sys
import requests, progressbar
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

# URLs
onet_url = "https://www.onetonline.org/find/family?f=0&g=Go"
onet_summary = "https://www.onetonline.org/link/summary/"
robots_url = "https://willrobotstakemyjob.com/"
requests_except_message = "Exception Raised due to timeout or poor response code. Python Exiting."
KeyboardInterrupt_message = "Script Interrupted by user. Python Exiting."
skip = True

print("Getting O*NET data...")
try:
	response = requests.get(onet_url, timeout=5)
	assert 200 <= response.status_code < 300
except:
	print(requests_except_message)
	sys.exit()

print("Response OK")
print("Tabulating Jobs...")
soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table", border="0")
table2 = table.find_all("tr")

columnNames = ["SOCcode", "JobName", "JobFamily", "isBright", "isGreen"]
jobFamilySkip = ["Military Specific"] # skip these for now; these don't have any data
rows = onet_helper.tabulateONETData(table2, jobFamilySkip)

jobData = pd.DataFrame(rows, columns = columnNames)

jobData.insert(jobData.shape[1], "JobZone", -1)
jobData.insert(jobData.shape[1], "MedianSalary", 0)
jobData.insert(jobData.shape[1], "JobForecast", 0)
jobData.insert(jobData.shape[1], "ChanceAuto", -1.0)
jobData.insert(jobData.shape[1], "WageGroup","")


print(f"{jobData.shape[0]} jobs found.")
print("Scraping O*NET data for each job...")
pbar = progressbar.ProgressBar(maxval=jobData.shape[0])
pbar.start()

for index, row in jobData.iterrows():
	if skip:
		jobData = pd.read_csv('jobData.csv')
		break
	SOCcode = row["SOCcode"]
	# format for O*NET
	link_onet = onet_summary + SOCcode
	
	try:
		jobSummary = onet_helper.getONETSummary(link_onet) # return [Job Zone, Salary, Growth, WageGroup]
	except Exception:
		print(requests_except_message)
		sys.exit()
	except KeyboardInterrupt:
		print(KeyboardInterrupt_message)
		sys.exit()

	jobData.loc[index, "JobZone"] = jobSummary[0]
	jobData.loc[index, "MedianSalary"] = jobSummary[1]
	jobData.loc[index, "JobForecast"] = jobSummary[2]
	jobData.loc[index, "WageGroup"] = jobSummary[3]
	pbar.update(index)
pbar.finish()

print("Scraping 'willrobotstakemyjob' data for each job...")
pbar = progressbar.ProgressBar(maxval=jobData.shape[0])
pbar.start()

for index, row in jobData.iterrows():
	SOCcode = row["SOCcode"]
	jobName = row["JobName"]
	if (str(jobData.loc[index, "WageGroup"]) != 'nan'): # part of group, so it won't have chanceAuto
		continue

	# format for this website
	d_replace = {",":"", "/":"", " ":"-", "--":chr(8211)}
	prefix = robots_url + SOCcode[:-3] + "-"
	# Max URL len is 103-108 chars
	# sometimes 109...
	name = onet_helper.nameRobotsFormat(jobName, d_replace, 108-len(prefix), 103-len(prefix))
	link_robots = prefix + name

	try:
		chanceAuto = onet_helper.getRobots(link_robots) # return [Chance Auto]
	except Exception:
		print(requests_except_message)
		sys.exit()
	except KeyboardInterrupt:
		print(KeyboardInterrupt_message)
		sys.exit()

	jobData.loc[index, "ChanceAuto"] = chanceAuto[0]
	pbar.update(index)
pbar.finish()

jobData.to_csv('jobData.csv',index=False)

print("Script Complete. Press Enter to quit.")
input()

