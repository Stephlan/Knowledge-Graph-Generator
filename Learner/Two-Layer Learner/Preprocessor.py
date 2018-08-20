import csv
import re

superClassDict = {}
superClassDict["significant drug interaction"] = superClassDict["physically interacts with"] = "interact with"
superClassDict['parent taxon'] = superClassDict['taxon rank'] = 'taxon'
superClassDict['has part'] = superClassDict['part of'] = superClassDict['health specialty'] = 'part'
superClassDict['subject has role'] = superClassDict['active ingredient in'] = superClassDict['found in taxon'] = 'active role in'
superClassDict['medical condition treated'] = superClassDict['drug used for treatment'] = 'treated'
superClassDict['has cause'] = superClassDict['has effect'] = 'cause and effect'
print(superClassDict)

def csvToString(columns):
    ret = ""
    for col in columns:
        ret +=  '\"' + col + '\",'
    return ret[:len(ret) - 1]

with open('../../Datasets/TrainSetUnique.csv', 'r', encoding = 'utf-8') as filein:
    with open('../../Datasets/TrainSetAggreg.csv', 'w', encoding = 'utf-8') as fileout:
        reader = csv.reader(filein)
        for cols in reader:
            if cols[2] in superClassDict:
                cols[2] = superClassDict[cols[2]]
            fileout.write(csvToString(cols) + '\n')


        