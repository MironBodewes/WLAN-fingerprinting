import os

os.system("sudo airmon-ng stop wlp4s0mon 1> /dev/null")
os.system("nmcli device set wlp4s0 managed yes")
