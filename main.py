from string import ascii_lowercase
from itertools import product

test = "123AZR grekop\x15^$ù^ùµgfdG  fdoGFJ\x00DKM4789 gwwxxyrghhzzzzzzaaaaaa"
notfilter = ascii_lowercase + ' '


bigrams = [''.join(i) for i in product(ascii_lowercase, repeat=2)]

def filterData(s):
    s = s.lower()
    printable = set(notfilter)
    s = ''.join(filter(lambda x: x in printable, s))
    s = s.replace(" ","__") #Replace all whitespaces
    return s

def bigramCount(s):
    res = [0]*len(bigrams)
    for i in range(len(bigrams)):
        res[i] = s.count(bigrams[i])
    return res

"""
def rawTrigramCount(s):
    res = [[0]*len(ascii_lowercase)]*len(bigrams)
    for i in s:
"""
        

def main():
    s = filterData(test)
    print(s)
    print(bigramCount(s))

main()
