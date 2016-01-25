import sys
import tika
from tika import parser
import re
from tika import language, translate
import os
import csv
import pandas as pd

'''
- Tor Spiders collect logs and data. 
- Tika, NLP algorithms analyze for pandas/Postgres ingestion
- Query is passed here and outputs key. 
'''

class SearchEngine(object):

	def __init__(self):

		# dataPath = os.getcwd()+'/data/'
		logPath = os.getcwd()+'/logs/process.csv'
		with open(logPath) as logs:
			self.logs = pd.read_csv(logs, header=None, sep='\t')

	def search(self, query):
		# Columns = [DATE,URL,NAME,SIZE,LANG,CONTENT]
		content = self.logs[5]
		matches = self.logs[content.str.contains(query)]
		self.dates = matches[0]
		self.urls = matches[1]
		self.names = matches[2]
		self.size = matches[3]
		self.lang = matches[4]
		self.content = matches[5]

		for i in range(len(matches)):
			print self.content.iloc[[1]].values#Make into string, then do: .decode('unicode-escape')


if __name__ == '__main__':

	test = SearchEngine()
	test.search('claire') 
