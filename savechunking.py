#Harrison Clark 85444859
#Ron Pineda 54333410
#Jeffrey Hutton 42773058
#Sam Hassanzadeh 20547066

# Save 4 times, each time outputting to 16 files.
# To look up a word we will only have to load the 4 relevant segment files
SAVE_TIMES = 20 # number of times to save tokens to disk
FILE_COUNT = 16 # number of files to segment output into per save

# which file to write/search for a word in
def outputFileNum(word):
	return ord(word[0]) % FILE_COUNT
