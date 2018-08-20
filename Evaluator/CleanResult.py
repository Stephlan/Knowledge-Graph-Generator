from NeoManager import *

"subclass of",0
"instance of",1
"interact with",2
"genetic Association",3
"symptoms",4
"taxon",5
"topic’s main category",6
"part",7
"active role in",8
"treated",9
"cause and effect",10 
"NA",11


detectDict = ['symptoms']
StartConflictRules = {}
StartConflictRules['symptoms'] = {}
StartConflictRules['symptoms']['startTo'] = ['sypmtoms', 'active role in', 'treated', 'interact with', 'part']
StartConflictRules['symptoms']['endWith'] = ['active role in', 'treated', 'interact with', 'part']
EndConflictRules = {}
EndConflictRules['symptoms'] = {}
EndConflictRules['symptoms']['startTo'] = ['active role in', 'treated', 'interact with', 'part']
EndConflictRules['symptoms']['endWith'] = ['sypmtoms', 'active role in', 'treated', 'interact with', 'part']

def DetectLogics(neo, node0, trustable0, node1, trustable1, rel):
    for relDetect in detectDict:
        if trustable0:
            res = neo.hasStartToRelation(node0, relDetect)    #如果是疾病
            if res and relDetect in StartConflictRules and rel in StartConflictRules[relDetect]['startTo']:
                return False
            res = neo.hasEndWithRelation(node0, relDetect)    #如果是症状
            if res and relDetect in StartConflictRules and rel in StartConflictRules[relDetect]['endWith']:
                return False
        if trustable1:
            res = neo.hasStartToRelation(node1, rel)
            if res and relDetect in EndConflictRules and rel in EndConflictRules[relDetect]['startTo']:
                return False
            res = neo.hasEndWithRelation(node1, rel)
            if res and relDetect in EndConflictRules and rel in EndConflictRules[relDetect]['endWith']:
                return False
    return True

def __main__():
    neo = NeoManager('localhost', 7474, 'neo4j', '123')
    neo.connect()
    with open('../Evaluator/CalculationResult.csv', 'r', encoding = 'utf-8') as input:
        reader = csv.reader(input)
        # row: [0] entity1 [1] entity2 [2] relation [3] example
        for row in reader:
            print(row)
            fatherTrustable, fatherNode = neo.findByName(row[0])
            trustable0, node0 = neo.findByName(row[1])
            trustable1, node1 = neo.findByName(row[2])
            print(node0)
            if fatherNode == None:
                fatherNode = neo.createNode("Creditless", row[0])
            if node0 == None:
                print("NotFound!!!")
                node0 = neo.createNode("Creditless", row[1])
            if node1 == None:
                print("NotFound!!!")
                node1 = neo.createNode("Creditless", row[2])
            
            # Logical Conflicts
            noConflict = DetectLogics(neo, node0, trustable0, node1, trustable1, row[3])
            if not noConflict:
                continue

            relation = neo.getRelationBetween(node0, node1)
            if relation == None or relation != row[3]:
                relation = neo.createRelation(node0, node1, row[3]) 
            print(relation)

            relation = neo.getRelationBetween(fatherNode, node0)
            if relation == None or relation != 'BookTiltleOf':
                relation = neo.createRelation(fatherNode, node0, 'BookTiltleOf') 
            print(relation)

            relation = neo.getRelationBetween(fatherNode, node1)
            if relation == None or relation != 'BookTiltleOf':
                relation = neo.createRelation(fatherNode, node1, 'BookTiltleOf') 

            print(relation)

__main__()