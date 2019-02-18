# !/usr/bin/env python3
# _*_ coding: utf-8 _*_

import sys
import time
import nltk
import os

localtime = str(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time())))

def zh_segmentation():
    cutLineFlag = ["？", "！", "。", '……', '\n']
    sentenceList = []
    with open(sys.argv[2], "r", encoding="utf-8") as fileZh:
        for line in fileZh:
            words = line
            oneSentence = ""

            for word in words:    #add content to sentencelist
                if word not in cutLineFlag:
                    oneSentence = oneSentence + word
                else:
                    oneSentence = oneSentence + word
                    if oneSentence.__len__() > 4:
                        sentenceList.append(oneSentence.strip() + "\n")
                    oneSentence = ""
    fileZh.close()

    sentences = pretreatment(sentenceList)

    fileseg = path_seg(2)
    with open(fileseg, "w", encoding="UTF-8") as resultFile:
        resultFile.write(sentences)
    resultFile.close()

def en_segmentation():
    with open(sys.argv[1], 'r', encoding='UTF-8') as fileEn:
        sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        paragraphs = fileEn.readlines()
        sentenceList = []
        for paragraph in paragraphs:
            for sentence in sent_tokenizer.tokenize(paragraph):
                sentenceList.append(sentence + '\n')
    fileEn.close()

    sentences = pretreatment(sentenceList)

    fileseg = path_seg(1)
    with open(fileseg, "w", encoding='UTF-8') as fileResult:
        fileResult.write(sentences)
    fileResult.close()

def pretreatment(sentenceList):
    sentences = ''
    for sentence in sentenceList[0:-1:1]:
        sentences += sentence
    return sentences + sentenceList[-1].strip()

def path_seg(i):
    pathList = sys.argv[i].strip('.txt').split('/')
    path = mkdir('seg' + localtime) + '/' + pathList[-1]
    
    return path.strip('.txt') + '_seg.txt'

def mkdir(path):
    path = path.strip()
    path = path.rstrip("/")
    pathList = sys.argv[2].strip('.txt').split('/')
    pathmo = ''
    for name in pathList[0:-1:1]:
        pathmo += name
        pathmo += '/'
    path = pathmo + path 
    try: 
        os.makedirs(path)
        return path
        
    except Exception:
        return path

if __name__ == '__main__':
    en_segmentation()
    zh_segmentation()
