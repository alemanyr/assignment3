#!/usr/bin/python3

import sys
from savechunking import *

def termOccursIn(term, fileCount):
	segment = outputFileNum(term)
	oFileName = "output/output_block{}.txt".format(segment)
	oFile = open(oFileName, "r", encoding='utf-8')
	#this could be optimized but we could also just split into more blocks
	for line in oFile:
		splitLine = line.strip("\n").split(" ")
		if splitLine[0] == term:
			return splitLine[1:fileCount]

def main(term):
	fileNums = termOccursIn(term, 100)
	for fileNum in fileNums:
		print(fileNum)

if __name__ == "__main__":
	main(sys.argv[1])
