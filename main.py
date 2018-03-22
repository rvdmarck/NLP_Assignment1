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
        res[bigrams[i]] = 0
        trigrams[bigrams[i]] = makeAlphabetDic()
    for i in range(2, len(s)):
        res[(s[i-2] + s[i-1])] += 1
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
    res = random.choice(myAlphabet) + random.choice(myAlphabet)
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

def perplexity(s, model):
    res = 1
    for i in range(2,len(s)):
        prevBigram = s[i-2] + s[i-1]
        if prevBigram in model.keys():
            res *= model[prevBigram][s[i]]
        else:
            res *= laplaceSmooth(0, 0)
    return res**(-1/len(s))
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", help = "generate random letters", type=int)
    parser.add_argument("-m", help="source model for generating random letters", choices=["AU", "GB", "US"])
    parser.add_argument("-c", help = "compute the language model for the given country", choices=["AU", "GB", "US"])
    parser.add_argument("-t", help="iz question", choices=["AU", "GB", "US"])
    parser.add_argument("-tests", help = "run all tests")
    parser.add_argument("-test", help="run tests for a single model", choices=["AU", "GB", "US"])
    args = parser.parse_args()

    if(args.g and not args.m):
        print("missing -m arg")
    elif(not args.g and args.m):
        print("missing -g arg")
    elif(args.g and args.m):
        model = loadModel("model." + args.m)
        if model != None:
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
        if model != None:
            for key, val in model["iz"].items():
                print("iz" + key + " : " + str(val))
    if args.tests:
        testTexts = parseTestFile("test")
        countries = ["AU", "GB", "US"]
        for i in range(len(testTexts)):
            print("__________________________________________________________________________________")
            tmpPerps = []
            for country in countries:
                model = loadModel("model." + country)
                if model != None:
                    tmpPerps.append(perplexity(testTexts[i][1], model))
            if model != None:
                minTmpPerp = min(tmpPerps)
                for j in range(len(countries)):
                    if tmpPerps[j] == minTmpPerp:
                        print("TEXT nr " + str(i) + " | EXPECTED RESULT = " + testTexts[i][0] + " | Perplexity for : " + countries[j] + " : " + bcolors.WARNING + str(tmpPerps[j]) + bcolors.ENDC)
                    else:
                        print("TEXT nr " + str(i) + " | EXPECTED RESULT = " + testTexts[i][0] + " | Perplexity for : " + countries[j] + " : " + str(tmpPerps[j]))
    if args.test:
        testTexts = parseTestFile("test")
        model = loadModel("model." + args.test)
        if model != None:
            for i in range(len(testTexts)):
                print("TEXT nr " + str(i) + " | Perplexity for : " + args.test + " : " + str(perplexity(testTexts[i][1], model)))
    

main()
