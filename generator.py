import torch
import numpy as np
from torch import nn, autograd, optim
from torch.autograd import Variable
import torch.nn.functional as F
import random
import pickle

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
	
tweetsDictionary = {}

print ("Loading now model and lang file.")

with open('lang.pickle', 'rb') as langFile:
    lang = pickle.load(langFile)
	
with open('model.pickle', 'rb') as modelFile:
    model = pickle.load(modelFile)
	
print ("Loaded model and lang file successfully.")
	
for i in range(200):
    tweetGenerated = generate(model, 'i am at ', 0.8, 200)	
	tweetsDictionary[tweetGenerated] = tweetGenerated[tweetGenerated] + 1

	# this is hurani. it can be changed with some kind of algorithm
maxValue = 0

for key, value in tweetsDictionary.items():
    if (value > maxValue):
		value = maxValue
		bestTweet = key

print bestTweet	