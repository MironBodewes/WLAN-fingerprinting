import os

os.system("nmcli device set wlp4s0 managed no")
os.system("sudo airmon-ng start wlp4s0 1> /dev/null")
