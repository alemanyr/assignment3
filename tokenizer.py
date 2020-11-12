import json, time, re, nltk, requests
from bs4 import BeautifulSoup
from simhash import Simhash
#nltk.download('punkt')
class Tokenizer:
	def __init__(self):
		self.inverted = {} #inverted index 
			
	def tokenize(self, content, docID):
		#print(content["content"])
		chars = set('@.,/:;()-_') #set of chars that dont count as tokens on their own
	
		soup = BeautifulSoup(content["content"], 'html.parser')
		text_tokens = nltk.tokenize.word_tokenize(soup.get_text())
		tokens2 = []
		for item in text_tokens:
			item = item.lower()
			if item not in tokens2:
				tokens2.append(item)
		for s in tokens2:
			if not any((c in chars) for c in s): #
				if s not in self.inverted:
					self.inverted[s] = [docID]
				elif (s, docID) not in self.inverted.items(): #TODO: dont append to key if docID value is already posted
					self.inverted[s].append(docID)
					#print(s + " not in the inverted list\n")
		print(self.inverted)			
		#time.sleep(300)
			
		#with open("content.txt", 'a', encoding = "utf-8") as content_file:
		#	print("hi")	
	def getDict(self):
		return self.inverted	
