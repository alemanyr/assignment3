import math


def computeTF(wordDict, doc):
    tfDict = {}
    corpusCount = len(doc)
    for word, count in wordDict.items():
        tfDict[word] = count/float(corpusCount)
    return(tfDict)

def computeIDF(docList):
    idfDict = {}
    N = len(docList)
    
    idfDict = docList
    for word, val in idfDict.items():
        idfDict[word] = math.log10(N / (float(val) + 1))
        
    return(idfDict)

def computeTFIDF(wordDict, doc):
    tfBow = computeTF(wordDict,doc)
    idfs = computeIDF(wordDict)
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = val*idfs[word]
    return(tfidf)


    
