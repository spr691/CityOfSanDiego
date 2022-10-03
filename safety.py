import pandas as pd
import numpy as np

df_request = pd.read_csv("get_it_done_requests_open_datasd.csv", low_memory=False).dropna(subset=["street_address","zipcode"])

df_collision = pd.read_csv("pd_collisions_datasd_v1.csv", low_memory=False).dropna(subset=["address_road_primary"])
df_collision = df_collision[["report_id", "date_time", "address_road_primary", "address_sfx_primary"]]
df_collision["zip"] = np.nan

for index1, row1 in df_collision.iterrows():
    for index2, row2 in df_request.iterrows():
        if row1["address_road_primary"].lower() in row2["street_address"].lower():
            df_collision.at[index1, "zip"] = row2["zipcode"]
            break

df_collision.dropna(subset=["zip"])

df_collision.to_csv('pd_collisions_zip.csv')
