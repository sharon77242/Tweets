#!/usr/bin/python
import glob
import os
from learn import *

if __name__ == "__main__":
	path = 'txts/*.txt'
	files = glob.glob(path)
	for fileName in files:
		modelFileName = fileName.replace("tweets", "model")
		langFileName = fileName.replace("tweets", "lang")
		modelFileNamePath = 'models/' + os.path.basename(modelFileName).replace('.txt', '.pickle')
		langFileNamePath = 'models/' + os.path.basename(langFileName).replace('.txt', '.pickle')
		learn.start(fileName)

