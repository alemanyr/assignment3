#!/usr/bin/python3

import zipfile, sys, time
from savechunking import *

def termOccursIn(term, fileCount):
	segment = outputFileNum(term)
	oFileName = "output/output_block{}.txt".format(segment)
	oFile = open(oFileName, "r", encoding='utf-8')
	#this could be optimized but we could also just split into more blocks if necessary
	for line in oFile:
		splitLine = line.strip("\n").split(" ")
		if splitLine[0] == term:
			return [int(fileNum) for fileNum in splitLine[1:fileCount + 1]]
	# no result found
	return []

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

	# Search for term
	fileNums = termOccursIn(terms[0], maxResults)
	for fileNum in fileNums:
		print(fileNumToName(fileNum))

	# End
	end = time.perf_counter()
	timeMS = int((end - start) * 1000)
	print("Ran in {} ms".format(timeMS))

if __name__ == "__main__":
	main(int(sys.argv[1]), sys.argv[2:])
