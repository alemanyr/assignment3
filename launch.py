import zipfile, sys, getopt, time, json, math, os, psutil
from tokenizer import Tokenizer
import ntpath

# Save 4 times, each time outputting to 16 files.
# To look up a word we will only have to load the 4 relevant segment files
SAVE_TIMES = 4 # number of times to save tokens to disk
FILE_COUNT = 16 # number of files to segment output into per save

# which file to write/search for a word in
def outputFileNum(word):
	return ord(word[0]) % FILE_COUNT

def main(inputFilePath):
	# clear the content folder before running
	for fileName in os.listdir("output/"):
		print("Removing output/" + fileName)
		os.remove("output/" + fileName)

	# stuff
	zipFile = inputFilePath
	print("zip file location is: " + zipFile)
	docID = 0
	t = Tokenizer()	
	with zipfile.ZipFile(zipFile, "r") as zipped:
		#Determine which file counts/document IDs to save after
		inCount = len(zipped.namelist())
		saveTimes = [math.floor((inCount / SAVE_TIMES) * saveNum) for saveNum in range(1, SAVE_TIMES)] + [inCount - 1]
		print("{} files, saving at file #: {}".format(inCount, saveTimes))
		saveNum = 0

		for filename in zipped.namelist():
			if (filename.endswith('.json')):
				with zipped.open(filename) as f:
					content = json.loads(f.read())
					#print("tokenizing " + filename)
					t.tokenize(content, docID)
			# Save things
			if docID in saveTimes:
				print("Beginning save {} of {}".format(saveNum, SAVE_TIMES))

				# open output files
				oFiles = []
				for i in range(FILE_COUNT):
					oFile = open("output_save{}_block{}.txt".format(saveNum, i), "a")
					oFiles.append(oFile)
				#save tokenizer output
				for word, locs in t.getDict():
					oFiles[outputFileNum(word)].write("{} {}\n".format(word, " ".join([str(loc) for loc in locs])))
				# clear tokenizer, so the next saves don't have our results included
				t.clearDict()
				# close output files
				for oFile in oFiles:
					oFile.close()

				print("Completed save {} of {}".format(saveNum, SAVE_TIMES))

				saveNum += 1

			if docID % 100 == 0:
				process = psutil.Process(os.getpid())
				print("Files read: {:6} Memory usage: {:8.2f} MB".format(docID, process.memory_info()[0] / 1000000))
			docID += 1

	f = open("output.txt", "w+")
	f.write(str(t.getDict()))
	f.close()
if __name__ == "__main__":
	main(sys.argv[1])

