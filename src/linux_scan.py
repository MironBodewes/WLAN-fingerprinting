import subprocess
import re
import numpy as np
import time
from my_tshark import my_scan_function


WLAN_INTERACE = "wlp4s0"
 
def get_frequency_band(channel):
    # Define the channel ranges for 2.4 GHz and 5 GHz
    if 1 <= channel <= 14:
        return "2.4 GHz"
    elif 32 <= channel <= 177:
        return "5 GHz"
    else:
        return "Unknown"


def scan_func(fingerprint_number: int, locate=True, debug=False) -> list:
    start_time = time.time()

    # scan the wifi
    if locate == False:
        location_name = input("Where are you? ")
    else:
        location_name = None
    x_coordinate = None
    y_coordinate = None
    # print("before scan",time.time()-start_time); start_time=time.time()

    # changed to iw
    try:
        # Run the iw command to scan for wireless networks
        channel_list, signal_strength_list, bssid_list, essid_list, = my_scan_function()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

    if (debug):
        print(essid_list, bssid_list, signal_strength_list, channel_list, sep="\n")
    # print(len(essid_list),len(bssid_list),len(signal_strength_list),len(channel_list))

    # Print the results including frequency band information
    fingerprint = []
    for essid, bssid, signal_strength, channel in zip(essid_list, bssid_list, signal_strength_list, channel_list):
        frequency_band = get_frequency_band(int(channel))
        # print(f"ESSID: {essid}, BSSID: {bssid}, Signal Strength: {signal_strength} dBm, Frequency Band: {frequency_band}")
        accesspoint = []
        accesspoint.append(fingerprint_number)
        accesspoint.append(x_coordinate)  # x-pos (relative to something...)
        accesspoint.append(y_coordinate)  # y-pos
        accesspoint.append(essid)
        accesspoint.append(bssid)
        accesspoint.append(int(signal_strength))
        accesspoint.append(frequency_band)
        accesspoint.append(location_name)
        fingerprint.append(accesspoint)
    print(len(fingerprint), "accesspoints found")
    # for thing in accesspoint:
    #     print(type(thing),thing)

    # print("end",time.time()-start_time); start_time=time.time()
    return fingerprint


if __name__ == "__main__":
    scan_func(150)
