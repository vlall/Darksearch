#!/usr/bin/python

import os
import pandas as pd
import json
from elasticsearch import Elasticsearch


class DarkElastic(object):
    """
    Take a DataFrame and turn it into an ElasticSearch Index.
    Need to delete an index?
    curl -XDELETE 'http://localhost:9200/your_index/'
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
        self.size = len(searchIndex.index)
        searchIndex = searchIndex.to_json(orient='index')
        searchIndex = json.loads(searchIndex)
        self.searchIndex = searchIndex

    def save_json(self, dataframe):
        with open("../logs/process.json", "w") as outfile:
            json.dump(dataframe, outfile, indent=4)
        print ('Dataframe converted to JSON.')

    def ingest_items(self):
        for i in range(0, self.size):
            doc = self.searchIndex[str(i)]
            res = es.index(index="dark", doc_type='html', id=i, body = doc)
            print('Ingested document %d...' % i)
        return (res['created'])

    #  curl -XGET 'http://localhost:9200/your_index/doc_type/id'
    def get_items(self, i):
        res = es.get(index="dark", doc_type='html', id=i)
        return (res['_source'])

    def search_index(self, myIndex, myQuery):
        res = es.search(index=myIndex, body={'query': {'match': {'CONTENT':myQuery}}})
        hitList = ("Got %d Hits:" % res['hits']['total'])
        for hit in res['hits']['hits']:
            print("%(DATES)s: %(URLS)s" % hit['_source'])
        return hitList


if __name__ == '__main__':
    es = Elasticsearch()
    test = DarkElastic()
    ## Turn DataFrame into JSON
    # test.save_json(test.searchIndex)
    ## Build your index.
    #  test.ingest_items()
    es.indices.refresh(index='dark')
    print test.search_index('dark','look')
