import subprocess
import re
import numpy as np
import time
from my_tshark import my_scan_function


WLAN_INTERACE = "wlp4s0"


class Accesspoint:
    def __init__(self, fingerprint_number, location_name, bssid, essid, signal_strength: int, frequency_band, signals_recorded: int = 1, x_coordinate=None, y_coordinate=None):
        self.fingerprint_number = fingerprint_number
        self.location_name = location_name
        self.bssid = bssid
        self.essid = essid
        self.signal_strength = signal_strength
        self.frequency_band = frequency_band
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.signals_recorded = signals_recorded

    def __repr__(self):
        return "essid="+str(self.essid)+" bssid="+str(self.bssid)+" signal_strength="+str(self.signal_strength)+"\n"

# TODO channel input is ambigious, 6GHz networks also use channel numbers 1-14 so the frequency as input is more accurate


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
    my_accesspoints = []
    # map: bssid -> object with the bssid
    bssid_object_map = dict()

    for essid, bssid, signal_strength, channel in zip(essid_list, bssid_list, signal_strength_list, channel_list):
        signal_strength = int(signal_strength)
        frequency_band = get_frequency_band(int(channel))
        # print(f"ESSID: {essid}, BSSID: {bssid}, Signal Strength: {signal_strength} dBm, Frequency Band: {frequency_band}")

        # using classes instead of lists
        # problem is that one bssid will now have possibly multiple signal strengths because we are recording more than one beacon frame per ap now.
        # so we have to gather all the signal_strenghts per bssid and get the mean and stddev
        my_accesspoint = Accesspoint(fingerprint_number=fingerprint_number, location_name=location_name,
                                     bssid=bssid, essid=essid, signal_strength=signal_strength, frequency_band=frequency_band, x_coordinate=x_coordinate, y_coordinate=y_coordinate)
        if (bssid not in bssid_object_map):
            my_accesspoints.append(my_accesspoint)  # TODO I hope this just puts the reference in the list
            bssid_object_map[bssid] = my_accesspoint
        else:
            ap_to_change: Accesspoint = bssid_object_map[bssid]
            # print(ap_to_change.signal_strength, ap_to_change.signals_recorded, my_accesspoint.signal_strength)
            ap_to_change.signal_strength = (ap_to_change.signal_strength*ap_to_change.signals_recorded +
                                            my_accesspoint.signal_strength)/(ap_to_change.signals_recorded+1)
            ap_to_change.signals_recorded+=1
            # print("new=", ap_to_change.signal_strength)
    
    #converting from classes to a lists
    for k, v in bssid_object_map.items():
        accesspoint = []
        accesspoint.append(v.fingerprint_number)
        accesspoint.append(v.x_coordinate)  # x-pos (relative to something...)
        accesspoint.append(v.y_coordinate)  # y-pos
        accesspoint.append(v.essid)
        accesspoint.append(v.bssid)
        accesspoint.append(v.signal_strength)
        accesspoint.append(v.frequency_band)
        accesspoint.append(location_name)
        fingerprint.append(accesspoint)



    print(len(fingerprint), "accesspoints found")
    for ap in my_accesspoints:

        continue
        # for thing in accesspoint:
        #     print(type(thing),thing)

        # print("end",time.time()-start_time); start_time=time.time()
    return fingerprint


if __name__ == "__main__":
    scan_func(150)
