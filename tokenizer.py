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
			# find all formatted lines
			bold = []
			strong = []
			h1 = []
			h2 = []
			h3 = []
			for i in soup.findAll('b'):
				bold.append(i.text)
			for i in soup.findAll('strong'):
				strong.append(i.text)
			for i in soup.findAll('h1'):
				h1.append(i.text)
			for i in soup.findAll('h2'):
				h2.append(i.text)
			for i in soup.findAll('h3'):
				h3.append(i.text)
			# tokenize formatted lines
			bold_tokens = [nltk.tokenize.word_tokenize(i) for i in bold]
			strong_tokens = [nltk.tokenize.word_tokenize(i) for i in strong]
			h1_tokens = [nltk.tokenize.word_tokenize(i) for i in h1]
			h2_tokens = [nltk.tokenize.word_tokenize(i) for i in h2]
			h3_tokens = [nltk.tokenize.word_tokenize(i) for i in h3]
			
			#get stems and make lower for each token
			for i in bold_tokens:
				for word in i:
					word = ps.stem(word.lower())
			for i in strong_tokens:
				for word in i:
					word = ps.stem(word.lower())
			for i in h1_tokens:
				for word in i:
					word = ps.stem(word.lower())
			for i in h2_tokens:
				for word in i:
					word = ps.stem(word.lower())
			for i in h3_tokens:
				for word in i:
					word = ps.stem(word.lower())
			#tokenize entire doc (regardless of format)
			text_tokens = nltk.tokenize.word_tokenize(soup.get_text())
			token_count = {}
			#creates a dict of the text and their weight
			tfidf = {}
			for word in text_tokens:
				word = ps.stem(word.lower())
				if word not in token_count:
					token_count[word] = 1
				else:
					if word in strong_tokens:
						token_count[word] += 5
					if word in bold_tokens:
						token_count[word] += 4
					if word in h1_tokens:
						token_count[word] += 3
					if word in h2_tokens:
						token_count[word] += 2
					if word in h3_tokens:
						token_count[word] += 1
					# always add 1 to token count if word appears with no formatting
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
