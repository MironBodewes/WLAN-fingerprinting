import re
import subprocess
import time
from winsdk.windows.devices.wifi import WiFiAdapter

BYTE_N = 78  # N
BYTE_COLON = bytes(":", encoding="utf8")  # 112
CONFIG_PATH = "config.csv"
FINGERPRINTS_PATH = "accesspoints.csv"


class Accesspoint:
    def __init__(self, ssid, bssidd, signal_strength, frequency_standard):
        self.ssid = ssid
        self.bssidd = bssidd
        self.signal_strength = signal_strength
        self.frequency_standard = frequency_standard

    def __repr__(self):
        return "ssid="+str(self.ssid)+" bssidd="+str(self.bssidd)+" signal_strength="+str(self.signal_strength)+"\n"

###
# this method does a few things.
# first it tells Windows to do a wlan scan. It also asks the user for coordinates of the fingerprint
# then it calls netsh and finds the network ssid, bssidd, signal strength
#   and the frequency standard (usually 802.11n or 802.11ac which stand for 2.4 GHz and 5 Ghz respectively)
# @params locate, False -> a fingerprint is being made, True -> the function is used to find the current position (position is unknown)
#


def scan_func(fingerprint_number: int, locate=False, debug=False) -> list:
    WiFiAdapter.request_access_async()
    x_coordinate=None
    y_coordinate=None
    if locate == False:
        x_coordinate = input("x-Koordinate?")
        y_coordinate = input("y-Koordinate?")
    wifi_adapter = WiFiAdapter.find_all_adapters_async()
    while (True):  # TODO
        if (wifi_adapter.status == True):
            #print("myWifi=", wifi_adapter.id, wifi_adapter.status)
            wifi_adapter = wifi_adapter.get_results()[0]
            break
    async_obj = WiFiAdapter.scan_async(wifi_adapter)
    while (async_obj.status == False):  # TODO
        time.sleep(0.001)
        
    # reading the available networks
    results = subprocess.check_output(
        ["netsh", "wlan", "show", "network", "mode=Bssid"])
    # TODO try | findstr /I /R "SSID | signal"
    lines = results.splitlines()
    accesspoints = []
    i = 0
    ssid = -1
    bssidd = -1
    signal_strength = -1
    bssi_found = 0
    # for line in lines:
    #     print(line)
    if (debug):
        print(len(lines))
    while (i < len(lines)):
        if (debug):
            print(lines[i])
        if re.search(bytes("SSID ", encoding="utf8"), lines[i]):
            ssid = lines[i].split(bytes(":", encoding="utf8"))[1][1:]
            if (lines[i+1][4] != BYTE_N):  # useless debug block
                raise Exception(
                    "should always be <Netzwerk> in the line after ssid")
            i += 4
        try:
            match = re.search(bytes("BSSIDD", encoding="utf8"), lines[i])
        except:
            print("nothing")
        if (match):
            bssi_found += 1
            bssidd = str(lines[i][-17:])  # magic
            signal_strength = int(lines[i+1][-5:-3])
            frequency_standard = str(lines[i+2][-8:])
            accesspoints.append(Accesspoint(
                ssid, bssidd, signal_strength, frequency_standard))
        i += 1
    print("bssids_found=", bssi_found)

    fingerprint = []

    for ap in accesspoints:
        accesspoint = []
        accesspoint.append(fingerprint_number)
        accesspoint.append(x_coordinate)  # x-pos (relative to something...)
        accesspoint.append(y_coordinate)  # y-pos
        accesspoint.append(ap.ssid)
        accesspoint.append(ap.bssidd)
        accesspoint.append(ap.signal_strength)
        accesspoint.append(ap.frequency_standard)
        fingerprint.append(accesspoint)
    return fingerprint
