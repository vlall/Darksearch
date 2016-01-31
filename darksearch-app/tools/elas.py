#!/usr/bin/python

import os
import pandas as pd
import json
from elasticsearch import Elasticsearch
import requests

class DarkElastic(object):

    def __init__(self):
        """
        Load JSON.
        """
        self.jsonPath = os.getcwd()+"/../logs/process.json"
        with open(self.jsonPath) as searchIndex:
            searchIndex = json.load(searchIndex)
        self.size = len(searchIndex.keys())
        self.searchIndex = searchIndex

    def pandas_to_json(self):
        """
        Take logFile, open as Dataframe, covert to JSON, Save JSON.
        """
        self.logPath = os.getcwd()+'/../logs/process.csv'
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
                                                "CONTENT"
                                        ]
                            )
        self.size = len(searchIndex.index)
        searchIndex = searchIndex.to_json(orient='index')
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

    def search_index(self, myIndex, myQuery, start, end):
        stopFilter = ['a', 'an', 'the'] 
        res = es.search(
                        index=myIndex,
                        body={
                                "from": start,
                                "size": end,
                                'query' : {
                                            "query_string" : {
                                            "default_field" : "CONTENT",
                                            "query" : myQuery
                                            }
                                },
                                "sort" : {
                                            "_score" : {
                                            "order" : "desc"
                                    }
                                },
                        }
        )
        hitList = ("Got %d Hits:" % res['hits']['total'])
        for hit in res['hits']['hits']:
            print("%(DATES)s: %(URLS)s" % hit['_source'])
        return hitList
    
    def delete_deuplicates(self, i):
        pass

    def delete_all(self, index='dark,'):
        """
        Runs $ curl -XDELETE 'http://localhost:9200/your_index/'
        """
        r = requests.delete('http://localhost:9200/%s' % (index))
        print('Index %s deleted.' % index)

if __name__ == '__main__':
    es = Elasticsearch()
    test = DarkElastic()
    ###  Build your index.
    #  test.ingest_items()
    es.indices.refresh(index='dark')
    print test.search_index('dark', 'yes', 0, 10)
