
import os
from time import gmtime, strftime

import pandas as pd

num=0
fingerprints_path = "data/accesspoints.pkl"+str(num)
df = pd.read_pickle(fingerprints_path)
df.head()
df.to_csv("aps.csv", sep=";")
#find all location names and change them to the correct ones
print(df["location_name"].unique())
df["location_name"] = df["location_name"].replace("tisch", "küche")
print(df["location_name"].unique())
# DataFrame
# read_csv = pd.read_csv("aps.csv", sep=";")
df.to_csv("aps.csv", sep=";")
df.to_pickle(fingerprints_path)

# if os.path.isfile(fingerprints_path):
#     os.remove(fingerprints_path)
#     df.to_pickle(fingerprints_path)
