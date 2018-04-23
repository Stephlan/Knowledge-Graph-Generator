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
        self.filepath = "../Datasets/enList.csv"
        self.outpath = "../Datasets/outputsEn.csv"
        self.errpath = "../Datasets/errputsEn.csv"

    def crawl(self, entityList, outfile):
        opener = request.build_opener(request.ProxyHandler(self.proxies))
        request.install_opener(opener)
        entityList = ["糖尿病"]
        with open(self.filepath, "r", encoding="utf8") as enInput:
            with open(self.outpath, "a", encoding="utf8") as enOutput:
                with open(self.errpath, "a", encoding="utf8") as enErrput:
                    reader = csv.reader(enInput)
                    for row in reader:
                        entity = row[0]
                        url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=" + entity + "&language=zh&format=json"
                        response = requests.get(url, proxies=self.proxies)
                        enOutput.write(response.text)
                        # enErrput.write(response.text)
                        time.sleep(random.random() * 2)

