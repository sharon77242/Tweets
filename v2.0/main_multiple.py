import glob
import os
from main import *

if __name__ == "__main__":
	path = 'txts/*.txt'
	files = glob.glob(path)
	for fileName in files:
		modelFileName = fileName.replace("tweets", "model")
		langFileName = fileName.replace("tweets", "lang")
		modelFileNamePath = 'models/' + os.path.basename(modelFileName).replace('.txt', '.pickle')
		langFileNamePath = 'models/' + os.path.basename(langFileName).replace('.txt', '.pickle')
		main.start(fileName)

