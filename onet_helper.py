#ONET_helper
#contains functions for web scraping

import requests
import pandas as pd
from bs4 import BeautifulSoup

def getONETSummary(url_onet):
	'''
	type: a URL to an O*NET summary page
	rtype: List[int] of relevant values
	'''
	ans = []
	jobZone = -1
	salary = -1
	growth = -1 # Job Zone, Salary, Growth
	wageGroup = "" # some jobs have their wage data taken from a larger category of jobs

	try:
		response = requests.get(url_onet)
	except KeyboardInterrupt:
		raise
	soup = BeautifulSoup(response.text, "html.parser")
	
	jobZoneTable = soup.find("table", summary="Job Zone information for this occupation")
	if jobZoneTable: # not all occupations have this
		jobZoneTable = jobZoneTable.find("td", class_="report2") # The first such entry has the actual Job Zone
		zoneToIntMap = {"One":1, "Two":2, "Three":3, "Four":4, "Five":5}
		for key in zoneToIntMap.keys():
			if key in jobZoneTable.contents[0]:
				jobZone = zoneToIntMap[key]

	wagesEmployment = soup.find("div", id="wrapper_WagesEmployment")
	wagesCollectedFrom = wagesEmployment.find_all("p", class_="sm")
	wageTable = wagesEmployment.find_all("tr")

	if "wages" in wagesCollectedFrom[1].contents[0]: # wage group exists
		wageGroup = str(wagesCollectedFrom[1].contents[1].contents[0])

	salary_str = wageTable[0].contents[3].contents[0]
	if "annual" in salary_str:
		salary_str = salary_str.split(", ")[-1] # split between hourly and annual wage, not on numerical commas

	try:
		growth_str = wageTable[5].contents[3].contents[0] # this field is missing from some jobs
	except:
		growth_str = "0"

	salary = float(salary_str[1:-7].replace(",","").replace("+","")) # remove $, +, 'annual'/'hourly', and comma
	growth = int(growth_str.replace(",",""))
	ans.extend([jobZone, salary, growth, wageGroup])
	return ans

def getRobots(url_robots):
	'''
	type: a URL to a 'will robots take my job' summary page
	rtype: List[float] of relevant values
	'''
	ans = [-1.0] # data not found
	MAX_LEN = 104 # max url size of website
	if len(url_robots) > MAX_LEN:
		url_robots = url_robots[:MAX_LEN]
		url_robots += '-'

	try:
		response = requests.get(url_robots)
	except KeyboardInterrupt:
		raise

	soup = BeautifulSoup(response.text, "html.parser")
	table = soup.find("div", class_="probability")
	if table:
		ans[0] = float(table.contents[0][:-1])
	return ans

def tabulateONETData(table, jobFamilySkip=[]):
	'''
	type: a suitable bs4 object, and an optional list of Job Families to skip
	rType: a list of rows to be formatted into a dataframe
	'''
	
	rows = []

	for i, element in enumerate(table):
		ans = []
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
					

		ans.extend([SOC_code, jobName, jobFamily, isBright, isGreen])
		rows.append(ans)
	return rows
	