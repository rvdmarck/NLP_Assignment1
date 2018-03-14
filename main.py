#-*- coding:utf-8 -*-

from itertools import product
from time import clock
import random
import sys
import argparse
from utils import *


test = "123AZR grekop\x15^$ù^ùµgfdG fdoGFJ\x00DKM4789 gwwxxyrghhzzzzzzaaaaaa"

myAlphabet = ascii_lowercase+'_'
V = len(myAlphabet)**2
bigrams = [''.join(i) for i in product(myAlphabet, repeat=2)]

def makeAlphabetDic():
    res = {}
    for i in myAlphabet:
        res[i] = 0
    return res
        

def bigramCountDic(s):
    res = {}
    trigrams = {}
    for i in range(len(bigrams)):
        res[bigrams[i]] = s.count(bigrams[i])
        trigrams[bigrams[i]] = makeAlphabetDic()
    return (res, trigrams)

def rawTrigramCountDic(r, s):
    for i in range(2, len(s)):
        prevBigram = s[i-2] + s[i-1]
        r[prevBigram][s[i]] += 1
    return r

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
    cumulatedProbs = [0]*(len(myAlphabet)+1)
    sumProbs = 0
    for i in bigramProbs.values():
        sumProbs += i
    for i in range(1, len(myAlphabet)+1):
        cumulatedProbs[i] = cumulatedProbs[i-1] + bigramProbs[myAlphabet[i-1]]
    randomNumber = random.uniform(0.0, sumProbs)
    for i in range(len(cumulatedProbs)):
        if randomNumber <= cumulatedProbs[i]:
            return myAlphabet[i-1]

    return max(bigramProbs, key=lambda i: bigramProbs[i])

def perplexity(s, model):
    res = 1
    for i in range(2,len(s)):
        prevBigram = s[i-2] + s[i-1]
        if prevBigram in model.keys():
            res *= model[prevBigram][s[i]]
        else:
            res *= laplaceSmooth(0, 0) #pas sûr là
    return res**(-1/len(s))
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", help = "load the given country language model", choices=["AU", "GB", "US"])
    parser.add_argument("-g", help = "generate random letters", type=int)
    parser.add_argument("-m", help = "source model for generating random letters")
    parser.add_argument("-c", help = "compute the language model for the given country", choices=["AU", "GB", "US", "FR"])
    parser.add_argument("-t", help = "compute the language model for the given country", choices=["AU", "GB", "US"])
    parser.add_argument("-tests", help = "run all tests")
    args = parser.parse_args()

    if args.l:
        print("load file")
        model = loadModel("model." + args.l)

    if(args.g and not args.m):
        print("missing -m arg")
    elif(not args.g and args.m):
        print("missing -g arg")
    elif(args.g and args.m):
        model = loadModel("model." + args.m)
        print(generateRandom(args.g, model))
    if args.c:
        f = open("training." + args.c, encoding="utf8")
        content = f.read()
        s = filterData(content)
        (b,r) = bigramCountDic(s)
        r = rawTrigramCountDic(r, s)
        trigramProba(b, r)
        writeModel("model." + args.c, r)
    if args.t:
        model = loadModel("model." + args.t)
        res = 0
        for i in model["ab"].values():
            res += i
        print(res)
    if args.tests:
        testTexts = parseTestFile("test")
        for i in range(len(testTexts)):
            for country in ["AU", "GB", "US"]:
                model = loadModel("model." + country)
                print("TEXT nr " + str(i) + " | RESULT = " + testTexts[i][0] + " | Perplexity for : " + country + " : " + str(perplexity(testTexts[i][1], model)))

main()
