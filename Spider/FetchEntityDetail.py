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
        self.filepath = "../Datasets/AfterSorted.csv"
        self.outpath = "../Datasets/outputsEn.csv"
        self.errpath = "../Datasets/errputsEn.csv"

    def crawl(self):
        opener = request.build_opener(request.ProxyHandler(self.proxies))
        request.install_opener(opener)
        with open(self.filepath, "r", encoding="utf8") as enInput:
            with open(self.outpath, "a", encoding="utf8") as enOutput:
                with open(self.errpath, "a", encoding="utf8") as enErrput:
                    for row in enInput:
                        row = row.replace("\n", "")
                        entity = row
                        url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=" + entity + "&language=zh&format=json"
                        print(url)
                        try:
                            response = requests.get(url, proxies=self.proxies)
                            enOutput.write(response.text + "\n")
                        except:
                            enErrput.write(url)
                        time.sleep(random.random() * 2)

fetcher = EnFetcher()
fetcher.crawl()
