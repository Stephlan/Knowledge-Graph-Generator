#-*-coding:utf-8-*- #编码声明，不要忘记！
import requests  #这里使用requests，小脚本用它最合适！
from lxml import html    #这里我们用lxml，也就是xpath的方法
import csv
import random
import time

class Spider:
    def __init__(self):
        self.url = "http://www.baidu.com/"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"}

    def crawl(self, disease, symptom, condition = "互动百科"):
        req = "s?wd=" + disease + "%2C" + symptom + "%20" + condition #A链球菌群感染%2C头痛%20互动百科
        page = requests.get(self.url + req, self.headers)
        print(self.url + req)
        #对获取到的page格式化操作，方便后面用XPath来解析
        tree = html.fromstring(page.text)
        abstract = tree.xpath('//*[@id="1"]/div/div[2]/div[1]//text()')
        return "".join(abstract[1:])

filepath = "../Datasets/disease_symptom.csv"
outpath = "../Datasets/outputs.csv"
errpath = "../Datasets/errputs.csv"
with open(filepath, "r", encoding="utf8") as ds:
    with open(outpath, "a", encoding="utf8") as output:
        with open(errpath, "a", encoding="utf8") as errput:
            reader = csv.reader(ds)
            spider = Spider()
            spliter = "@@@"
            for row in reader:
                ret = spider.crawl(row[0], row[1], "互动百科")
                if(ret == ""):
                    errput.write(row[0] + spliter + row[1] + "\n")
                else:
                    output.write(row[0] + spliter + row[1] + spliter + ret + "\n")
                time.sleep(random.random() * 2)
