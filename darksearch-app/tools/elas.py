#!/usr/bin/python

import os
import pandas as pd
import json
from elasticsearch import Elasticsearch
es = Elasticsearch()



class DarkElastic(object):
    """
    Take a DataFrame and turn it into an Elastic Search Index. 
    """


    def __init__(self):
        logPath = os.getcwd()+'/../logs/process.csv'
        with open(logPath) as logs:
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
        searchIndex = searchIndex.to_json(orient='index')
        searchIndex = json.loads(searchIndex)
        doc = searchIndex['0']
        self.doc = doc

        ##  Ingest...
        #  res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
        #  print(res['created'])

        ##  Get it...
        #  res = es.get(index="test-index", doc_type='tweet', id=1)
        #  print(res['_source'])

        ##  Refresh
        es.indices.refresh(index="test-index")

        ##  Elastic Search
        res = es.search(index="test-index", body={"query": {"match": {'CONTENT':'BTC'}}})
        print("Got %d Hits:" % res['hits']['total'])
        for hit in res['hits']['hits']:
            print("%(DATES)s: %(URLS)s" % hit["_source"])  


if __name__ == '__main__':
    test = DarkElastic()