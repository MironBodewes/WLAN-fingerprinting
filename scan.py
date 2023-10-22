import re
import subprocess
import json
import numpy as np
import pandas as pd

BYTE_N = 78  # N
BYTE_COLON = bytes(":", encoding="utf8")  # 112


class Accesspoint:
    def __init__(self, ssid, bssidd, signal_strength):
        self.ssid = ssid
        self.bssidd = bssidd
        self.signal_strength = signal_strength

    def __repr__(self):
        return "ssid="+str(self.ssid)+" bssidd="+str(self.bssidd)+" signal_strength="+str(self.signal_strength)+"\n"


def scan():
    accesspoints = []
    i = 0
    ssid = -1
    bssidd = -1
    signal_strength = -1
    byte_N = bytes("N", encoding="utf8")
    bssi_found = 0
    print(len(lines))
    while (i < len(lines)):
        print(lines[i])
        if re.search(bytes("SSID ", encoding="utf8"), lines[i]):
            ssid = lines[i].split(bytes(":", encoding="utf8"))[1][1:]
            if (lines[i+1][4] != BYTE_N):  # useless debug line
                raise Exception(
                    "should always be <Netzwerk> in the line after ssid")
            i += 4
        try:
            match = re.search(bytes("BSSIDD", encoding="utf8"), lines[i])
        except:
            print("nothing")
        if (match):
            bssi_found += 1
            bssidd = lines[i][-17:]  # magic
            signal_strength = lines[i+1][-5:-3]
            print("rssi=", signal_strength)
            accesspoints.append(Accesspoint(ssid, bssidd, signal_strength))
        i += 1


### start of main
    print("bssi_found=", bssi_found)
    print(accesspoints)
    list_of_lists = []

    # with open("config.txt", "r+", encoding="utf8"):
    fingerprint_number = 0

    fingerprint_number += 1
    for ap in accesspoints:
        # print("hi")
        mylist = []
        mylist.append(fingerprint_number)
        mylist.append(5)  # x-pos (relative to something...)
        mylist.append(5)  # y-pos
        mylist.append(ap.ssid)
        mylist.append(ap.bssidd)
        mylist.append(ap.signal_strength)
        list_of_lists.append(mylist)
    print(list_of_lists)


# try reading the config. If it does not exist initialize with 0
try:
    config_df = pd.read_csv("config.csv")
    fingerprint_number = config_df.loc["fingerprint_id"]
    +1
    config_df.to_csv("config.csv")
except:
    mylist = []
    mylist.append(0)
    config_df = pd.DataFrame(mylist, columns=['fingerprint_id'])
    config_df.to_csv("config.csv")
    mylist.clear()

results = subprocess.check_output(
    ["netsh", "wlan", "show", "network", "mode=Bssid"])
lines = results.splitlines()
while (True):
    befehl = input("Welchen Befehl wollen sie ausführen?")
    if (befehl == "f" or befehl == "fingerprint"):
        scan()  # scan the WLAN (do a fingerprint)
    if befehl == "s" or befehl == "save":
        df = pd.DataFrame(list_of_lists, columns=['fingerprint',
                                                  'x-pos', 'y-pos', 'ssid', 'bssidd', 'signal_strength'])
        print(df.head())
        df.to_csv("accesspoints.csv")
