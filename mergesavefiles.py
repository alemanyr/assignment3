#Harrison Clark 85444859
#Ron Pineda 54333410
#Jeffrey Hutton 42773058
#Sam Hassanzadeh 20547066

import os

class Merger:
	def mergeSaveFiles(saveTimes, segmentNum):
		# this function merges save files
		# since each save is split into many segments, we can load a particular segment across all save files at once without loading the whole index into memory
		for segment in range(segmentNum):
			print("Merging segment {}".format(segmentNum))
			inverted = {} # inverted index
			for saveTime in range(saveTimes):
				print("Merging segment {} save {}".format(segmentNum, saveTime))
				fileName = "output/output_save{}_block{}.txt".format(saveTime, segment)
				curFile = open(fileName, "r", encoding='utf-8')
				for line in curFile:
					splitLine = line.strip("\n").split(" ")
					if splitLine[0] in inverted.keys():
						inverted[splitLine[0]].extend(splitLine[1:])
					else:
						inverted[splitLine[0]] = splitLine[1:]
				curFile.close()
				print("Removing " + fileName)
				os.remove(fileName)
			oFileName = "output/output_block{}.txt".format(segment)
			oFile = open(oFileName, "w",encoding='utf-8')
			print("Creating merged segment {} file".format(segmentNum))
			for word, locs in inverted.items():
				oFile.write("{} {}\n".format(word, " ".join([str(loc) for loc in locs])))
			oFile.close()
