import subprocess
import os

# Define the paths to your first and second Python scripts
script1 = "api_testing.py"  # Replace with the actual path to your YOLOv8 script
script2 = "object_detection.py"  # Replace with the actual path to your voice recognition script

# Function to open a new terminal and run a script
def open_new_terminal(script_path):
    # Using `start` to open a new terminal window in Windows
    subprocess.Popen(['start', 'cmd', '/k', f'python {script_path}'], shell=True)

# Start both scripts in separate terminal windows
open_new_terminal(script1)
open_new_terminal(script2)

print("Both scripts are now running in separate terminals.")
