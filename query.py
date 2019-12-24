import requests
import json
from elasticsearch import Elasticsearch

def search(term):
    es = Elasticsearch()
    res = es.search(index="twitter", doc_type="tweet", body={"query": {"match": {"text": term}}})
    result = []
    i = 1
    for doc in res['hits']['hits']:
        if i > 10:
            break
        result.append(str(i) + ") score: " + str(doc['_score']) + " tweet: " 
                      + str(doc['_source']['text']) + ' ' + str(doc['_source']['created_at']))
        i += 1
    return result

if __name__ == "__main__":
    search("dog")

