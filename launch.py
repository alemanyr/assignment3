import zipfile, sys, getopt, time, json, math, os, psutil, signal
from tokenizer import Tokenizer
import ntpath

# Save 4 times, each time outputting to 16 files.
# To look up a word we will only have to load the 4 relevant segment files
SAVE_TIMES = 20 # number of times to save tokens to disk
FILE_COUNT = 16 # number of files to segment output into per save
MAX_TIME_BASE = 10
MAX_TIME_PER_MB = 10

# timeout signal handler function
def alarmHandler(sig, frame):
        raise Exception("Timeout(if you see this, it wasn't caught correctly)")

# which file to write/search for a word in
def outputFileNum(word):
	return ord(word[0]) % FILE_COUNT

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
	# log
	logFile = open("output/log.txt", "a")
	# signal handler
	signal.signal(signal.SIGALRM, alarmHandler)
	# ctrl-c interrupt cancels the current tokenization
	signal.signal(signal.SIGINT, alarmHandler)
	with zipfile.ZipFile(zipFile, "r") as zipped:
		#Determine which file counts/document IDs to save after
		inCount = len(zipped.namelist())
		saveTimes = [math.floor((inCount / SAVE_TIMES) * saveNum) for saveNum in range(1, SAVE_TIMES)] + [inCount - 1]
		print("{} files, saving at file #: {}".format(inCount, saveTimes))

		for zinfo in zipped.infolist():
			if (zinfo.filename.endswith('.json')):
				with zipped.open(zinfo) as f:
					# set a timeout on the tokenization
					fileSizeMB = float(zinfo.file_size) / 1000000
					fileTimeout = MAX_TIME_BASE + int(MAX_TIME_PER_MB * fileSizeMB)
					try:
						signal.alarm(fileTimeout) # timeout
						logFile.write("tokenizing " + zinfo.filename + " with timeout {}s... ".format(fileTimeout))
						content = json.loads(f.read())
						t.tokenize(content, docID)
						logFile.write("DONE\n")
					except Exception as exc:
						logFile.write("TIMEOUT\n")
						print("WARNING: Timed out on file {}, skipping".format(zinfo.filename))
					finally:
						# clear timeout
						signal.alarm(0)
					filesTokenized += 1
			# Save things
			if docID in saveTimes:
				print("Beginning save {} of {}".format(saveNum + 1, SAVE_TIMES))

				# open output files
				oFiles = []
				for i in range(FILE_COUNT):
					oFile = open("output/output_save{}_block{}.txt".format(saveNum, i), "a")
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

