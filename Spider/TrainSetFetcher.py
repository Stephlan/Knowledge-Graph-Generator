import urllib.request as request
import requests
import csv
import time
import random
import json
from lxml import html
from langconv import *

class TrainsetFetcher:
    def __init__(self):
        self.proxies = {
            'https': 'https://127.0.0.1:1080',
            'http': 'http://127.0.0.1:1080'
        }
        self.filepath = "../Datasets/entityRelation.json"
        self.outpath = "../Datasets/outTrain.csv"
        self.errpath = "../Datasets/errTrain.csv"

    def crawl(self):
        opener = request.build_opener(request.ProxyHandler(self.proxies))
        request.install_opener(opener)
        with open(self.filepath, "r", encoding="utf8") as trainInput:
            with open(self.outpath, "a", encoding="utf8") as trainOutput:
                with open(self.errpath, "a", encoding="utf8") as trainErrput:
                    data = json.load(trainInput)
                    cnt = 0
                    for row in data:
                        cnt += 1
                        entity1 = Converter('zh-hans').convert(row['entity1'])
                        entity2 = Converter('zh-hans').convert(row['entity2'])
                        url = "https://www.google.com.hk/search?q=" + entity1 + "+" + entity2
                        print(url)
                        try:
                            response = requests.get(url, proxies=self.proxies)
                            tree = html.fromstring(response.text)
                            abstract = tree.xpath('//*[@id="ires"]/ol/div[1]/div/span//text()')
                            abstract = ''.join(abstract)
                            abstract = Converter('zh-hans').convert(abstract)
                            abstract = abstract.replace('\n', '')
                            if entity1 not in abstract or entity2 not in abstract:
                                if entity1 not in abstract and entity2 not in abstract:
                                    trainErrput.write(url)
                                print("Lack")
                            else:
                                # trainOutput.write(response.text)
                                trainOutput.write("\"" + entity1 + "\",\""+ entity2 + "\",\"" + abstract + "\"\n")
                        except:
                            print("Err")
                            trainErrput.write(url)
                        time.sleep(random.random() * 2)
                        if cnt % 101 == 0:
                            time.sleep(10 * random.random())

fetcher = TrainsetFetcher()
fetcher.crawl()
