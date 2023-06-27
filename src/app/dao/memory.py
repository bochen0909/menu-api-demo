import glob
import json
import os
import logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s [%(levelname)s] %(message)s",  # Set the log message format
    handlers=[
        logging.StreamHandler()  # Output logs to the console
    ]
)
from bs4 import BeautifulSoup

data_folder = os.getenv("DATA_HOME")
if not data_folder:
    logging.error("$DATA_HOME must be set to use memory data store.")

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


data = {d['id']: d for d in [read_json_file(path) for path in json_files]}


def find_customer(customer_id):
    if customer_id in data:
        obj = data[customer_id]
        ret = obj.copy()
        ret.pop("raw_text")
        return ret
    else:
        return None


def find_food_term(term, limit):
    ans = []
    for k, d in data.items():
        if term in d['raw_text']:
            ans.append(k)
    return ans[:limit]
