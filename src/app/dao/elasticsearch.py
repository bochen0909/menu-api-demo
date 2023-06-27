import glob
import json
import os
import logging

from elasticsearch import Elasticsearch
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    # Set the log message format
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()  # Output logs to the console
    ]
)

es_ep = [os.environ.get('ES_ENDPOINT', "http://es01:9200")]
logging.info(f"Connecting to {es_ep}")
es = Elasticsearch(es_ep)

logging.info(f"Elasticsearch info: {es.info()}")


def find_customer(customer_id):
    res = es.search(index="restaurants-index",
                    body={"query": {"match": {"id": customer_id}}})
    for hit in res['hits']['hits']:
        doc = hit["_source"]
        ret = doc.copy()
        ret.pop("raw_text")
        return ret

    return None


def find_food_term(term, limit):
    ans = []
    body = {
        "query": {
            "fuzzy": {
                "raw_text": {
                    "value": term,
                    "fuzziness": 2
                }
            }
        },
        "size": limit
    }

    res = es.search(index="restaurants-index", body=body)

    for hit in res['hits']['hits']:
        score = hit['_score']
        docid = hit['_source']['id']
        ans.append({'id': docid, 'score': score})

    return ans
