import collections
import os
from random import random

n = 4 #n-gram

def train_word_ngram(data, order):
    lm = collections.defaultdict(collections.Counter)
    pad = ["~"] * order
    data = pad + data
    for i in range(len(data)-order):
        history, char = ' '.join(data[i:i+order]), ''.join(data[i+order])
        lm[history][char]+=1
    return lm

def normalize(counter):
    s = float(sum(counter.values()))
    return [(c,cnt/s) for c,cnt in counter.items()]


def generate_word(lm, history, order):
        history = history[-order:]
        dist = normalize(lm[' '.join(history)])
        x = random()
        for c,v in dist:
            x = x - v
            if x <= 0: return c

def generate_text(lm, order, nwords=200):
    history = ["~"] * order
    out = []
    for i in range(nwords):
        c = generate_word(lm, history, order)
        history = history[-order:] + [c]
        out.append(c)
    return out


indir = os.getcwd() + '/althingisraedur/'

lm = collections.defaultdict(collections.Counter)

for root,dirs,filenames in os.walk(indir):
    for f in filenames:
        with open(indir + f) as d:
            data = d.readlines()
        pad = ["~"] *  n
        data = pad + data
        print(f)
        for i in range(len(data)-n):
            history, char = ' '.join(data[i:i+n]), ''.join(data[i+n])
            lm[history][char]+=1


new_speech = generate_text(lm, 120)

for word in new_speech:
    if word =='NA':
        print('\n\n')
    if word == ' ':
        print('\n')
    else:
        print(word[:-1],end=" ")


import pickle

#save ngram dict
with open('fourgram.pickle','wb') as handle:
    pickle.dump(lm,handle,protocol=pickle.HIGHEST_PROTOCOL)

#with open('fourgram.pickle','rb') as handle:
#    b = pickle.load(handle)

