import torch
from torch import nn, autograd, optim
from torch.autograd import Variable

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
			
class TextGen(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, n_layers):
        super(TextGen, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.n_layers = n_layers
        
        self.embedding = nn.Embedding(input_size, hidden_size).cuda()
        self.lstm = nn.LSTM(hidden_size, hidden_size, n_layers)
        self.out = nn.Linear(hidden_size, output_size)
    
    def forward(self, char_input, hidden):
        seq_len = len(char_input)
        embedded = self.embedding(char_input).view(seq_len, 1, -1)
        output, hidden = self.lstm(embedded, hidden)
        output = self.out(output.view(1, -1))
        return output, hidden
    
    def init_hidden(self):
        return (Variable(torch.zeros(self.n_layers, 1, self.hidden_size).cuda()),
                Variable(torch.zeros(self.n_layers, 1, self.hidden_size).cuda()))