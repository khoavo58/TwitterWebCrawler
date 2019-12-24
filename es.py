import json, requests
from elasticsearch import Elasticsearch

es = Elasticsearch()
f = open("tweet.json")
tweet = f.read().split('\n')
es.indices.delete(index = "twitter", ignore = [400, 404])
for i in range(len(tweet) - 1):
    res = es.index(index = "twitter", doc_type = 'tweet', id = i + 1, body = tweet[i])
print(res)









