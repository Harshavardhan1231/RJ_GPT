import subprocess
import time
# Define the command to run your app.py
command = r'app_env\python.exe app.py'

# Use subprocess.run to execute the command
result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
