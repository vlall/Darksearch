#!/usr/bin/python

import subprocess
from time import sleep
import requests

process = subprocess.Popen("python dark_server.py", shell=True)
print('Darksearch started.')
sleep(5)
darkRequest = requests.get('http://0.0.0.0')
darkRequest.raise_for_status()
process.kill()
print('Darksearch killed.')
