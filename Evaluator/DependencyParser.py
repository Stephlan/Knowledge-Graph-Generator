from pyhanlp import *

class DependencyParser:
    def findEntities(self, sentence):
        cores, conllSentence = self.findCore(sentence)
        entities = self.extend(cores, sentence, conllSentence)
        print(entities)
        return entities
    def findCore(self, sentence):
        conllSentence = HanLP.parseDependency(sentence)
        coreNum = len(conllSentence.word)
        if coreNum > 10:
            coreNum = 10
        elif coreNum == 0:
            coreNum = 2
        # print(coreNum)
        # print(sentence)
        cores = HanLP.extractKeyword(sentence, coreNum)
        # print(cores)
        return cores, conllSentence
    def extend(self, cores, sentence, conllSentence = None):
        if conllSentence == None:
            conllSentence = HanLP.parseDependency(sentence)
        conllWords = conllSentence.word
        completions = []
        coreIds = []
        for word in conllWords:
            if word.LEMMA in cores:
                coreIds.append(word.ID)
        for word in conllWords:
            cur = word
            path = str(word.ID)
            while True:
                if cur.ID == 0:
                    break
                if cur.ID in coreIds:
                    completions.append(path)
                    break
                # print(cur.LEMMA, cur.DEPREL)
                if cur.DEPREL == "定中关系":
                    cur = cur.HEAD
                else:
                    break
                path = path + '/' + str(cur.ID)
        i = 0
        while i < len(completions):
            cur = completions[i]
            curlen = len(cur)
            for route in completions:
                if len(route) < curlen:
                    continue
                else:
                    if cur in route:
                        del completions[i]
                        break
            i += 1
        rets = []
        for each in completions:
            ret = ""
            arr = each.split('/')
            arr.sort()
            for i in arr:
                ret += conllWords[int(i) - 1].LEMMA
            rets.append(ret)
        return rets