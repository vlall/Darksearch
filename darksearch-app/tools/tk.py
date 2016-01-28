import sys
import tika
from tika import parser
import re
from tika import language, translate
import os
import csv
import pandas as pd

class Tikify:

	'''
	DataBase Ingestion Script
	- You have Data in html files in '/data'
	- You have 'logs/scrape.log with the time scraped, size.
	- Create table in Postgres with 
	- Date, .onion, name(.html), tikify(text), size, language, type, title, sentiment, etc
	- 
	'''

	def __init__(self, fileName):
		parsed = parser.from_file(fileName)
		self.metadata = parsed["metadata"]
		content = parsed["content"]
		#   Return re.sub('[\s+]', '', content)
		content = content.replace('\n', '')
		#  TODO: Delete... Very Redundant..
		self.content = content.replace('\t', '')
		self.content = content.replace('\'', '')
		self.content = content.replace('\"', '')
		rx = re.compile('\W+')
		self.content = rx.sub(' ', self.content).strip()
		#  self.title = self.metadata['title']
		#  self.type = self.metadata['Content-Type-Hint']
		#  self.name = self.metadata['resourceName']
		#  lanFix = re.sub('[\s+]', '', content)
		self.lang = language.from_file(fileName)

	def toEnglish(self, language='en'):
		self.eng = translate.from_file(self.content.encode('UTF-8'), self.lang, language)

	def analyze(self, translate):
		pass


if __name__ == "__main__":
	dataPath = os.getcwd()+'/data/'
	logPath = os.getcwd()+'/logs/scrape.log'
	print 'Started...'
	with open(logPath) as logs:
		print 'Reading csv...'
		logs = pd.read_csv(logs)
		#   Columns = [DATE,URL,NAME,SIZE,LANG,CONTENT')]
		#  with open("logs/process.csv", "a") as log:
		#	  log.write('DATE,URL,NAME,SIZE,LANG,CONTENT\n')
		for i in range(0, len(logs)): 
			date = str(logs['DATE'][i].strip())
			url = str(logs['URL'][i].strip())
			name = str(logs['NAME'][i].strip())
			size = str(logs['SIZE'][i])
			try:
				output = Tikify(dataPath + name)
				content = str(output.content.encode('UTF-8'))
				lang = str(output.lang)
				print ('Appended line %d...') % i 
				with open("logs/process.csv", "a") as log:
					log.write(('%s\t%s\t%s\t%s\t%s\t%s\n') % (date, url, name, size, lang, content))     
			except Exception:
				continue
