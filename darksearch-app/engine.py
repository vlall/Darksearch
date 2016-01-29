#!/usr/bin/python

import sys
import tika
from tika import parser
import re
from tika import language, translate
import os
import csv
import pandas as pd


#  csv.field_size_limit(sys.maxsize)


class SearchEngine(object):
    """
    - First, Tor Spiders collect information in /logs and /data.
    - Then, Tika, NLP algorithms analyze for pandas/pgres ingestion.
    - The query is then passed here and output to search results.
    """
    def __init__(self):
        logPath = os.getcwd()+'/logs/process.csv'
        with open(logPath) as logs:
            self.logs = pd.read_csv(
                                    logs,
                                    header=None,
                                    sep='\t',
                                    names=[
                                            "DATES",
                                            "URLS",
                                            "NAMES",
                                            "SIZE",
                                            "LANG",
                                            "CONTENT"
                                    ]
            )
            self.logs.dropna(how='any', inplace=True)

    def search(self, query):
        """
        Parse a pandas data structure for searchability
        """
        self.query = query.lower()
        #  TODO: Fix how to make query not exactly match the searched content
        content = self.logs['CONTENT']
        matches = self.logs[content.str.lower().str.contains(query.lower())]
        self.dates = matches['DATES']
        self.urls = matches['URLS']
        self.names = matches['NAMES']
        self.size = matches['SIZE']
        self.lang = matches['LANG']
        self.content = matches['CONTENT']
        self.contentList = self.content.tolist()
        self.briefList = []
        for i in self.contentList:
            description = i[0:200]  # Take first 200 words
            description = re.sub(' +', ' ', description)  # Subtract spaces
            self.briefList.append(description)


if __name__ == '__main__':
    test = SearchEngine()
    test.search('test')
    results = test.contentList
    for i in test.briefList:
        print i
        print '---------'
    print len(test.briefList)
