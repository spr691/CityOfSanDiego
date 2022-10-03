import pandas as pd
import glob

# Read Get It Done Requests
df_dict = []
filenames = glob.glob("get_it_done_requests*.csv")
for f in filenames:
    df = pd.read_csv(f, low_memory=False)
    df_dict.append(df)
df = pd.concat(df_dict)

# Filter for tickets related to streetlight repair
df_lights = df.loc[(df["service_name"] == "Street Light Maintenance")]
print("Total Street Light Tickets: ", df_lights.shape[0])

# Select Columns that are important to this study
df_lights = df_lights[["service_request_id", "case_age_days", "service_name", "status", "zipcode", "comm_plan_name"]]
df_lights = df_lights.dropna().astype({"service_request_id": int, "case_age_days": int, "service_name": str,
                              "zipcode": int, "comm_plan_name": str})

# Filter for open requests
df_open = df_lights.loc[df_lights["status"].isin(["In Process", "New"])]

# Filter for closed requests
df_closed = df_lights.loc[df_lights["status"].isin(["Closed", "Referred"])]

# Tabulate past service requests by zip
df_closed_count = df_closed.groupby(["zipcode"])["zipcode"] \
                            .count()\
                            .reset_index(name='total_closed_requests') \
                            .sort_values(['total_closed_requests'], ascending=False)
df_closed_count['closed_rank'] = df_closed_count['total_closed_requests'].rank(method='dense', ascending=False)
df_closed_count = df_closed_count.astype({"closed_rank": int})

# Tabulate open service requests by zip
df_open_count = df_open.groupby(["zipcode"])["zipcode"] \
                            .count()\
                            .reset_index(name='total_open_requests') \
                            .sort_values(['total_open_requests'], ascending=False)
df_open_count['open_rank'] = df_open_count['total_open_requests'].rank(method='dense', ascending=False)
df_open_count = df_open_count.astype({"open_rank": int})

# Select Unique Zipcodes
SD_ZIPCODES = df_lights.zipcode.unique()

#Read Median Incomes from US Census Bureau
df_median = pd.read_csv("ACSST5Y2020.S1903-Data.csv", low_memory=False) \
                .iloc[1:-1 , :] \
                [["NAME", "S1903_C03_001E"]]
df_median.rename(columns={"NAME": "zipcode", "S1903_C03_001E": "median_income"}, inplace=True)
df_median = df_median[df_median["median_income"] != '-']
df_median["zipcode"] = df_median["zipcode"].str.replace(r"ZCTA5 ", "")
df_median["median_income"] = df_median["median_income"].str.replace(r"+", "")\
                                                    .str.replace(r",", "")\
                                                    .str.replace(r"-", "")
df_median = df_median.dropna().astype({"zipcode": int, "median_income": int})
df_median = df_median.loc[df_median["zipcode"].isin(SD_ZIPCODES)]
df_median['median_income_rank'] = df_median['median_income'].rank(method='dense', ascending=False)
df_median = df_median.astype({"median_income_rank": int})

# Calculate Avg Work Time  past service requests by zip
df_case_age = df_closed.groupby(["zipcode"])["case_age_days"] \
                            .mean()\
                            .reset_index(name='avg_case_age_days') \
                            .sort_values(['avg_case_age_days'], ascending=False)
df_case_age['case_age_rank'] = df_case_age['avg_case_age_days'].rank(method='dense', ascending=False)

#Read collision data thats been augmented with zipcode
df_collision = pd.read_csv("pd_collisions_zip.csv", low_memory=False)
df_collision.rename(columns={"zip": "zipcode"}, inplace=True)
df_collision = df_collision.dropna(subset=["zipcode"]).astype({"zipcode": int})
df_collision = df_collision.groupby(["zipcode"])["zipcode"] \
                            .count()\
                            .reset_index(name='total_collision_reports') \
                            .sort_values(['total_collision_reports'], ascending=False)
df_collision['collision_rank'] = df_collision['total_collision_reports'].rank(method='dense', ascending=False)
df_collision = df_collision.astype({"collision_rank": int})

# Join dataframes so we can get a complete picture for each zipcode
df_complete = pd.merge(df_closed_count, df_open_count, on="zipcode")
df_complete = pd.merge(df_complete, df_median, on="zipcode")
df_complete = pd.merge(df_complete, df_collision, on='zipcode')
df_complete = pd.merge(df_complete, df_case_age, on='zipcode')

# Write out report to csv
df_complete.to_csv('transportation_report.csv')
