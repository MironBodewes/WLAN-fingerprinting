import subprocess
results = subprocess.check_output(
    ["netsh", "wlan", "show", "network", "mode=Bssid"])
lines = results.splitlines()
print(len(lines))
for line in lines:
    print(line)
