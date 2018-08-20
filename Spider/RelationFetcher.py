import json
import time
import requests
from requests.adapters import HTTPAdapter
import urllib.request as request
import requests
import csv
import time
import random
import scrapy

class EnFetcher:
	def __init__(self):
		self.proxies = {
			'https': 'https://127.0.0.1:1080',
			'http': 'http://127.0.0.1:1080'
		}
		self.filepath = "../Datasets/enList.csv"
		self.outpath = "../Datasets/relationResultOut.csv"
		self.errpath = "../Datasets/errputsEn.csv"
		print("Initialization")
		content = self.crawl()
		for i in content:
			print(i.meta)

	def crawl(self):
		print("Here")
		opener = request.build_opener(request.ProxyHandler(self.proxies))
		request.install_opener(opener)
		relationName = dict()
		with open("../Datasets/relationResult.json", "r", encoding="utf-8") as fr:
			for line in fr.readlines():
				relationJson = json.loads(line)
				relation = relationJson['rmention']
				relationName[relation] = relationJson['chrmention']

		count = 0 
		with open("../Datasets/readytoCrawl.json","r", encoding="utf-8") as fr:
			with open(self.outpath, "w") as outfile:
				for line in fr.readlines():
					count += 1 
					print(1.0*count/33355)
					entityJson  = json.loads(line)
					link = "https:"+entityJson['entity']['url']
					entityName = entityJson['entityOriginName']
					entity = scrapy.Request(link,callback=self.parseEntity)
					entity.meta['entityName'] = entityName
					entity.meta['link'] = link
					yield entity

	def parseEntity(self, response, entityName):
		print("=======================")
		entity1 = entityName
		entityRelation = dict()
		headers = {
			"user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
			"accept-language" : "zh-CN,zh;q=0.9,en;q=0.8",
			"keep_alive" : "False"
		}
		for section in response.xpath('//h2[contains(@class,"wb-section-heading")]//span/text()'):
			title = section.extract()
			flag =  0
			if(title == "Statements"):
				flag = 1 
				for statement in response.xpath('.//div[@class="wikibase-statementgroupview"]'):
					relationItem = statement.xpath('.//div[@class="wikibase-statementlistview"]')
					relationName = statement.xpath('.//div[contains(@class,"wikibase-statementgroupview-property-label")]//a[contains(@title,"P")]/text()').extract()
					if(len(relationName)>0):
						relationName = relationName[0]
					else:
						continue
					for relatedEntity in relationItem.xpath('.//div[contains(@class,"wikibase-statementview-mainsnak")]//div[contains(@class,"wikibase-statementview-mainsnak")]\
						//div[contains(@class,"wikibase-snakview-value-container")]//div[contains(@class,"wikibase-snakview-body")]\
						//div[contains(@class,"wikibase-snakview-value")]//a[contains(@title,"Q")]'):
							entityId = relatedEntity.xpath('./@title').extract()
							if(len(entityId) == 0):
								continue
							else:
								relatedEntityId = entityId[0]							 
								httpRequest = requests.session()
								httpRequest.mount('https://', HTTPAdapter(max_retries=30)) 
								httpRequest.mount('http://',HTTPAdapter(max_retries=30))
								url = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids="+relatedEntityId+"&format=json"
								relatedEntityJson = httpRequest.get(url,headers=headers).json()
								httpRequest.close()
								entity2 = str()
								if 'zh' in relatedEntityJson['entities'][relatedEntityId]['labels']:
									entity2 = relatedEntityJson['entities'][relatedEntityId]['labels']['zh']['value']
								elif 'en' in relatedEntityJson['entities'][relatedEntityId]['labels']:
									entity2 = relatedEntityJson['entities'][relatedEntityId]['labels']['en']['value']
								else:
									continue
								entityRelation['entity1'] = entity1
								entityRelation['relation'] = relationName 
								entityRelation['entity2'] = entity2
								yield entityRelation
			if(flag):
				break

fetcher = EnFetcher()