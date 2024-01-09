import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

FINGERPRINTS_PATH="data/config.csv"

df:pd.DataFrame = pd.read_pickle(FINGERPRINTS_PATH)
df.head()
df.drop("")