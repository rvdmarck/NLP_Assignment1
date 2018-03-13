import string
test = "123AZR grekop\x15^$ù^ùµgfdG  fdoGFJ\x00DKM4789 grghh"
notfilter = "abcdefghijklmnopqrstuvwxyz "

def filterData(s):
    s = s.lower()
    printable = set(notfilter)
    s = ''.join(filter(lambda x: x in printable, s))
    s = s.replace(" ","__") #Replace all whitespaces

    return s

def main():
    s = filterData(test)
    print(s)

main()