#-*- coding:utf-8 -*-

from itertools import product
from time import clock
import random
import sys
from utils import *


test = "123AZR grekop\x15^$ù^ùµgfdG fdoGFJ\x00DKM4789 gwwxxyrghhzzzzzzaaaaaa"

myAlphabet = ascii_lowercase+'_'
V = len(myAlphabet)**2
bigrams = [''.join(i) for i in product(myAlphabet, repeat=2)]


def bigramCountDic(s):
    res = {}
    for i in range(len(bigrams)):
        res[bigrams[i]] = s.count(bigrams[i])
    return res

def rawTrigramCountDic(s):
    res = {}
    for i in range(2, len(s)):
        prevBigram = s[i-2] + s[i-1]
        if prevBigram in res.keys():
            if s[i] in res[prevBigram].keys():
                res[prevBigram][s[i]] = res.get(prevBigram).get(s[i]) + 1
            else:
                res[prevBigram][s[i]] = 1
        else:
            res[prevBigram] = {s[i] : 1}
    return res

def trigramProba(biCount, triCount):
    for bigram in triCount.keys():
        for unigram in triCount[bigram].keys():
            triCount[bigram][unigram] = laplaceSmooth(triCount[bigram][unigram], biCount[bigram])

def laplaceSmooth(a,b):
    return (a+1)/(b+V)

def generateRandom(k, probs):
    fst = random.choice(myAlphabet)
    snd = random.choice(myAlphabet)
    res = fst + snd
    for i in range(k-2):
        if(3< k <300):
            res += selectNext(res, probs)
        else:
            print("wrong k value (random gen)")
    return res

def selectNext(s, probs):
    prevBigram = s[-2] + s[-1]
    bigramProbs = probs.get(prevBigram)
    return max(bigramProbs, key=lambda i: bigramProbs[i])

def perplexity(s, model):
    res = 1
    for i in range(2,len(s)):
        prevBigram = s[i-2] + s[i-1]
        if prevBigram in model.keys():
            res *= model[prevBigram][s[i]]
        else:
            res *= laplaceSmooth(0, 0) #pas sûr là
        print(res)
    res = res**(-1/len(s))
    

def main():
    country = sys.argv[1]
    f = open("training."+country, encoding="utf8")
    content = f.read()
    """
    s = filterData(content)
    b = bigramCountDic(s)
    r = rawTrigramCountDic(s)
    trigramProba(b,r)
    writeModel("model."+country,r)
    """
    z = loadModel("model."+country)
    #print(generateRandom(100, z))
    testText = parseTestFile("test")
    print(perplexity(testText[0][1], z))
    

main()


"""
def bigramCount(s):
    res = [0]*len(bigrams)
    for i in range(len(bigrams)):
        res[i] = s.count(bigrams[i])
    return res
"""

"""
def rawTrigramCount(s):
    res = [[0]*len(myAlphabet)]*len(bigrams)
    #skip 1st letter
    #skip 2nd letter
    for i in range(2,len(s)):
        col = ord(s[i]) - 97
        prev = s[i-2] + s[i-1]
        line = bigrams.index(prev)
        res[line][col] += 1 
    return res
"""
