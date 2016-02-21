#!/usr/bin/python

import os
import signal
import subprocess
from time import sleep
import requests

process = subprocess.Popen("python dark_server.py", shell=True)
print ('Darksearch started.')
sleep(10)
darkRequest = requests.get('http://0.0.0.0')
darkRequest.raise_for_status()
os.killpg(os.getpgid(process.pid), signal.SIGTERM)
print ('Darksearch killed.')
