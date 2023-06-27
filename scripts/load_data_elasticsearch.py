#!/usr/bin/env python3
import glob
import json
from elasticsearch import Elasticsearch, helpers
from bs4 import BeautifulSoup
import sys
import logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    # Set the log message format
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()  # Output logs to the console
    ]
)

def process_folder(data_folder, url):
    json_files = glob.glob(f"{data_folder}/**/*.json", recursive=True)

    logging.info(f"Loadding {len(json_files)} files from '{data_folder}'.")

    def read_json_file(filepath):
        with open(filepath) as fil:
            obj = json.load(fil)
        html = obj['raw_text']
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.body.get_text(separator=' ')
        obj['raw_text'] = text
        return obj

    docs = [read_json_file(path) for path in json_files]
    endpoints = url.split(",")
    es = Elasticsearch(endpoints)
    if not es.ping():
        print(es.info())
        raise ValueError("Connection failed")
    actions = [
        {
            "_index": "restaurants-index",
            "_id": doc['id'],
            "_source": doc,
        }
        for i, doc in enumerate(docs, 1)
    ]

    helpers.bulk(es, actions)


if __name__ == '__main__':
    if len(sys.argv) not in [2, 3]:
        print(f"Usage: python {sys.argv[0]} <data folder> [elasticsearch url]")
    else:
        folder_path = sys.argv[1]
        url = "http://es01:9200" if len(sys.argv) == 2 else sys.argv[2]
        process_folder(folder_path, url)
