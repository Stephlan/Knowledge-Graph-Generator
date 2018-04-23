inpath = "../Datasets/outputsEn.csv"
outpath = "../Datasets/outputsEn_Readable.csv"

with open(inpath, "r") as infile:
    with open(outpath, "w", encoding="utf-8") as outfile:
        for line in infile:
            outfile.write(line.encode('latin-1').decode('unicode_escape').encode('UTF-8','ignore').decode('UTF-8')  )