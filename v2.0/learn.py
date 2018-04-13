import torch
import numpy as np
from torch import nn, autograd, optim
from torch.autograd import Variable
import torch.nn.functional as F
import random
from classes import *
import pickle
import glob
import os
import sys

def read_data(fileNamePath): 
    #lines = open('data/eng-heb.txt').read().strip().split('\n')
	lines = open(fileNamePath, encoding="utf8").read().strip().split('\n')
	english_lines = [l.split('\t')[0].lower().strip() for l in lines]
	return english_lines

def prepare_data(data):
    lang = Lang()
    for sentence in data:
        if len(sentence) <= MAX_SEQ_LEN:
            lang.index_sentence(sentence)
    return lang

def sentence2variable(sentence, lang):
    indexes = [lang.char2id[c] for c in sentence]
    input_var = Variable(torch.LongTensor(indexes).view(-1, 1).cuda())
    indexes.append(EOS_TOKEN)
    target_var = Variable(torch.LongTensor(indexes[1:]).view(-1, 1).cuda())
    return input_var, target_var

def data2variables(data, lang):
    variables = [sentence2variable(s, lang) for s in data if len(s) <= MAX_SEQ_LEN]
    return variables
    
def train_seq(model, optimizer, criterion, input_var, target_var):
    optimizer.zero_grad()
    seq_len = len(input_var.data)
    if seq_len == 0:
        return
    loss = 0
    hidden = model.init_hidden()
    for o in range(seq_len):
        output, hidden = model(input_var[o], hidden)
        loss += criterion(output.view(-1).unsqueeze(0), target_var[o])
    
    loss.backward()
    torch.nn.utils.clip_grad_norm(model.parameters(), 5.0)
    optimizer.step()
    return loss.data[0] / seq_len
	
def start(fileName):
	modelFileName = fileName.replace("tweets", "model")
	langFileName = fileName.replace("tweets", "lang")
	modelFileNamePath = 'models/' + os.path.basename(modelFileName).replace('.txt', '.pickle')
	langFileNamePath = 'models/' + os.path.basename(langFileName).replace('.txt', '.pickle')
	
	data = read_data(fileName)
	print (random.choice(data))
	lang = prepare_data(data)
	data_variables = data2variables(data, lang)
	
	hidden_size = 800
	n_layers = 3

	model = TextGen(lang.n_chars, hidden_size, lang.n_chars, 1)
	model.cuda()

	criterion = nn.CrossEntropyLoss()
	learning_rate = 0.0001
	optimizer = optim.Adam(model.parameters(), lr=learning_rate)
	
	n_epochs = 20000
	print_every = 100
	loss = 0
	for e in range(1, n_epochs + 1):
		pair = random.choice(data_variables)
		input_var = pair[0]
		target_var = pair[1]
		temp = train_seq(model, optimizer, criterion, input_var, target_var)
		if temp != None:
			#print temp
			loss += temp
		
		if e % print_every == 0:
			loss = loss / print_every
			print ('Epoch %d Current Loss = %.4f' % (e, loss))
			loss = 0
		
	print ('Saving now model file for ' + modelFileName) 	
	torch.save(model, modelFileName + ".pth")
	with open(modelFileNamePath, 'wb') as modelFile:
		pickle.dump(model, modelFile)			
	print ('Saved model file successfully.')
	
	print ('Saving now lang file for ' + langFileName)
	with open(langFileNamePath, 'wb') as langFile:
		pickle.dump(lang, langFile)	
	print ('Saved lang file successfully.')
				
if __name__ == "__main__":
	if len(sys.argv) != 2:
		print ('Are you stupid?! Give me the tweets txt file!!')
		sys.exit()
	EOS_TOKEN = 0
	MAX_SEQ_LEN = 40
	start(sys.argv[1])