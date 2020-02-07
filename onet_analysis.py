#onet_analysis

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import onet_helper

pd.set_option('display.max_rows', 100)

print("="*17 + " O*NET Dataviz " + "="*17)
pre_message = """
Step 2: Analysis

This step analyzes job data from an existing file. In particular:
1. Jobs which have the same "WageGroup" value are grouped into a single entry. If there is
  a given value missing from this entry, use the average of all sub-entries (rounding as necessary).
2. Entries which do not have both a value for 'Job Zone' and 'Chance of Automation' are removed.
3. Relevant summary values are found.

This will also produce a plot, which will appear in a browser window.
"""
print(pre_message)

print("Loading data from file...")
jobData = pd.read_csv('jobData.csv')
print("Columns:")
print(list(jobData.columns.array))


print("\n=== Data Reduction ===")
print(f"Number of entries before reduction: {jobData.shape[0]}")
#jobData = jobData.loc[jobData["MedianSalary"] > 1000] # remove hourly workers (about 6 jobs overall)

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
		wg_soc = wgData["SOCcode"].iloc[0]
		wg_soc = wg_soc[:-3] + ".99" # unique; SOC code suffixes do not go this high
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
			jobData.loc[jobData["JobName"] == wg, "JobZone"] = jobZone

# remove all jobs that were just grouped up
jobData = jobData.loc[jobData["WageGroup"].isna()] 
# select all jobs with both a job zone and a chanceAuto
# jobData = jobData.loc[(jobData["JobZone"] > 0) & (jobData["ChanceAuto"] > 0)]
print(f"Number of entries after reduction: {jobData.shape[0]}")


print("\n=== Summary Data ===")
totalJobs = round(sum(jobData["JobForecast"].tolist()) / 1e6, 1)

jobData_Uni = jobData[jobData["JobZone"] > 3]
jobData_NonUni = jobData[jobData["JobZone"] <= 3]
# not weighted by no of jobs

avgSal_Uni = round(jobData_Uni["MedianSalary"].mean())
avgSal_NonUni = round(jobData_NonUni["MedianSalary"].mean())

jobData_Uni = jobData_Uni[jobData_Uni["ChanceAuto"] > 0] # only include jobs that have this value
jobData_NonUni = jobData_NonUni[jobData_NonUni["ChanceAuto"] > 0]
chanceAuto_Uni = round(jobData_Uni["ChanceAuto"].mean())
chanceAuto_NonUni = round(jobData_NonUni["ChanceAuto"].mean())


print("Job Zone Counts:")
print(jobData["JobZone"].value_counts())
print("\nJob Family Counts:")
print(jobData["JobFamily"].value_counts())
print(f"\nTotal Number of Jobs Forecast: {totalJobs} M")

print("\nData Below determined by number of job titles, not number of jobs.")
print(f"Average Salary, Non-University (USD): {avgSal_NonUni}")
print(f"Average Salary, University (USD): {avgSal_Uni}")
print(f"Average Chance of Automation, Non-University (%): {chanceAuto_NonUni}")
print(f"Average Chance of Automation, University (%): {chanceAuto_Uni}")


print("\n=== Plotting ===")
# === Bubble Chart ===
# The dataframe has hundreds of entries, so the bubble chart will be crowded
# X-axis: ChanceAuto
# Y-axis: Salary
# Bubble Size: Jobs Forecast
# Bubble Color: Job Zone

# scaling factor: larger = smaller bubbles. This formula is recommended within the plotly docs.
sizeref = 2. * max(jobData["JobForecast"])/(100 ** 2)
sizemin = 2.

# force the color-scale to be discrete
for index, row in jobData.iterrows():
	jobData.loc[index, "JobZone"] = str(jobData.loc[index, "JobZone"])

# sort so that as many bubbles as possible can be shown
jobData = jobData[(jobData["JobForecast"] > 2000) | (jobData["MedianSalary"] > 50000)].sort_values("JobForecast", ascending=False)
print(f"Number of entries plotted: {jobData.shape[0]}")
print("Plotting Bubble Chart. This will show up in-browser.")

fig = px.scatter(jobData, x="ChanceAuto", y="MedianSalary", size="JobForecast",
				color="JobZone", hover_name="JobName", log_x=False, size_max=60)

fig.update_traces(mode='markers', marker=dict(sizemode='area',
        sizeref=sizeref, sizemin=sizemin, line_width=1))

fig.update_layout(
	title="Salary vs Chance of Automation For Selected Jobs (SOC Code) (Bubble Size indicates 10-yr Forecasted Job Openings)",
		xaxis=dict(
		title="Chance of Automation (%)",
		gridcolor="white",
		gridwidth=2,
	),
	yaxis=dict(
		title="Median Salary (USD)",
		gridcolor="white",
		gridwidth=2,
	),
	paper_bgcolor='rgb(170, 170, 170)',
    plot_bgcolor='rgb(170, 170, 170)',
	)

fig.show()

onet_helper.exitMsg()
