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
    print 'indexes are ' + indexes
    input_var = Variable(torch.LongTensor(indexes).view(-1, 1))
    print 'input_var is' + input_var
    indexes.append(EOS_TOKEN)
    target_var = Variable(torch.LongTensor(indexes[1:]).view(-1, 1))
    print 'target_var is' + target_var
    return input_var, target_var
	
def generate(model, start_string, temperature, max_len):
    hidden = model.init_hidden()
    print 'hidden is ' + hidden
    start_var,_ = sentence2variable(start_string)
    print 'start_var is ' + start_var

    for i in range(len(start_string) - 1):
        _, hidden = model(start_var[i], hidden)
    
    str = start_string
    print 'str is ' + str
    out, hidden = model(start_var[-1], hidden)
    print 'out is ' + out
    out_dist = out.data.view(-1).div(temperature).exp()
    print 'out_dist is ' + out_dist 
    new_c = lang.id2char[torch.multinomial(out_dist, 1)[0]]
    print 'new_c is ' + new_c
    str += new_c
    print 'str after +=new_c is ' str
    for i in range(max_len):
        new_c_var, _ = sentence2variable(new_c)
        print 'new_c_var is' + new_c_var
        out, hidden = model(new_c_var, hidden)
        out_dist = out.data.view(-1).div(temperature).exp()
        print 'out_dist is' + out_dist
        char_id = torch.multinomial(out_dist, 1)[0]
        print 'char_id is ' + char_id 
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
            print 'tweetGenerated is ' + tweetGenerated
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
