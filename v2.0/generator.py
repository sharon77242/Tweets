import torch
from torch import nn, autograd, optim
from torch.autograd import Variable
import torch.nn.functional as F
import pickle
import sys
from classes import *

EOS_TOKEN = 0

def sentence2variable(sentence):
    indexes = [lang.char2id[c] for c in sentence]
    input_var = Variable(torch.LongTensor(indexes).view(-1, 1))
    indexes.append(EOS_TOKEN)
    target_var = Variable(torch.LongTensor(indexes[1:]).view(-1, 1))
    return input_var, target_var
	
def generate(model, start_string, temperature, max_len):
    hidden = model.init_hidden()
    start_var,_ = sentence2variable(start_string)
    for i in range(len(start_string) - 1):
        _, hidden = model(start_var[i], hidden)
    
    str = start_string
    out, hidden = model(start_var[-1], hidden)
    out_dist = out.data.view(-1).div(temperature).exp()
    new_c = lang.id2char[torch.multinomial(out_dist, 1)[0]]
    str += new_c
    for i in range(max_len):
        new_c_var, _ = sentence2variable(new_c)
        out, hidden = model(new_c_var, hidden)
        out_dist = out.data.view(-1).div(temperature).exp()
        char_id = torch.multinomial(out_dist, 1)[0]
        if char_id == EOS_TOKEN:
            return str
        new_c = lang.id2char[char_id]
        str += new_c
    return str

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print 'Are you stupid?! How can I generate something without the paths of the model and lang files?!'
		sys.exit()

	modelFileNamePath = sys.argv[1]
	langFileNamePath = sys.argv[2]

	tweetsDictionary = {}

	print 'Loading now model file.'
	with open(modelFileNamePath, 'rb') as modelFile:
		model = pickle.load(modelFile)		
	print 'Loaded model file successfully.'
	
	print 'Loading now lang file.'
	with open(langFileNamePath, 'rb') as langFile:
		lang = pickle.load(langFile)		
	print 'Loaded lang file successfully.'

	print 'Generating tweets..........'
	for i in range(1000):
		tweetGenerated = generate(model, '# ', 0.15, 50)
		if tweetGenerated in tweetsDictionary:
		tweetsDictionary[str(tweetGenerated)] += 1
		else:
		tweetsDictionary[str(tweetGenerated)] = 0

	# this is hurani. it can be changed with some kind of algorithm
	maxValue = 0

	for key, value in tweetsDictionary.items():
		print('tweet is: ' + key + ' count: ' + str(value))
		if (value > maxValue):
			maxValue = value
			bestTweet = key

	print ('dictionary size is: ' + str(len(tweetsDictionary)))

	print ('bestTweet is: ' + bestTweet + " size is: " + str(maxValue))
