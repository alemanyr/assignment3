#Harrison Clark 85444859
#Ron Pineda 54333410
#Jeffrey Hutton 42773058
#Sam Hassanzadeh 20547066
from nltk.stem import PorterStemmer
import json, time, re, nltk, requests
from bs4 import BeautifulSoup
from simhash import Simhash
import TFIDF
ps = PorterStemmer()
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
                        token_count = {}
                        #creates a dict of the text and their weight
                        tfidf = {}
                        for word in text_tokens:
                                word = ps.stem(word.lower())
                                if word not in token_count:
                                        token_count[word] = 0
                                else:
                                        token_count[word] += 1
                        #computes the tf idf score
                        tfidf = TFIDF.computeTFIDF(token_count,soup.get_text())
                        tokens2 = []
                        for word in tfidf.keys():
				if word not in tokens2:
					tokens2.append(word)
			for s in tokens2:
                                if s not in tokens2:
                                        tokens2.append(s)
                                if not any((c in chars) for c in s): 
                                        if s not in self.inverted:
                                                self.inverted[s] = [(docID,tfidf[s])]
                                        elif (s, docID) not in self.inverted.items(): 
                                                self.inverted[s].append((docID,tfidf[s]))
					
        def getDict(self):
                return self.inverted
        def clearDict(self):
                self.inverted = {}
