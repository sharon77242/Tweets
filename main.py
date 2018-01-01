import torch
import numpy as np
from torch import nn, autograd, optim
from torch.autograd import Variable
import torch.nn.functional as F
import random
import pickle

def read_data():
    #lines = open('data/eng-heb.txt').read().strip().split('\n')
    lines = open('notebooks/newtweet.txt').read().strip().split('\n')
    english_lines = [l.split('\t')[0].lower().strip() for l in lines]
    return english_lines

data = read_data()

print random.choice(data)

EOS_TOKEN = 0
MAX_SEQ_LEN = 40

class Lang:
    def __init__(self):
        self.char2id = {}
        self.id2char = {}
        self.char2count = {}
        self.n_chars = 1
        
        
    def index_sentence(self, sentence):
        for c in sentence:
            self.index_char(c)
        
    
    def index_char(self, c):
        if c not in self.char2id:
            self.char2id[c] = self.n_chars
            self.char2count[c] = 1
            self.id2char[self.n_chars] = c
            self.n_chars += 1
        else:
            self.char2count[c] += 1
            
            
def prepare_data(data):
    lang = Lang()
    for sentence in data:
        if len(sentence) <= MAX_SEQ_LEN:
            lang.index_sentence(sentence)
    return lang

lang = prepare_data(data)

def sentence2variable(sentence):
    indexes = [lang.char2id[c] for c in sentence]
    input_var = Variable(torch.LongTensor(indexes).view(-1, 1))
    indexes.append(EOS_TOKEN)
    target_var = Variable(torch.LongTensor(indexes[1:]).view(-1, 1))
    return input_var, target_var

def data2variables(data):
    variables = [sentence2variable(s) for s in data if len(s) <= MAX_SEQ_LEN]
    return variables

data_variables = data2variables(data)

class TextGen(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, n_layers):
        super(TextGen, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.n_layers = n_layers
        
        self.embedding = nn.Embedding(input_size, hidden_size)
        self.lstm = nn.LSTM(hidden_size, hidden_size, n_layers)
        self.out = nn.Linear(hidden_size, output_size)
    
    def forward(self, char_input, hidden):
        seq_len = len(char_input)
        embedded = self.embedding(char_input).view(seq_len, 1, -1)
        output, hidden = self.lstm(embedded, hidden)
        output = self.out(output.view(1, -1))
        return output, hidden
    
    def init_hidden(self):
        return (Variable(torch.zeros(self.n_layers, 1, self.hidden_size)),
                Variable(torch.zeros(self.n_layers, 1, self.hidden_size)))
    
hidden_size = 800
n_layers = 4

model = TextGen(lang.n_chars, hidden_size, lang.n_chars, 1)

criterion = nn.CrossEntropyLoss()
learning_rate = 0.0001
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

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
        print 'Epoch %d Current Loss = %.4f' % (e, loss)
        loss = 0
	
print ("Saving now model and lang file.")

with open('lang.pickle', 'wb') as langFile:
    pickle.dump(lang, langFile)
	
with open('model.pickle', 'wb') as modelFile:
    pickle.dump(model, modelFile)
	
print ("Saved model and lang file successfully.")