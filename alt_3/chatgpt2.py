import subprocess
import re

def get_wifi_signal_strength():
    try:
        # Run the netsh command to get information about available wireless networks
        result = subprocess.run(["netsh", "wlan", "show", "network", "mode=Bssid"], capture_output=True, errors="replace", timeout=10)

        # Check if the command was successful
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, result.args, result.stdout, result.stderr)

        # Extract information for each wireless network using a regular expression with German keywords
        print(result.stdout)
        network_info_matches = re.finditer(r"SSID (\d+) : (.*?)\r?\n(?:.*\r?\n)?.*?Authentifizierung\s*:\s*(.*?)\r?\n.*?sselung\s*:\s*(.*?)\r?\n", result.stdout)

        network_strengths = [(match.group(2), match.group(1)) for match in network_info_matches]

        return network_strengths

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None
    except subprocess.TimeoutExpired as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
network_strengths = get_wifi_signal_strength()

if network_strengths is not None and network_strengths:
    for ssid, strength in network_strengths:
        print(f"WiFi Network: {ssid}, Signal Strength: {strength} dBm")
else:
    print("Unable to retrieve WiFi signal strengths.")
