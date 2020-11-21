#!/usr/bin/python3

import zipfile, sys, time
from savechunking import *
scores = {}
def termOccursIn(term):
        segment = outputFileNum(term)
        oFileName = "output/output_block{}.txt".format(segment)
        oFile = open(oFileName, "r", encoding='utf-8')
	#this could be optimized but we could also just split into more blocks if necessary
        for line in oFile:
                splitLine = line.strip("\n").split(" ")
                if splitLine[0] == term:
                        docs = set()
                        splitLine = splitLine[1:]
                        for x in range(len(splitLine)):
                                if int(x)%2 == 0:
                                        docs.add(int(splitLine[x]))
                                else:
                                        if splitLine[x-1] not in scores:
                                                scores[int(splitLine[x-1])] = float(splitLine[x])
                                        else:
                                                scores[int(splitLine[x-1])] += float(splitLine[x])
                        return docs
	# no result found
        return set()

def fileNumToName(fileNum):
        lineNum = 0
        with open("output/output_filenames.txt", "r", encoding='utf-8') as NameFile:
                for line in NameFile:
                        if lineNum == fileNum:
                                return line.strip("\n")
                        lineNum += 1
        return "Invalid filenum"

def main(maxResults, terms):
	# Start
        start = time.perf_counter()
        results = {}
	# Search for files each term occurs in, update fileNums set via intersection(boolean AND)
        fileNums = termOccursIn(terms[0])
        for term in terms[1:]:
                fileNums.intersection_update(termOccursIn(term))
        
	# Count results
        for id in fileNums:
                results[id] = scores[id]
        sorted_results = sorted(results.keys(),key=lambda x:results[x],reverse=True)
        #print(sorted_results)
        fileNumList = list(sorted_results)[0:maxResults]
        print("{} results, displaying {}".format(len(fileNums), len(fileNumList)))
	# Output results
        for fileNum in fileNumList:
                print(fileNumToName(fileNum))

	# End
        end = time.perf_counter()
        timeMS = int((end - start) * 1000)
        print("Ran in {} ms".format(timeMS))

if __name__ == "__main__":
        main(int(sys.argv[1]), sys.argv[2:])
