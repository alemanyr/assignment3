import zipfile, sys, getopt, time, json
from tokenizer import tokenize
import ntpath


def main(inputFilePath):
	zipFile = inputFilePath
	print("zip file location is: " + zipFile)
	
	with zipfile.ZipFile(zipFile, "r") as f:
		for filename in f.namelist():
			if(filename.endswith('.json')):
				# print(ntpath.basename(filename))	
				# TODO tokenizer class/functions 
				tokenize(zipFile, ntpath.basename(filename))
				time.sleep(300)
				
	
		
	
	
if __name__ == "__main__":
	main(sys.argv[1])

