from ../utils import NeoManager

neoManager = NeoManager()
neoManager.connect("localhost", "7474", "neo", "123")
relations = neoManager.getAllRelations()
# No actual fixed Relationships
# All Relationships are Entities
# or entity relationship
potentialRels = {}

test = open("../Datasets/test.txt", "r")
seq2seq = Seq2seq()

for line in test:
    entities = extractEntity(test)
    for entity in entities:
        print(entity)
        if neoManager.findByName(entity) == None:
            neoManager.createNode(entity)
        else neoManager.checkRelationship() #Each check -> potential relationships
    input_x = seq2seq.decode(line)