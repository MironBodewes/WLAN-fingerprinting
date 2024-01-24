import subprocess
import re
import numpy as np


def get_frequency_band(channel):
    # Define the channel ranges for 2.4 GHz and 5 GHz
    if 1 <= channel <= 14:
        return "2.4 GHz"
    elif 36 <= channel <= 165:
        return "5 GHz"
    else:
        return "Unknown"


def scan_func(fingerprint_number: int, locate=False, debug=False) -> list:
    # scan the wifi
    if locate == False:
        location_name = input("Where are you? ")
    else:
        location_name = None
    x_coordinate = None
    y_coordinate = None

    try:
        # Run the iwlist command to scan for wireless networks
        result = subprocess.check_output(["sudo", "iwlist", "wlp4s0", "scan"], universal_newlines=True)

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

    # Extract BSSID, signal strength, and channel using regular expressions
    essid_list = re.findall(r"ESSID:\"(.*?)\"", result)
    bssid_list = re.findall(r"Address: (\S+)", result)
    signal_strength_list = re.findall(r"Signal level=(-\d+)", result)
    channel_list = map(int, re.findall(r"Channel:(\d+)", result))

    # Print the results including frequency band information
    fingerprint = []
    for essid, bssid, signal_strength, channel in zip(essid_list, bssid_list, signal_strength_list, channel_list):
        frequency_band = get_frequency_band(channel)
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
    # print(len(fingerprint),"accesspoints found")
    for thing in accesspoint:
        print(type(thing),thing)
    return fingerprint


if __name__ == "__main__":
    scan_func(150)
