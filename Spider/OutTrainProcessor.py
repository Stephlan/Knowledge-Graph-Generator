import csv
import json
from langconv import *

jsonpath = "../Datasets/entityRelation.json"
csvpath = "../Datasets/outTrain.csv"
outpath = "../Datasets/TrainSet.csv"
relationOut = "../Datasets/RelationSet.csv"

with open(jsonpath, "r", encoding="utf8") as jsonInput:
    with open(csvpath, "r", encoding="utf8") as csvInput:
        with open(relationOut, "w", encoding="utf8") as output:
            data = json.load(jsonInput)
            reader = csv.reader(csvInput)
            cnt = 0
            relStorage = {}
            # jsonStorage = {}
            for row in data:
                if row['relation'] not in relStorage:
                    relStorage[row['relation']] = 1
                else:
                    relStorage[row['relation']] += 1

            for key in relStorage:
                if relStorage[key] > 200:
                    output.write(key + '\n')
                # entity1 = Converter('zh-hans').convert(row['entity1'])
                # entity2 = Converter('zh-hans').convert(row['entity2'])
                # cnt += 1
                # jsonStorage[entity1 + '@' +entity2] = row['relation']
            # cnt = 0
            # for row in reader:
            #     print(row)
            #     key = row[0] + '@' + row[1]
            #     if key in jsonStorage:
            #         cnt += 1
            #         print(cnt)
            #         output.write("\"" + row[0] + "\",\"" + row[1] + "\",\"" + jsonStorage[key] + "\",\"" + row[2] + "\"\n")
            #     else:
            #         print(key)