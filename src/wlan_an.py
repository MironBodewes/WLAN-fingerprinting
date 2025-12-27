from pathlib import Path
import os

os.system("sudo airmon-ng stop wlp4s0mon 1> /dev/null")
os.system("nmcli device set wlp4s0 managed yes")


# Construct the path to the directory to make
directory_path = Path.cwd() / "documents/test"

# Make the directory by calling mkdir() on the path instance
directory_path.mkdir()

# Report the result
print(f"Successfully made the '{directory_path}' directory.")
