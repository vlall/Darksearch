#!/usr/bin/python

import os
import pandas as pd
import json
from elasticsearch import Elasticsearch
import requests
import re
es = Elasticsearch()

class DarkElastic(object):

    def __init__(self):
        self.size = 0

    def pandas_to_json(self, jsonPath):
        """
        Take logFile, open as Dataframe, covert to JSON, Save JSON.
        """
        self.jsonPath = jsonPath
        self.logPath = os.getcwd()+'/../logs/process2.csv'
        with open(self.logPath) as logs:
            searchIndex = pd.read_csv(
                                        logs,
                                        header=None,
                                        sep='\t',
                                        names=[
                                                "DATES",
                                                "URLS",
                                                "NAMES",
                                                "SIZE",
                                                "LANG",
                                                "TITLE",
                                                "CONTENT"
                                        ]
                            )
        self.size = len(searchIndex.index)
        searchIndex = searchIndex.to_json(orient='index')
        #  If you want to use a JSON file rather than converting
        #  with open(self.jsonPath) as searchIndex:
        searchIndex = json.loads(searchIndex)
        self.searchIndex = searchIndex
        self.save_json(searchIndex)

    def save_json(self, dataframe):
        with open(self.jsonPath, "w") as outfile:
            json.dump(dataframe, outfile, indent=4)
        print('Dataframe converted to JSON.')

    def ingest_items(self):
        for i in range(0, self.size):
            doc = self.searchIndex[str(i)]
            res = es.index(
                            index="dark",
                            doc_type='html',
                            id=i,
                            body=doc
                )
            print('Ingested document %d...' % i)
        return (res['created'])

    def get_items(self, i):
        res = es.get(
                        index="dark",
                        doc_type='html',
                        id=i
                )
        return (res['_source'])

    def search_index(self, myIndex, myQuery, start=0, end=10):
        res = es.search(
                        index=myIndex,
                        body={
                                "from": start,
                                "size": end,
                                'query': {
                                            "query_string": {
                                                "default_field": "CONTENT",
                                                "query": myQuery
                                            }
                                },
                                "sort": {
                                            "_score": {
                                                        "order": "desc"
                                            }
                                }
                        }
        )
        self.briefList = []
        self.namesList = []
        self.datesList = []
        self.titleList = []
        hitList = ("Got %d Hits:" % res['hits']['total'])
        for hit in res['hits']['hits']:
            print("%(DATES)s: %(URLS)s" % hit['_source'])
            content = hit['_source']['CONTENT']
            names = hit['_source']['NAMES']
            dates = hit['_source']['DATES']
            title = hit['_source']['TITLE']
            brief = self.get_brief(myQuery, content, 20)
            self.briefList.append(brief)
            self.namesList.append(names)
            self.datesList.append(dates)
            self.titleList.append(title)
            self.size = res['hits']['total']
        return hitList

    def delete_deuplicates(self, i):
        pass

    def delete_all(self, index='dark'):
        """
        Runs $ curl -XDELETE 'http://localhost:9200/your_index/'
        """
        r = requests.delete('http://localhost:9200/%s' % (index))
        print('Index %s deleted.' % index)

    def get_brief(self, query, content, n):
        """
        Obtain the brief description that shows up in search
        """
        query = query.lower()
	#  Strips quotes
	query = query.replace('\"', "")
	queryList = query.split()
        queryList.sort(key=len)
        content = content.lower().split()
        try:
            pos = content.index(query)
        except ValueError:
            pos = 0
        if ((pos - n) < 0):
            start = 0
            end = pos + n + abs((pos - n))
        else:
            start = pos - n
            end = pos + n
        #  Find Nearest period to end sentence...
        #  try:
        #      endSentence = content.index(".")
        #      if endSentence < (start+40):
        #          end = endSentence
        #  except:
        #     pass
        content = content[start:end]
        if len(content) >= 500:
            content = content[0:400]
        for query in queryList:
            wrap = '<font color=\'yellow\'><b>'+query+'</b></font>'
            try:
                content[content.index(query)] = wrap
            except:
                pass
        brief = " ".join(content)
        return brief

    def runSetup(self, jsonPath):
        self.pandas_to_json(jsonPath)
        self.save_json(self.searchIndex)

    def check_cat(self, description):
        return 'tor'

    def free_mem(self):
        del self.briefList
        del self.namesList
        del self.datesList
        del self.titleList

if __name__ == '__main__':
    test = DarkElastic()
    test.runSetup("../logs/process2.json")
    #  Build your index.
    test.ingest_items()
    es.indices.refresh(index='dark')
    print test.search_index('dark', 'cocaine', 15, 10)
