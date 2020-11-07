import json
from bs4 import BeautifulSoup
import zipfile


def tokenize(zipfilepath, filename):
	website = zipfile.ZipFile(zipfilepath, 'r')
		
	data = json.loads(website.read(filename))
		
	print("\n" +data+ "\n")
	
