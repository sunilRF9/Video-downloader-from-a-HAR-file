#! /usr/bin/env python
import re
import argparse
import os
import threading
import requests
import json
from tqdm import tqdm
from urllib.parse import urlparse
import uuid
links=[]
chunk_size = 1024
pattern = ['720p','1080p']
def main(harfile_path):
    harfile = open(harfile_path)
    harfile_json = json.loads(harfile.read())
    i = 0
    for entry in harfile_json['log']['entries']:
        i = i + 1
        url = entry['request']['url']
        mimetype = 'unknown'
        if 'mimeType' in entry['response']['content']:
            mimetype = entry['response']['content']['mimeType']
        if re.search(pattern[0],url):
            links.append(url)
        else:
            pass
    print(f"Chosen resolution : {pattern[0]}")
    print('Links found')
    print("**********************STARTING DOWNLOAD**************************")
    download(links[0])
    print("*****************************DONE********************************")
def download(url):
    r = requests.get(url, stream=True)
    with open (str(uuid.uuid4()) +".mp4", "wb") as f:
        for chunk in tqdm(r.iter_content(chunk_size=chunk_size)):
            f.write(chunk)

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        prog='parsehar',
        description='Parse .har files')
    argparser.add_argument('harfile', type=str, nargs=1,
                        help='path to harfile to be processed.')
    args = argparser.parse_args()
    #main(args.harfile[0])
    t1 = threading.Thread(target=main,args=(args.harfile[0],))
    t1.start()
    t1.join()
