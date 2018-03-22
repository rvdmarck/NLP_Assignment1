from json import dumps, loads
from string import ascii_lowercase

notfilter = ascii_lowercase + ' '

def writeModel(filename, model):
    f = open(filename, 'w')
    f.write(dumps(model))
    f.close

def loadModel(filename):
    try:
        f = open(filename, 'r')
        model = loads(f.read())
        f.close()
        return model
    except FileNotFoundError:
        print("Please use first the -c [AU|GB|US] command before in order to compute the different models")
        return None
    

def parseTestFile(filename):
    f = open(filename, 'r')
    testText = f.readlines()
    res = makeTestData(testText)
    f.close()
    return res

def makeTestData(s):
    for i in range(len(s)):
        s[i] = s[i].split("\t")
        s[i][1] = filterData(s[i][1])
    return s

def filterData(s):
    s = s.lower().replace("\n", " ")
    printable = set(notfilter)
    s = ''.join(filter(lambda x: x in printable, s))
    s = ' '.join(s.split())
    s = s.replace(" ", "__")  # Replace all whitespaces
    return s

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
