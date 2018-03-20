from py2neo import Graph, Node, Relationship

class NeoManager:
    def __init__(self, host, port, userName, password):
        self.username = username
        self.host = host
        self.port = port
        self.password = password
        
    def connect(self):
        self.graph = Graph("http://" + self.host + ":" + str(self.port), self.username, self.password)
        if self.graph != None:
            print("Neo4j Database Connected.")

    def createNode(self, nodeLabel, nodeName):
        node = Node(label = nodelabel, name = nodename)
        self.graph.create(node)
        return node

    def createRelation(self, nodeSrc, nodeDst, relationName):
        relationship = new Relationship(nodeSrc, relationName, nodeDst)
        return relationship

    def setRelationAttribute(self, relationship, attribute, val):
        relationship[attribute] = val
        return relationship[attribute]
        
    def getRelationAttribute(self, relationship, attribute):
        return relationship[attribute]

    def findByLabel(self, findLabel):
        return self.graph.find_one(label = findLabel)

    def findByName(self, findName):
        return self.graph.find_one(property_key = "name", property_value = findName)
        
    def findNodeRelation(self, node):
        return self.graph.match_one(start_node = node, bidirectional = True)

    def getAllRelations(self):
        return self.graph.relationship_types()

    def getRelationBetween(self, nodeNameA, nodeNameB):
        nodeA = graph.findByName(nodeNameA)
        nodeB = graph.findByName(nodeNameB)
        if nodeA == None or nodeB == None:
            return None
        else
            return self.graph.match(start_node = nodeA, end_node = nodeB, bidirectional = True)