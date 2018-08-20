import csv
import random
with open("TrainSetAggreg.csv", "r", encoding = 'utf-8') as filein:
    with open("relation2times.txt", 'r', encoding = 'utf-8') as timein:
        arr = []
        times = {}
        reader = csv.reader(timein)
        for line in reader:
            times[line[0]] = int(line[1])
        for line in filein:
            if line == "\n":
                print("cont")
                continue
            arr.append(line)
        random.shuffle(arr)
        num = len(arr)
        everylen = num / 10
        isDup = False
        for i in range(10):
            with open(str(i) + '/test.txt', 'w', encoding = 'utf-8') as testout:
                with open(str(i) + '/train.txt', 'w', encoding = 'utf-8') as trainout:
                    outbuffer = []
                    for j in range(num):
                        if j > i * everylen and j < (i + 1) * everylen:
                            testout.write(arr[j])
                        else:
                            writeTimes = 1
                            if isDup:
                                cur = list(csv.reader([arr[j]]))
                                cur = list(cur[0])
                                # print(cur[2])
                                writeTimes = times[cur[2]]
                            for tim in range(writeTimes):
                                outbuffer.append(arr[j])
                    random.shuffle(outbuffer)
                    for x in outbuffer:
                        trainout.write(x)

    