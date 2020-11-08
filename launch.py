import zipfile, sys, getopt, time, json
from tokenizer import tokenize
import ntpath


def main(inputFilePath):
	zipFile = inputFilePath
	print("zip file location is: " + zipFile)
	
	with zipfile.ZipFile(zipFile, "r") as zipped:
		for filename in zipped.namelist():
			if (filename.endswith('.json')):
				with zipped.open(filename) as f:
					content = json.loads(f.read())
					#print(content)
					tokenize(content)
					time.sleep(300)
				
if __name__ == "__main__":
	main(sys.argv[1])

