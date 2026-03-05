
import os
from time import gmtime, strftime

import pandas as pd
num1 = 0
num2 = 2

fingerprints_path = "data/accesspoints.pkl"+str(num1)
fingerprints_path2 = "data/accesspoints.pkl"+str(num2)


def change_labels():
    df = pd.read_pickle(fingerprints_path)
    df.head()
    df.to_csv("aps.csv", sep=";")
    # find all location names and change them to the correct ones
    print(df["location_name"].unique())
    df["location_name"] = df["location_name"].replace("tijjsch", "küche")
    df2 = pd.read_pickle(fingerprints_path2)

    # for each location_name in df 2, have the order be the same as in df
    df2 = df2.sort_values(by=["location_name"])
    df2.to_pickle(fingerprints_path2)
    print(df2["location_name"].unique())
    # DataFrame
    # read_csv = pd.read_csv("aps.csv", sep=";")
    df.to_csv("aps.csv", sep=";")
    df.to_pickle(fingerprints_path)


    # if os.path.isfile(fingerprints_path):
    #     os.remove(fingerprints_path)
    #     df.to_pickle(fingerprints_path)
# change_labels()
def sort_labels():
    df = pd.read_pickle(fingerprints_path)
    df2 = pd.read_pickle(fingerprints_path2)

    # sort df and df2 by location_name
    df = df.sort_values(by=["location_name"])
    df.to_pickle(fingerprints_path)
    df2 = df2.sort_values(by=["location_name"])
    df2.to_pickle(fingerprints_path2)

sort_labels()
df = pd.read_pickle(fingerprints_path)
print(df["location_name"].unique())
df.to_csv("aps.csv", sep=";")
df2 = pd.read_pickle(fingerprints_path2)
print(df2["location_name"].unique())
df2.to_csv("aps2.csv", sep=";")

