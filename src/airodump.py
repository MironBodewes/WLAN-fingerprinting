

import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time
from time import gmtime, strftime

if not os.geteuid() == 0:
    sys.exit('Script must be run as root.')

WLAN_INTERFACE = "wlp4s0"
WLAN_INTERFACEMON = WLAN_INTERFACE+"mon"
FILTER = ""
modes = "i f k y"
FILEPATHRAW = "./airdumps/scan"
ENDING = ".pcapng"

# TODO rename


def my_scan_function():
    datetime = strftime("%Y-%m-%d_%H:%M:%S", gmtime())
    filepath = FILEPATHRAW+datetime+"_"
    radio_channel_list = []
    signal_strength_list = []
    bssid_list = []
    essid_list = []

    # os.system("sudo airmon-ng check kill 1> /dev/null")
    # ahhhhhhhhhhhhh
    os.system("nmcli device set " + WLAN_INTERFACE+" managed no")
    directory_path = Path.cwd() / "data/airdumps"
    Path(directory_path).mkdir(parents=True, exist_ok=True)
    try:
        os.system("sudo airmon-ng start " + WLAN_INTERFACE + " 1> /dev/null")
    except:
        pass
    filename = "data/airdumps/"+datetime
    cmd = "sudo airodump-ng -f 1600 -w " + filename + " --channel 1,3,6,9,11 --output-format csv --write-interval 2 "+WLAN_INTERFACEMON
    try:
        p = subprocess.Popen(cmd, shell=True, start_new_session=True)
        p.wait(timeout=20)
    except subprocess.TimeoutExpired:
        print('Terminating the whole process group...', file=sys.stderr)
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)

    os.system("sudo airmon-ng stop wlp4s0mon 1> /dev/null")
    # analyse output
    # Extract ESSID, BSSID, signal strength, and channel
    import csv
    filename = filename+"-01.csv"
    lines = 0
    with open(filename, "r") as f:
        text = f.readlines()

        # if a line is empty, break
        count = 0
        for i in range(len(text)):
            lines += 1
            if len(text[i]) <= 10:
                count += 1
            if count == 2:
                break
    # print("lines:", lines)

    import pandas as pd
    df = pd.read_csv(filename, nrows=lines-3)
    print(df.columns)
    essid_list = df[' ESSID'].tolist()
    bssid_list = df['BSSID'].tolist()
    signal_strength_list = df[' Power'].tolist()
    channel_list = df[' channel'].tolist()

    # print(essid_list, bssid_list, signal_strength_list, channel_list, sep="\n")
    # print(len(essid_list), len(bssid_list), len(signal_strength_list), len(channel_list))
    # if (essid == "<MISSING>"):
    #     pass
    # else:
    #     essid = bytearray.fromhex(essid).decode()

    # stopping:
    os.system("sudo airmon-ng stop wlp4s0mon 1> /dev/null")
    # TODO enable NetworkManager
    # os.system("systemctl start NetworkManager")
    return radio_channel_list, signal_strength_list, bssid_list, essid_list


# debug by starting this file isolated
if __name__ == "__main__":
    my_scan_function()
