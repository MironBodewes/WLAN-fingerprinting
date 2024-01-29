import re

input_string = "BSS c0:25:06:0d:4b:7d(on wlp4s0)"
match = re.search(r"BSS (\S+)\(", input_string)

if match:
    result = match.group(1)
    print(result)