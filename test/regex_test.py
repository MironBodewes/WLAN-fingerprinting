import re

input_string = "signal: -79.00 dBm"
match = re.search(r'signal: (-\d+)', input_string)

if match:
    result = match.group(1)
    print(result)