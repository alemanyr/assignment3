import json, time, re, nltk, requests
from bs4 import BeautifulSoup
from simhash import Simhash
nltk.download('punkt')

def tokenize(content):
	#print(content["content"])
	chars = set('@.,/:;()-_') #set of chars that dont count as tokens on their own
	
	soup = BeautifulSoup(content["content"], 'html.parser')
	text_tokens = nltk.tokenize.word_tokenize(soup.get_text())
	for s in text_tokens:
		if not any((c in chars) for c in s):
			print(s)
	time.sleep(300)
	# TODO: do stuff with text_tokens and write inverse index to content_file
	#with open("content.txt", 'a', encoding = "utf-8") as content_file:
	#	print("hi")	
	
