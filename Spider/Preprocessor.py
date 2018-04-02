with open("../Datasets/outputs.csv", "r", encoding="utf8") as infile:
    with open("../Datasets/cooked.csv", "w", encoding="utf8") as outfile:
        cnt = 0
        for line in infile:
            row = line.split("@@@")
            print(cnt)
            cnt += 1
            outfile.write(row[0] + "\t" + row[1] + "\t" + "症状" + "\t\"" + row[2].replace("\n", "") + "\"\n")