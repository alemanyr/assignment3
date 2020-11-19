#!/usr/bin/python3

#Harrison Clark 85444859
#Ron Pineda 54333410
#Jeffrey Hutton 42773058
#Sam Hassanzadeh 20547066


import zipfile, sys, getopt, time, json, math, os, psutil
from tokenizer import Tokenizer
from mergesavefiles import *
from savechunking import *
import ntpath

def main(inputFilePath):
	# clear the output folder before running
	for fileName in os.listdir("output/"):
		print("Removing output/" + fileName)
		os.remove("output/" + fileName)

	# developer.zip
	zipFile = inputFilePath
	print("zip file location is: " + zipFile)
	# the document we're on in developer.zip, can look up the specific file any docID refers to via zipped.namelist()[docID]
	docID = 0
	# the number of documents from developer.zip we've actually tokenized (not the same as docID)
	filesTokenized = 0
	# the number of times we've saved the inverted index	
	saveNum = 0
	# set of unique words
	uniqueWords = set()
	# tokenizer
	t = Tokenizer()	
	with zipfile.ZipFile(zipFile, "r") as zipped:
	#Determine which file counts/document IDs to save after
		inCount = len(zipped.namelist())
		saveTimes = [math.floor((inCount / SAVE_TIMES) * saveNum) for saveNum in range(1, SAVE_TIMES)] + [inCount - 1]
		print("{} files, saving at file #: {}".format(inCount, saveTimes))

		for filename in zipped.namelist():
			fileInfo = zipped.getinfo(filename)
			if (filename.endswith('.json')):
				#if file is greater than 80000 kb we skip over it(too big for the tokenizer)
				if fileInfo.file_size/1000 < 80000:
					with zipped.open(filename) as f:
						content = json.loads(f.read())
						t.tokenize(content, docID)
						filesTokenized += 1
			# Save things
			if docID in saveTimes:
				print("Beginning save {} of {}".format(saveNum + 1, SAVE_TIMES))

				# open output files
				oFiles = []
				for i in range(FILE_COUNT):
					oFile = open("output/output_save{}_block{}.txt".format(saveNum, i), "a", encoding='utf-8')
					oFiles.append(oFile)
				#save tokenizer output
				for word, locs in t.getDict().items():
					oFiles[outputFileNum(word)].write("{} {}\n".format(word, " ".join([str(loc) for loc in locs])))
					uniqueWords.add(word)
				# clear tokenizer, so the next saves don't have our results included
				t.clearDict()
				# close output files
				for oFile in oFiles:
					oFile.close()

				print("Completed save {} of {}".format(saveNum + 1, SAVE_TIMES))

				saveNum += 1

			if docID % 200 == 0:
				process = psutil.Process(os.getpid())
				print("Files indexed: {:6} Percent done: {:4.2f}% Memory usage: {:8.2f} MB".format(filesTokenized, (docID / inCount) * 100, process.memory_info()[0] / 1000000))
			docID += 1

	# merge save files
	print("Merging save files")
	mergeSaveFiles(SAVE_TIMES, FILE_COUNT)

	# find index size on disk in KB
	sizeKB = 0
	for fileName in os.listdir("output/"):
			print("Counting output/" + fileName)
			sizeKB += os.path.getsize("output/" + fileName) / 1000

	print("========== FINAL REPORT ==========")
	print("Number of files indexed: {}".format(filesTokenized))
	print("Number of unique words: {}".format(len(uniqueWords)))
	print("Index disk size in KB: {}".format(sizeKB))

		
if __name__ == "__main__":
		main(sys.argv[1])

