import re
import subprocess
import json


class Accesspoint:
    def __init__(self, ssid, bssidd, signal_strength):
        self.SSID = ssid
        self.BSSIDD = bssidd
        self.signal_strength = signal_strength

    def __repr__(self):
        return "ssid="+str(ssid)+" bssidd="+str(bssidd)+" signal_strength="+str(signal_strength)+"\n"


results = subprocess.check_output(
    ["netsh", "wlan", "show", "network", "mode=Bssid"])
lines = results.splitlines()

accesspoints = []
# for i in range(len(lines)):
i = 0
BYTE_N = 78  # N
BYTE_COLON = bytes(":", encoding="utf8")  # 112

ssid = 3
bssidd = 4
signal_strength = 5
byte_N = bytes("N", encoding="utf8")
bssi_found = 0
print(len(lines))
while (i < len(lines)):
    print(lines[i])
    if re.search(bytes("SSID ", encoding="utf8"), lines[i]):
        ssid = lines[i].split(bytes(":", encoding="utf8"))[1][1:]
        if (lines[i+1][4] != BYTE_N):  # useless debug line
            raise Exception("should always be Netzwerk in the line after ssid")
        i += 4
        try:
            match = re.search(bytes("BSSIDD", encoding="utf8"), lines[i])
        except:
            print("nothing")
        while (match):
            bssi_found += 1
            bssidd = lines[i][-17:]  # magic
            signal_strength = lines[i+1][-5:-3]
            print("rssi=", signal_strength)
            accesspoints.append(Accesspoint(ssid, bssidd, signal_strength))
            i += 6
            match = re.search(bytes("BSSIDD", encoding="utf8"), lines[i])
    i += 1


print("bssi_found=", bssi_found)
print(accesspoints)
