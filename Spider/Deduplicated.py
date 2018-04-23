with open('../Datasets/BFSUnique.csv', 'r', encoding='utf8') as infile:
    with open('../Datasets/BFSUniqueOut.csv', 'w', encoding='utf8') as outfile:
        l1 = []
        for row in infile:
            l1.append(row)
        l2 = list(set(l1))
        l2.sort(key = l1.index)
        for row in l2:
            outfile.write(row + '\n')

# with open('../Datasets/BFSUnique.csv', 'r', encoding='utf8') as infile:
#     with open('../Datasets/BFSUniqueOut.csv', 'w', encoding='utf8') as outfile:
#         for row in infile:
#             if(row != '\n'):
#                 outfile.write(row)