import pandas as pd
import numpy as np
# df=pd.read_csv("aps.csv", sep=";")
# df.to_pickle("./data/accesspoints.pkl3")
# df.to_csv("aps.csv", sep=";")
# from time import gmtime, strftime
# datetime=strftime("%Y-%m-%d_%H:%M:%S", gmtime())
# print(datetime)

mylist=[[1,2]]
print(mylist)
print("DEBUG:dataset=",0,"\nfingerprint_number=", 0)
config_df = pd.DataFrame(mylist, columns=["FID", "DATASET"])
config_df.to_csv("data/config_test.csv")