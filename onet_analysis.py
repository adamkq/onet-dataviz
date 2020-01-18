#onet_analysis

import pandas as pd
import numpy as np
import matplotlib

print("="*17 + " O*NET Dataviz " + "="*17)
pre_message = """
Step 2: Analysis

This step analyzes job data from an existing file. In particular:
1. Jobs with an hourly wage are replaced with an equivalent salary. Such jobs
  * are in Arts & Entertainment and have highly irregular hours
2. Jobs which have the same "WageGroup" value are grouped into a single entry, in which:
  * the Job Zone value is taken as the most common Job Zone value of the set (highest 
	in case of a tie)
  * The Chance of Automation value is taken as the weighted average of all such values 
	based on the Jobs Forecast value.
3. Relevant summary values are found.
"""
print(pre_message)

print("Loading data from file...")

jobData = pd.read_csv('jobData.csv')

print("Columns:")
print(list(jobData.columns.array))

print(jobData[jobData["WageGroup"].notna()]) # these jobs are part of a Wage Group
print(jobData[jobData["Avg Salary"] < 1000])

jobZoneCounts = []
for i in range(1,6):
	jobZoneCounts.append(len(jobData.loc[(jobData["Job Zone"]) == i].index))
print("Job Zone Counts: ",jobZoneCounts)

jobStandard = jobData.loc[(jobData["Job Zone"] > 0) & (jobData["ChanceAuto"] > 0)] # get rid of filler values
print(jobStandard.describe())