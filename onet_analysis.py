#onet_analysis

import pandas as pd
import numpy as np
import matplotlib as plt
import plotly.express as px
import plotly.graph_objects as go
import math

pd.set_option('display.max_rows', 100)

print("="*17 + " O*NET Dataviz " + "="*17)
pre_message = """
Step 2: Analysis

This step analyzes job data from an existing file. In particular:
1. Jobs with an hourly wage are removed. Such jobs are in Arts & Entertainment and 
  do not have regular hours.
2. Jobs which have the same "WageGroup" value are grouped into a single entry. If there is
  a given value missing from this entry, use the average of all sub-entries (rounding as necessary).
3. Entries which do not have both a value for 'Job Zone' and 'Chance of Automation' are removed.
4. Relevant summary values are found.

This will also print a plot, which will appear in a browser window.
"""
print(pre_message)

print("Loading data from file...")
jobData = pd.read_csv('jobData.csv')
print("Columns:")
print(list(jobData.columns.array))


print("\n=== Data Reduction ===")
print(f"Number of entries before reduction: {jobData.shape[0]}")
jobData = jobData.loc[jobData["MedianSalary"] > 1000] # remove hourly workers (about 6 jobs overall)

wageGroups = [x for x in jobData.WageGroup.unique() if str(x) != 'nan']


for index, wg in enumerate(wageGroups):
	# Find all jobs that fall into wg
	wgData = jobData[jobData["WageGroup"] == wg]
	wgActual = jobData.loc[jobData["JobName"] == wg] 

	# pick out and calculate data
	# Job Family, Salary and Forecast are the same for all jobs in a group
	jZEntries = [x for x in wgData["JobZone"].tolist() if x > 0] 
	cAEntries = [x for x in wgData["ChanceAuto"].tolist() if x > 0]
	jobZone = -1
	chanceAuto = -1

	if jZEntries:
		jobZone = round(sum(jZEntries)/len(jZEntries)) # should be in [1, 5]

	if cAEntries:
		chanceAuto = round(sum(cAEntries)/len(cAEntries), 1) # float

	if wgActual.empty:
		# row must be created
		wg_soc = wgData["SOCcode"].iloc[0][:-3] + ".99" # unique; SOC code suffixes do not go this high
		# jobname
		wg_jf = wgData["JobFamily"].iloc[0] # copy
		wg_br = all(wgData["isBright"].tolist()) # all jobs in group must be Bright Outlook
		wg_gr = all(wgData["isGreen"].tolist()) # all jobs in group must be Green
		# jobZone
		wg_ms = wgData["MedianSalary"].iloc[0] # copy
		wg_jfore = wgData["JobForecast"].iloc[0] # copy
		# chanceAuto
		# wagegroup
		
		row = [wg_soc, wg, wg_jf, wg_br, wg_gr, jobZone, wg_ms, wg_jfore, chanceAuto, np.nan] # double list to get pd to work
		jobData.loc[-1] = row  # easiest way to actually insert
		jobData.index += 1

	else:
		# existing wageGroups already have a chanceAuto value
		# we only need to update jobzone
		if wgActual["JobZone"].iloc[0] == -1:
			jobData["JobZone"].loc[jobData["JobName"] == wg] = jobZone


jobData = jobData.loc[jobData["WageGroup"].isna()] # remove all jobs that we just summarized
# select all jobs with both a job zone and a chance auto
#jobData = jobData.loc[(jobData["JobZone"] > 0) & (jobData["ChanceAuto"] > 0)].sort_values(["JobZone", "MedianSalary"])
print(f"Number of entries after reduction: {jobData.shape[0]}")


print("\n=== Summary Data ===")
jZHisto = [jobData["JobZone"].tolist().count(x) for x in range(1,6)] # max jobZone = 5
totalJobs = round(sum(jobData["JobForecast"].tolist()) / 1e6, 1)

print(f"Job Zone Counts: {jZHisto}")
print("\n")
print(f"Total Number of Jobs Forecast: {totalJobs} M")
print(f"Average Salary, Non-University: {-1}")
print(f"Average Salary, University: {-1}")
print(f"Average Chance of Automation, Non-University: {-1}")
print(f"Average Chance of Automation, University: {-1}")


print("\n=== Plotting ===")
# === Bubble Chart ===
# The dataframe has over 600 entries, so the bubble chart will be crowded
# X-axis: ChanceAuto
# Y-axis: Salary
# Bubble Size: Jobs Forecast
# Bubble Color: Job Zone

print("\nPlotting Bubble Chart. This will show up in-browser.")

sizeref = max(jobData["JobForecast"])/6000 # scaling factor: larger = smaller bubbles
fig = px.scatter(jobData, x="ChanceAuto", y="MedianSalary", size="JobForecast",
				color="JobZone", hover_name="JobName", log_x=False, size_max=60)

fig.update_traces(mode='markers', marker=dict(sizemode='area',
                                              sizeref=sizeref, line_width=1))
fig.update_layout(
	title="Salary vs Chance of Automation For Selected Jobs (SOC Code)",
		xaxis=dict(
		title="Chance of Automation",
		gridcolor="white",
		gridwidth=2,
	),
	yaxis=dict(
		title="Median Salary",
		gridcolor="white",
		gridwidth=2,
	),
	paper_bgcolor='rgb(200, 200, 200)',
    plot_bgcolor='rgb(200, 200, 200)',
	)
fig.show()

print("\nScript Complete. Press Enter to quit.")
input()
