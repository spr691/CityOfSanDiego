import pandas as pd
import matplotlib.pyplot as mp

#Create basic visualizations

df_complete = pd.read_csv("transportation_report.csv", low_memory=False)

# Closed Requests By Zipcode
df_complete = df_complete.sort_values(['total_closed_requests'], ascending=False)
df_complete.plot(x="zipcode", y=["total_closed_requests"], kind="bar", figsize=(10, 9))
mp.xlabel("Zipcode")
mp.ylabel("Number of Reports")
mp.title("Number of Closed Requests By Zipcode")
mp.show()

# Number of Open Requests By Zipcode
df_complete = df_complete.sort_values(['total_open_requests'], ascending=False)
df_complete.plot(x="zipcode", y=["total_open_requests"], kind="bar", figsize=(10, 9))
mp.xlabel("Zipcode")
mp.ylabel("Number of Reports")
mp.title("Number of Open Requests By Zipcode")
mp.show()

# Median Income By Zipcode
df_complete = df_complete.sort_values(['median_income'], ascending=False)
df_complete.plot(x="zipcode", y=["median_income"], kind="bar", figsize=(10, 9))
mp.xlabel("Zipcode")
mp.ylabel("Median Income")
mp.title("Median Income By Zipcode")
mp.show()

# Collision Reports By Zipcode
df_complete = df_complete.sort_values(['total_collision_reports'], ascending=False)
df_complete.plot(x="zipcode", y=["total_collision_reports"], kind="bar", figsize=(10, 9))
mp.xlabel("Zipcode")
mp.ylabel("Total Collision Reports")
mp.title("Collision Reports By Zipcode")
mp.show()

# Closed Requests by Collision Reports
df_complete = df_complete.sort_values(['total_closed_requests'], ascending=False)
mp.xticks(df_complete["closed_rank"], df_complete["zipcode"], rotation='vertical')
mp.plot(df_complete["closed_rank"], df_complete["total_closed_requests"], label="Total Closed Get It Done Requests")
mp.plot(df_complete["closed_rank"], df_complete["total_collision_reports"], label="Total Collision Reports")
mp.xlabel("Zipcode")
mp.ylabel("Number of Records")
mp.title("Closed Get It Done Requests and Collision Reports Vs Zipcodes")
mp.legend()
mp.show()

# Open Requests by Collision Reports
df_complete = df_complete.sort_values(['total_open_requests'], ascending=False)
mp.xticks(df_complete["open_rank"], df_complete["zipcode"], rotation='vertical')
mp.plot(df_complete["open_rank"], df_complete["total_open_requests"], label="Total Open Get It Done Requests")
mp.plot(df_complete["open_rank"], df_complete["total_collision_reports"], label="Total Collision Reports")
mp.xlabel("Zipcode")
mp.ylabel("Number of Records")
mp.title("Open Get It Done Requests and Collision Reports Vs Zipcodes")
mp.legend()
mp.show()

# Closed Requests by Median Income
df_complete = df_complete.sort_values(['total_closed_requests'], ascending=False)
df_complete["median_income"] = df_complete["median_income"]/100
mp.xticks(df_complete["closed_rank"], df_complete["zipcode"], rotation='vertical')
mp.plot(df_complete["closed_rank"], df_complete["total_closed_requests"], label="Total Closed Get It Done Requests")
mp.plot(df_complete["closed_rank"], df_complete["median_income"], label=" Median Income (Hundreds of Dollars")
mp.xlabel("Zipcode")
mp.ylabel("Units")
mp.title("Closed Get It Done Requests and Median Income Vs Zipcodes")
mp.legend()
mp.show()

# Open Requests by Median Income
df_complete = df_complete.sort_values(['total_open_requests'], ascending=False)
df_complete["median_income"] = df_complete["median_income"]/100
mp.xticks(df_complete["open_rank"], df_complete["zipcode"], rotation='vertical')
mp.plot(df_complete["open_rank"], df_complete["total_open_requests"], label="Total Open Get It Done Requests")
mp.plot(df_complete["open_rank"], df_complete["median_income"], label=" Median Income (Hundreds of Dollars")
mp.xlabel("Zipcode")
mp.ylabel("Units")
mp.title("Open Get It Done Requests and Median Income Vs Zipcodes")
mp.legend()
mp.show()

# Avg Case Age by Median Income
df_complete = df_complete.sort_values(['avg_case_age_days'], ascending=False)
df_complete["median_income"] = df_complete["median_income"]/1000
mp.xticks(df_complete["case_age_rank"], df_complete["zipcode"], rotation='vertical')
mp.plot(df_complete["case_age_rank"], df_complete["avg_case_age_days"], label="Avg Case Age (Days)")
mp.plot(df_complete["case_age_rank"], df_complete["median_income"], label=" Median Income (Thousands of Dollars)")
mp.xlabel("Zipcode")
mp.ylabel("Units")
mp.title("Avg Case Age and Median Income Vs Zipcodes")
mp.legend()
mp.show()
