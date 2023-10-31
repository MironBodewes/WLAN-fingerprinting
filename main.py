import os
import time
import numpy as np
import pandas as pd
from winsdk.windows.devices.wifi import WiFiAdapter
from knn import knn_func
from scan import scan_func

BYTE_N = 78  # N
BYTE_COLON = bytes(":", encoding="utf8")  # 112
CONFIG_PATH = "config.csv"
FINGERPRINTS_PATH = "accesspoints.csv"
FID = 'fingerprint_id'


class Accesspoint:
    def __init__(self, ssid, bssidd, signal_strength, frequency_standard):
        self.ssid = ssid
        self.bssidd = bssidd
        self.signal_strength = signal_strength
        self.frequency_standard = frequency_standard

    def __repr__(self):
        return "ssid="+str(self.ssid)+" bssidd="+str(self.bssidd)+" signal_strength="+str(self.signal_strength)+"\n"


############################
# start of main
# try reading the config. If it does not exist, initialize with 0

try:
    config_df = pd.read_csv(CONFIG_PATH)
    # fingerprint_number = config_df.loc[FID]
    # print(type(config_df))
    config_df.head()
    fingerprint_number = config_df.loc[:, FID][0]
    # print(type(fingerprint_number))
    # print(fingerprint_number)
except FileNotFoundError:
    print("except in config_reading")
    fingerprint_number = 0
    mylist = []  # I only know how to make a df out of a list # TODO
    mylist.append(0)
    config_df = pd.DataFrame(mylist, columns=[FID])
    config_df.to_csv(CONFIG_PATH)
    mylist.clear()


fingerprints = []
while (True):
    befehl = input("Welchen Befehl wollen sie ausführen?")
    if (befehl == "f" or befehl == "fingerprint"):
        # scan the WLAN (do a fingerprint)
        count = input("how many fingerprints do you want to make?")
        print(int(count))
        for i in range(int(count)):
            fingerprints.extend(scan_func(fingerprint_number+1))
            # print("fingerprint:\n",fingerprints)
            fingerprint_number += 1
    elif befehl == "s" or befehl == "save":
        print("saving fingerprints")
        df = pd.DataFrame(fingerprints, columns=['fingerprint',
                                                 'x-pos', 'y-pos', 'ssid', 'bssidd', 'signal_strength', 'frequency_standard'])
        # print(df.head())
        df.to_csv(FINGERPRINTS_PATH, mode="a", sep=";")
    elif befehl == "l" or befehl == "locate":
        print("locating with f=", fingerprint_number)
        knn_func(fingerprint_number)
    elif befehl == "x" or befehl == "exit":
        print("exiting...")
        break
    elif befehl == "r":  # remove
        if os.path.isfile(FINGERPRINTS_PATH):
            os.remove(FINGERPRINTS_PATH)
            os.remove(CONFIG_PATH)
            print("removed the fingerprints")
        else:
            print("fingerprint file not found, can't remove")
    else:
        print("Befehl wurde nicht erkannt. Try \\f for fingerprint, \\s for save or \\x for exit")

# cleanup
mylist = []  # I only know how to make a df out of a list # TODO
mylist.append(fingerprint_number)
print("fingerprint_number=", fingerprint_number)
config_df = pd.DataFrame(mylist, columns=[FID])
config_df.to_csv(CONFIG_PATH)
