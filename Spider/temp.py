import csv
import json
import random
from langconv import *

relpath = "../Datasets/RelationSet.csv"
csvpath = "../Datasets/TrainSetUnique.csv"
outpath = "../Datasets/TrainSetUniqueOMIT.csv"

with open(relpath, "r", encoding="utf8") as relInput:
    with open(csvpath, "r", encoding="utf8") as csvInput:
        with open(outpath, "w", encoding="utf8") as output:
            reader = csv.reader(csvInput)
            relStorage = []
            cntStorage = {}
            tempStorage = []
            outStorage = []
            for row in relInput:
                relStorage.append(row.replace('\n', ''))

            print(relStorage)
            for row in reader:
                # print(row)
                key = row[2]
                if key in relStorage:
                    tempStorage.append((row[0], row[1], row[2], row[3]))
                    if key not in cntStorage:
                        cntStorage[key] = 1
                    else:
                        cntStorage[key] += 1

            for row in tempStorage:
                times = int(1000 / cntStorage[row[2]])
                if times == 0:
                    times = 1
                # for i in range(times):
                outStorage.append("\"" + row[0] + "\",\"" + row[1] + "\",\"" + row[2] + "\",\"" + row[3] + "\"\n")
            
            # random.shuffle(outStorage)
            for row in outStorage:
                output.write(row)

            print(cntStorage)