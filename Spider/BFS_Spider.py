import urllib.request as request
import requests
import csv
import time
import random
from lxml import html

class EnFetcher:
    def __init__(self):
        self.proxies = {
            'https': 'https://127.0.0.1:1080',
            'http': 'http://127.0.0.1:1080'
        }
        self.outpath = "../Datasets/outputsBFS2.csv"
        self.errpath = "../Datasets/errputsBFS.csv"

    def crawl(self):
        opener = request.build_opener(request.ProxyHandler(self.proxies))
        request.install_opener(opener)
        with open(self.outpath, "a", encoding="utf8") as enOutput:
            with open(self.errpath, "a", encoding="utf8") as enErrput:
                toBeAccessed = ["https://zh.wikipedia.org/wiki/Category:医学"]
                for target in toBeAccessed:
                    print(target)
                    try:
                        response = requests.get(target, proxies=self.proxies)
                        tree = html.fromstring(response.text)
                        categories = tree.xpath('//*[@id="mw-subcategories"]//*[@class="CategoryTreeLabel  CategoryTreeLabelNs14 CategoryTreeLabelCategory"]//text()')
                        for category in categories:
                            toBeAccessed.append("https://zh.wikipedia.org/wiki/Category:" + category)
                        pages = tree.xpath('//*[@id="mw-pages"]//*[@class="mw-category-group"]//a//text()')
                        for page in pages:
                            enOutput.write(page + "\n")
                        # enErrput.write(response.text)
                        time.sleep(random.random() * 2)
                    except:
                        enErrput.write(target)

                toBeAccessed.pop(0)

fetcher = EnFetcher()
fetcher.crawl()

