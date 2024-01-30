import pickle
import subprocess
import re
import numpy as np
import time
import matplotlib.pyplot as plt


class Accesspoint:
    def __init__(self, ssid, bssid, fingerprint_id, signal_strength):
        # could use one list with fingerprint, signal tuples instead of two lists here.
        self.fingerprint_list = [fingerprint_id]
        self.signal_strength_list = [signal_strength]
        self.ssid = ssid
        self.bssid = bssid


WLAN_INTERACE = "wlp4s0"


def get_frequency_band(freq):
    # Define the channel ranges for 2.4 GHz and 5 GHz
    # ranges are too wide here.
    if 2000 <= freq <= 3000:
        return "2.4 GHz"
    elif 5000 <= freq <= 5200:
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
        result = subprocess.check_output(["sudo", "iw", "dev", WLAN_INTERACE, "scan"], universal_newlines=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    # print(result)
    print("after scan", time.time()-start_time, "seconds")
    start_time = time.time()

    # Extract ESSID, BSSID, signal strength, and channel using regular expressions
    essid_list = re.findall(r"SSID: (.*)", result)
    bssid_list = re.findall(r"BSS (\S+)\(", result)
    signal_strength_list = re.findall(r"signal: (-\d+)", result)
    #                                 r'signal: (-\d+) dBm'
    channel_list = re.findall(r"freq: (\d+)", result)
    # print(essid_list, bssid_list, signal_strength_list, channel_list, sep="\n")
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
    # visualizing the scans.
    # plotting and boxplotting
    INDEX_ID = 0  # fingerprint id
    INDEX_SIGNAL = 5
    INDEX_BSSID = 4
    INDEX_ESSID = 3
    fingerprint_list = []
    SCAN = False
    if SCAN == True:
        for i in range(5):
            fingerprint_list.append(scan_func(i))

        # Saving and loading the list so we can restart the program without scanning.
        with open('./saved_dictionary.pkl', 'wb') as f:
            pickle.dump(fingerprint_list, f)

    with open('./saved_dictionary.pkl', 'rb') as f:
        fingerprint_list = pickle.load(f)

    ap_to_signals = {}
    ap_list = list[Accesspoint]()
    for fingerprint in fingerprint_list:
        for ap in fingerprint:
            # new version
            my_ap: Accesspoint = next((x for x in ap_list if x.bssid == ap[INDEX_BSSID]), None)
            if my_ap is None:
                ap_list.append(Accesspoint(ap[INDEX_ESSID], ap[INDEX_BSSID], ap[INDEX_ID], ap[INDEX_SIGNAL]))
            else:
                my_ap.signal_strength_list.append(ap[INDEX_SIGNAL])
                my_ap.fingerprint_list.append(ap[INDEX_ID])
            # old version
            if ap[INDEX_BSSID] not in ap_to_signals:
                ap_to_signals[ap[INDEX_BSSID]] = [ap[INDEX_SIGNAL]]  # list with 1 element. brackets are necessary.
            else:
                ap_to_signals[ap[INDEX_BSSID]].append(ap[INDEX_SIGNAL])
    print(ap_to_signals)

    fig = plt.figure()
    ax = plt.subplot(111)
    for ap in ap_list:
        ax.plot(ap.fingerprint_list, ap.signal_strength_list, label=ap.ssid)
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 1, box.height*0.8])
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3),
            ncol=3, fancybox=True, shadow=True)
    plt.show()
