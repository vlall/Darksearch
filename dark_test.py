#!/usr/bin/python

import subprocess
from time import sleep
import requests

process = subprocess.Popen("sudo gunicorn --bind 0.0.0.0:80 dark_server", shell=True)
print('Darksearch started.')
sleep(5)
#  Check maine search screen
darkRequest = requests.get('http://0.0.0.0')
darkRequest.raise_for_status()
#  Check cached pages get displayed
process.kill()
print('Darksearch is running in the background...')
