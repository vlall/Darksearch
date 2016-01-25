#!/usr/bin/python

import sys
import re
import os
import csv
import pandas as pd


class SearchEngine(object):
    """
    First, Tor Spiders collect information in /logs and /data.
    Then, Tika, NLP algorithms analyze for pandas/pgres ingestion.
    The query is then passed here and output to search results.
    """

    def __init__(self):
        logPath = os.getcwd()+'/logs/process.csv'
        with open(logPath) as logs:
            self.logs = pd.read_csv(logs, header=None, sep='\t')

    def search(self, query):
        """
        Parse a pandas data structure for searchability.
        """
        self.query = query
        content = self.logs[5]
        matches = self.logs[content.str.contains(query)]
        # Columns = [DATE,URL,NAME,SIZE,LANG,CONTENT]
        self.dates = matches[0]
        self.urls = matches[1]
        self.names = matches[2]
        self.size = matches[3]
        self.lang = matches[4]
        self.content = matches[5]
        self.contentList = self.content.tolist()
        self.brief = self.get_brief2(query, self.contentList[0], 10)


if __name__ == '__main__':
    test = SearchEngine()
    test.search('test')
