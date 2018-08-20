with open("test_bak.txt", "r", encoding="utf8") as infile:
    with open("test.txt", "w", encoding="utf8") as outfile:
        while True:
            line = infile.readline()
            if line == "":
                break
            rows = line.split("\t")
            print(rows)
            if not rows[2].startswith("\""):
                rows[3] = "\"" + rows[3].replace("\n", "") + "\"\n"
            outfile.write(rows[0] + "," + rows[1] + "," + rows[2] + "," + rows[3])