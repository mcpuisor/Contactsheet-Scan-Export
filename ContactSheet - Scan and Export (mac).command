#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
  echo "Python is not installed or not in PATH."
  echo "Download Python from https://www.python.org"
  exit 1
fi

# Run the Python script in the same folder as this script
SCRIPT_DIR="$(dirname "$0")"
python3 "$SCRIPT_DIR/bin/Mask_Batch.py"

# Prompt user to press any key before exiting
echo "Press any key to exit..."
read -n 1 -s

# Close the terminal window
osascript -e 'tell application "Terminal" to close (every window whose frontmost is true)' & exit
