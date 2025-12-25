import os
from pathlib import Path
import subprocess
import time
from time import gmtime, strftime


CHANNELS = 13
WLAN_INTERFACE = "wlp4s0"
WLAN_INTERFACEMON = WLAN_INTERFACE+"mon"
FILTER = ""
modes = "i f k y"
FILEPATHRAW = "./airdumps/scan"
ENDING = ".pcapng"

# TODO rename


def my_scan_function():
    datetime = strftime("%Y-%m-%d_%H:%M:%S", gmtime())
    filepath=FILEPATHRAW+datetime+"_"
    radio_channel_list = []
    signal_strength_list = []
    bssid_list = []
    essid_list = []

    # os.system("sudo airmon-ng check kill 1> /dev/null")
    # ahhhhhhhhhhhhh
    os.system("nmcli device set " + WLAN_INTERFACE+" managed no")
    Path("./airdumps").mkdir(parents=True, exist_ok=True)
    os.system("sudo airmon-ng start " + WLAN_INTERFACE + " 1> /dev/null")
    for index in range(1, CHANNELS+1):
        os.system("sudo airmon-ng start "+WLAN_INTERFACEMON+" " + str(index) + " 1> /dev/null")
        os.system("tshark -i " + WLAN_INTERFACEMON + " -w " + filepath+str(index)+ENDING + " -a duration:1.6 2> /dev/null")

    # analyse output
    for index in range(1, CHANNELS+1):
        os.system("tshark -r "+filepath+str(index)+str(ENDING) +
                  " -Y wlan.fc.type_subtype==8 -T fields -e wlan_radio.channel -e wlan_radio.signal_dbm  -e wlan.bssid -e wlan.ssid > channel"+str(index)+".txt")

        text = open("channel"+str(index)+".txt")
        # Extract ESSID, BSSID, signal strength, and channel
        for line in text:
            # print(line)
            parts = line.split()
            radio_channel = parts[0]
            signal_strength = parts[1]
            bssid = parts[2]
            essid = parts[3]
            if (essid == "<MISSING>"):
                # print("das war hier schon")
                # essid=None
                # essid="MISSING"
                continue
            else:
                essid = bytearray.fromhex(essid).decode()
            radio_channel_list.append(radio_channel)
            signal_strength_list.append(signal_strength)
            bssid_list.append(bssid)
            essid_list.append(essid)
        # print("len(essid_list)=",len(essid_list))

    # stopping:
    os.system("sudo airmon-ng stop wlp4s0mon 1> /dev/null")
    # TODO enable NetworkManager
    # os.system("systemctl start NetworkManager")
    return radio_channel_list, signal_strength_list, bssid_list, essid_list


# debug by starting this file isolated
if __name__ == "__main__":
    my_scan_function()
