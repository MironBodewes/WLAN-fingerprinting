import pandas as pd
import numpy as np
df=pd.read_csv("aps.csv", sep=";")
df.to_pickle("./data/accesspoints.pkl3")
df.to_csv("aps.csv", sep=";")