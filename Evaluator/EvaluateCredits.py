from NeoManager import *
import operator
from itertools import tee

def __main__():
    neo = NeoManager('localhost', 7474, 'neo4j', '123')
    neo.connect()
    probThreshold = 0.8
    markThreshold = 2
    updateCredits(neo, prune = True, probThreshold = probThreshold, markThreshold = markThreshold)
    
def updateCredits(neo, prune = False, probThreshold = 0.5, markThreshold = 3, topN = 5):
    selected = neo.findAllByLabel('Creditless')
    selected = list(selected)
    totalEdgeDel = 0
    totalNodeDel = 0
    for curNode in selected:
        print(curNode['name'])
        relevants = neo.graph.match(start_node = curNode, bidirectional = True)
        print(relevants)
        relevants = list(relevants)
        bakRels0 = list(relevants)
        bakRels1 = list(relevants)
        print(bakRels1)
        relDict = {}
        total = 0
        for rel in relevants:
            relType = rel.type()
            total += 1
            if relType in relDict:
                relDict[relType] += 1
            else:
                relDict[relType] = 1
        
        prob = 0.0
        mark = 0.0
        sortedDict = sorted(relDict.items(), key = operator.itemgetter(0))
        for relType, count in sortedDict[0:topN]:
            prob += count / total
            mark += count * prob

        print(prob, mark)
        cntEdge = 0
        cntNode = 0
        if mark < markThreshold or prob < probThreshold:
            for rel in bakRels0:
                cntEdge += 1
                print("seperate " + str(rel) )
                neo.graph.separate(rel)
            print(prob, mark)
            neo.graph.delete(curNode)
            cntNode += 0
            continue
        pruneKeys = list(map(lambda t: t[0], sortedDict[topN:]))
        for rel in bakRels1:
            relType = rel.type()
            if relType in pruneKeys:
                cntEdge += 1
                neo.graph.separate(rel)

        curNode["credits"] = mark
        print(curNode)
        neo.graph.push(curNode)
        totalEdgeDel += cntEdge
        totalNodeDel += cntNode
    print(totalEdgeDel, totalNodeDel)

__main__()