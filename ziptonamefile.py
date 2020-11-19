import zipfile

def zipToNameFile(zip):
	with zipfile.ZipFile(zip, "r") as zipped:
		with open("output/output_filenames.txt", "w", encoding='utf-8') as NameFile:
			for fileName in zipped.namelist():
				NameFile.write("{}\n".format(fileName))
