#Harrison Clark 85444859
#Ron Pineda 54333410
#Jeffrey Hutton 42773058
#Sam Hassanzadeh 20547066

import json, time, re, nltk, requests
from bs4 import BeautifulSoup
from simhash import Simhash

class Tokenizer:
    def __init__(self):
        self.inverted = {} #inverted index 
			
    def tokenize(self, content, docID):
	#print(content["content"])
        chars = set('@.,/:;()-_') #set of chars that dont count as tokens on their own
	#only look through files that nltk can read
        if content["encoding"] == "ascii" or content["encoding"] == "utf-8":
            soup = BeautifulSoup(content["content"], 'html.parser')
            text_tokens = nltk.tokenize.word_tokenize(soup.get_text())
            tokens2 = []
            for item in text_tokens:
                item = item.lower()
                if item not in tokens2:
                    tokens2.append(item)
            for s in tokens2:
                if not any((c in chars) for c in s): 
                    if s not in self.inverted:
                        self.inverted[s] = [docID]
                    elif (s, docID) not in self.inverted.items(): 
                        self.inverted[s].append(docID)
					
    def getDict(self):
        return self.inverted
    def clearDict(self):
        self.inverted = {}
