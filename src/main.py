import os
import time
import numpy as np
import pandas as pd
from knn import knn_func
# from windows_scan import scan_func
from linux_scan import scan_func
from pathlib import Path

BYTE_N = 78  # N
BYTE_COLON = bytes(":", encoding="utf8")  # 112
CONFIG_PATH = "data/config.csv"
fingerprints_base = "data/accesspoints.pkl" # not a constant
fingerprints_path = fingerprints_base
FID = 'fingerprint_id'
COLUMNS = ['fingerprint',
           'x-pos', 'y-pos', 'ssid', 'bssidd', 'signal_strength', 'frequency_standard', 'location_name']
dataset_id=0
DATASET="dataset"


class Accesspoint:
    def __init__(self, ssid, bssidd, signal_strength, frequency_standard):
        self.ssid = ssid
        self.bssidd = bssidd
        self.signal_strength = signal_strength
        self.frequency_standard = frequency_standard

    def __repr__(self):
        return "ssid="+str(self.ssid)+" bssidd="+str(self.bssidd)+" signal_strength="+str(self.signal_strength)+"\n"

def get_integer_input() -> int:
    user_input = input("Enter an integer to choose the dataset: ")
    try:
        value = int(user_input)
        return value
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
        return None
        
############################
# start of main
if __name__ == "__main__":
    # try reading the config. If it does not exist, initialize with 0
    try:
        config_df = pd.read_csv(CONFIG_PATH)
        # print(type(config_df))
        config_df.head()
        fingerprint_count = config_df.loc[:, FID][0]
        dataset_id=config_df.loc[:,DATASET]
        fingerprints_path=fingerprints_base+str(config_df.loc[:, DATASET][0])
        # print(type(fingerprint_number))
        # print(fingerprint_number)
    except FileNotFoundError:
        # testing sphinx documentation
        print("except in config_reading, FileNotFoundError")
        '''
        "fingerprint_number": the amount of fingerprints that have been made and saved in the accesspoints.csv file
        '''
        fingerprint_count = int(0)
        mylist = []  # I only know how to make a df out of a list # TODO
        mylist.append(0)
        mylist.append(0)
        Path("./data").mkdir(parents=True, exist_ok=True)
        config_df = pd.DataFrame([0,0], columns=[FID,DATASET])
        config_df.to_csv(CONFIG_PATH)
        mylist.clear()


    fingerprints = []
    while (True):
        befehl = input(
            "Welchen Befehl wollen sie ausführen? Try f for fingerprint, l to locate or x for exit or c to choose the dataset you wish to save in... \n")
        if (befehl == "f" or befehl == "fingerprint"):
            # scan the WLAN (do a fingerprint)
            count = input("how many fingerprints do you want to make? ")
            fingerprints = []
            fingerprints.clear()
            for i in range(int(count)):
                fingerprints.extend(scan_func(fingerprint_count, locate=False))
                print("fingerprint:\n", fingerprints)
                fingerprint_count += 1

            # saving
            print("saving fingerprints")
            if os.path.isfile(fingerprints_path):
                df = pd.read_pickle(fingerprints_path)
                df_new = pd.DataFrame(fingerprints, columns=COLUMNS)
                df = pd.concat([df, df_new], axis=0)
            else:
                print(fingerprints_path, "is not a file yet. Creating it now.")
                df = pd.DataFrame(fingerprints, columns=COLUMNS)
            if os.path.isfile(fingerprints_path):
                os.remove(fingerprints_path)
            df.to_pickle(fingerprints_path)
            df.to_csv("aps.csv", sep=";")

            # cleanup
            mylist = []  # I only know how to make a df out of a list # TODO
            mylist.append(fingerprint_count)
            print("fingerprint_number=", fingerprint_count)
            config_df = pd.DataFrame(mylist, columns=[FID])
            config_df.to_csv(CONFIG_PATH)
        elif befehl == "ssss" or befehl == "save":
            # save is deprecated
            print("save is deprecated")
            # print("saving fingerprints")
            # df = pd.DataFrame(fingerprints, columns=COLUMNS)
            # # print(df.head())
            # df.to_pickle(FINGERPRINTS_PATH)
        elif befehl == "l" or befehl == "locate":
            print("locating with fingerprints=", fingerprint_count)
            knn_func(fingerprints_path, fingerprint_count,verbose_level=1)
        elif befehl == "x" or befehl == "exit":
            print("exiting...")
            break
        elif befehl == "r":  # remove
            if os.path.isfile(fingerprints_path):
                os.remove(fingerprints_path)
                os.remove(CONFIG_PATH)
                fingerprint_count = 0
                print("removed the fingerprints")
            else:
                print("fingerprint file not found, can't remove")
        elif befehl == "c" or befehl == "choose save":
            user_input = get_integer_input()
            fingerprints_path = fingerprints_base+str(user_input)
            dataset_id=user_input
            fingerprint_count=0
        elif befehl == "fix": #fix the fingerprint_count in the config (should do this on load tbh)
            mylist = []  # I only know how to make a df out of a list # TODO
            my_df=pd.read_pickle(fingerprints_path)
            print("##################")
            print(my_df.head())
            helper=my_df.loc[:,"fingerprint"]
            fingerprint_count=helper.max()
            config_df = pd.DataFrame(np.array([[fingerprint_count,dataset_id]]), columns=[FID,DATASET])
            config_df.to_csv(CONFIG_PATH)

        else:
            print(
                "Befehl wurde nicht erkannt. Try f for fingerprint, l to locate or x for exit")

    # cleanup
    print("fingerprint_count=", fingerprint_count)
    config_df = pd.DataFrame(np.array([[fingerprint_count,dataset_id]]), columns=[FID,DATASET])
    config_df.to_csv(CONFIG_PATH)

