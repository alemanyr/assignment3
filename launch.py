import zipfile, sys, getopt, time, json
from tokenizer import Tokenizer
import ntpath


def main(inputFilePath):
	zipFile = inputFilePath
	print("zip file location is: " + zipFile)
	docID = 1
	t = Tokenizer()	
	with zipfile.ZipFile(zipFile, "r") as zipped:
		for filename in zipped.namelist():
			if (filename.endswith('.json')):
				with zipped.open(filename) as f:
					content = json.loads(f.read())
					print("tokenizing "+ filename+ "\n")
					t.tokenize(content, docID)
					docID = docID+1
					time.sleep(10)
				
if __name__ == "__main__":
	main(sys.argv[1])

