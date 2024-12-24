import os
from pathlib import Path
import subprocess

WLAN_INTERACE = "wlp4s0"
WLAN_INTERACEMON = WLAN_INTERACE+"mon"
print(WLAN_INTERACEMON)
FILTER = ""
modes = "i f k y"
FILEPATH = "./airdumps/scan-DATUM-ZEIT"
ENDING = ".pcapng"

os.system("sudo airmon-ng check kill")
Path("./airdumps").mkdir(parents=True, exist_ok=True)
subprocess.run(["sudo", "airmon-ng", "start", WLAN_INTERACE])
for index in range(1, 14):
    subprocess.run(["sudo", "airmon-ng", "start", WLAN_INTERACEMON, str(index)])
    # subprocess.run(["sudo", "airmon-ng","-h"])
    subprocess.run(["tshark", "-i", WLAN_INTERACEMON, "-w", FILEPATH+str(index)+ENDING, "-a" "duration:1"])
    # analysieren in python
for index in range(1, 14):
    stream=os.popen("tshark -r "+FILEPATH+str(index)+ENDING+" -Y wlan.fc.type_subtype==8 -T fields -e wlan.ssid -e wlan.bssid -e wlan_radio.signal_dbm")
    output=stream.read()
    # output.splitlines()
    for line in stream:
        
# stopping:
os.system("sudo airmon-ng stop wlp4s0mon")
os.system("systemctl start NetworkManager")
