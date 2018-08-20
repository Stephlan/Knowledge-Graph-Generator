# Finite State Machine

import docx
import re
import csv
from DependencyParser import *

class BookLearner:

    def __init__(self):
        self.filepath = 'book.docx'
        self.rankArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '零']
        self.parser = DependencyParser()
        self.outpath = 'BookKnowledge.csv'
        self.outHandle = open(self.outpath, 'a', encoding='utf-8')

    def JudgeListing(self, line):
        res = re.match(r'^\(.*\)', line)
        if res != None:
            curstr = res.group()
            num = len(curstr)
            curstr = curstr[1:-1]
            for i in curstr:
                if i not in self.rankArr:
                    return None
            return line[num:]
        else:
            res = re.match(r'^[0-9]*．', line)
            if res:
                num = len(res.group())
                return line[num:]
            return None

    def Submit(self, header, line):
        arr = line.split("。")
        for line in arr:
            extension = self.parser.findEntities(line)
            if header != None:
                extension.append(header)
            extension = list(set(extension))
            for i in range(len(extension)):
                for j in range(i + 1, len(extension)):
                    if i == j:
                        continue
                    self.outHandle.write('\"' + extension[i] + '\",\"' + extension[j] + '\",\"' + line + '\",\"' + header +  '\"\n')

    def run(self):
        content = docx.Document(self.filepath)
        contextHeader = None
        isEnd = True
        isListing = False
        context = ""

        for para in content.paragraphs:
            style = para.style.name
            curtext = para.text
            curtext = curtext.replace(' ', '').replace('\t', '')
            # print(para.text)
            if curtext.endswith('。'):
                isEnd = True
            else:
                isEnd = False

            if style.startswith('Heading') or style.startswith('Title'):
                contextHeader = curtext
                print("Before: " + contextHeader)
                contextHeader = re.sub(r"第.*章", '', contextHeader)
                contextHeader = re.sub(r"第.*篇", '', contextHeader)
                contextHeader = re.sub(r"第.*节", '', contextHeader)
                print("After: " + contextHeader)
                isEnd = True
                
            res = self.JudgeListing(curtext)
            if res:
                # print(res)
                curtext = res
            context += curtext
            if isEnd:
                self.Submit(contextHeader, context)
                context = ""


learner = BookLearner()
learner.run()