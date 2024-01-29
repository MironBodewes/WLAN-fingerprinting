import os

PATH="data/aps.csv"
with open( PATH)as file:
    print(os.path.abspath(PATH))
