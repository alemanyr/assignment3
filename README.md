#repo for assignment 3
new tokenizer that iterates through folders developer.zip
tokenizes every json file and places in inverted index
inverted index is periodically saved to many chunk files in output folder
search engine part will only have to search some subset of the chunk files

##Indexer
takes content.txt, inverts from Doc->terms to terms->Docs and saves it in invertedContent.txt
-stemming
-formatted text(headings, bold, etc)

to run:
```./index.py path```

(path is path to developer.zip)

##Search
searches the relevant files for each term
since terms are split between files, it only needs to search a small subset of files

```./search.py num_results term1 term2 term3```
