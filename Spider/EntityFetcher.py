import urllib.request as request
import requests
import csv
import time
import random

class EnFetcher:
    def __init__(self):
        self.proxies = {
            'https': 'https://127.0.0.1:1080',
            'http': 'http://127.0.0.1:1080'
        }
        self.filepath = "../Datasets/TrainSetUnique.csv"
        self.outpath = "../Datasets/EnWiki.json"
        self.errpath = "../Datasets/errWiki.csv"
        self.visited = []

    def crawl(self):
        opener = request.build_opener(request.ProxyHandler(self.proxies))
        request.install_opener(opener)
        with open(self.filepath, "r", encoding="utf8") as enInput:
            with open(self.outpath, "a", encoding="utf8") as enOutput:
                with open(self.errpath, "a", encoding="utf8") as enErrput:
                    reader = csv.reader(enInput)
                    for row in reader:
                        entity = row[0]
                        self.visited.append(entity)
                        url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=" + entity + "&language=zh&format=json"
                        response = requests.get(url, proxies=self.proxies)
                        enOutput.write(response.text + '\n')
                        # enErrput.write(response.text)
                        time.sleep(random.random() * 2)
                        entity = row[1]
                        self.visited.append(entity)
                        url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=" + entity + "&language=zh&format=json"
                        response = requests.get(url, proxies=self.proxies)
                        enOutput.write(response.text + '\n')

fetcher = EnFetcher()
fetcher.crawl()

