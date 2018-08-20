from py2neo import Graph, Node, Relationship, NodeSelector
import csv

class NeoManager:
    def __init__(self, host, port, username, password):
        self.username = username
        self.host = host
        self.port = port
        self.password = password
        
    def connect(self):
        print("http://" + self.host + ":" + str(self.port), self.username, self.password)
        self.graph = Graph("http://" + self.host + ":" + str(self.port), username = self.username, password = self.password)
        if self.graph != None:
            print("Neo4j Database Connected.")
            self.selector = NodeSelector(self.graph)

    def createNode(self, nodelabel, nodename):
        nodename = str(nodename)
        nodelabel = str(nodelabel)
        node = Node(nodelabel, name = nodename)
        self.graph.create(node)
        return node

    def createRelation(self, nodeSrc, nodeDst, relationName):
        relationName = str(relationName)
        if nodeSrc == None or nodeDst == None:
            return
        relationship = Relationship(nodeSrc, relationName, nodeDst)
        print(relationship)
        # self.setRelationAttribute(relation, 'credential', 0.9)
        self.graph.create(relationship)
        return relationship

    def setRelationAttribute(self, relationship, attribute, val):
        relationship[attribute] = val
        return relationship[attribute]
        
    def getRelationAttribute(self, relationship, attribute):
        return relationship[attribute]

    def findByName(self, findName):
        findName = str(findName)
        print("HEEEEEERE")
        print(findName)
        trustable = self.graph.find_one(property_key='name', property_value = findName, label = 'labelHolder')
        if trustable == None:
            untrustable = self.graph.find_one(property_key='name', property_value = findName, label = 'Creditless')
            print(untrustable)
            return False, untrustable
        else:
            return True, trustable
        
    def findNodeRelation(self, node):
        return self.graph.match_one(start_node = node, bidirectional = True)

    def findAllByLabel(self, findLabel):
        findLabel = str(findLabel)
        selected = self.selector.select(findLabel)
        return selected


    def hasStartToRelation(self, node, relstr):
        return self.graph.match(start_node=node, rel_type=relstr)

    def hasEndWithRelation(self, node, relstr):
        return self.graph.match(end_node=node, rel_type=relstr)

    def getRelationBetween(self, nodeA, nodeB):
        if nodeA == None or nodeB == None:
            return None
        else:
            return self.graph.match(start_node = nodeA, end_node = nodeB, bidirectional = True)



# neo = NeoManager('localhost', 7474, 'neo4j', '123')
# neo.connect()
# with open('../Datasets/TrainSetUnique.csv', 'r', encoding = 'utf-8') as input:
#     reader = csv.reader(input)
#     # row: [0] entity1 [1] entity2 [2] relation [3] example
#     for row in reader:
#         node0 = neo.findByName(row[0])
#         node1 = neo.findByName(row[1])
#         print(node0)
#         if node0 == None:
#             node0 = neo.createNode("labelHolder", row[0])
#         if node1 == None:
#             node1 = neo.createNode("labelHolder", row[1])
#         relation = neo.getRelationBetween(node0, node1)
#         print(relation)
#         if relation == None or relation != row[2]:
#             print(row[2])
#             relation = neo.createRelation(node0, node1, row[2])