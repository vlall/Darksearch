import sys
import tika
from tika import parser
import re
from tika import language, translate
import os
import csv
import pandas as pd

class Tikify(object):

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
        metadata = parsed["metadata"]
        #   Return re.sub('[\s+]', '', content)
        #  TODO: Delete... Very Redundant..
        content = parsed["content"]
        content = content.replace('\n', '')
        content = content.replace('\t', '')
        content = content.replace('\'', '')
        content = content.replace('\"', '')
        rx = re.compile('\W+')
        content = rx.sub(' ', content).strip()
        self.content = content
        #   Title...
        try:
            title = metadata['title']
        except:
            title = 'Untitled'
        title = title.replace('\t', '')
        title = title.replace('\t', '')
        title = title.replace('\'', '')
        title = title.replace('\"', '')
        title = rx.sub(' ', title).strip()
        self.title = title
        #  self.type = self.metadata['Content-Type-Hint']
        #  self.name = self.metadata['resourceName']
        #  lanFix = re.sub('[\s+]', '', content)
        self.lang = language.from_file(fileName)

    def toEnglish(self, language='en'):
        self.eng = translate.from_file(self.content.encode('UTF-8'), self.lang, language)

    def analyze(self, translate):
        pass


if __name__ == "__main__":
    dataPath = os.getcwd()+'/../data/'
    logPath = os.getcwd()+'/../logs/scrape.log'
    print 'Started...'
    with open(logPath) as logs:
        print 'Reading csv...'
        logs = pd.read_csv(
                            logs,
                            header=None,
                            sep=',',
                            skipinitialspace=True,
                            names=[
                                    "DATES",
                                    "URLS",
                                    "NAMES",
                                    "SIZE",
                            ]

                )
        #   Columns = [DATE,URL,NAME,SIZE,LANG,CONTENT')]
        #  with open("logs/process.csv", "a") as log:
        #     log.write('DATE,URL,NAME,SIZE,LANG,CONTENT\n')
        for i in range(0, len(logs)): 
            date = str(logs['DATE'][i].strip())
            url = str(logs['URL'][i].strip())
            name = str(logs['NAME'][i].strip())
            size = str(logs['SIZE'][i])
            try:
                output = Tikify(dataPath + name)
                content = unicode(output.content)
                title = str(output.title)
                lang = str(output.lang)
                with open("../logs/process2.csv", "a") as log:
                    log.write(('%s\t%s\t%s\t%s\t%s\t%s\t%s\n') % (date, url, name, size, lang, title, content))
                    print ('Appended line %d...') % i 
            except Exception:
                continue
