import os

from Project.vocab.normalize import normalizeString
from Project.vocab.vocab import Voc

# Read query/response pairs and return a voc object
def readVocs(datafile):
    print("Reading lines...")
    # Read the file and split into lines
    lines = open(datafile, encoding='utf-8').\
        read().strip().split('\n')
    # Split every line into pairs and normalize
    pairs = [[normalizeString(s) for s in l.split('\t')] for l in lines]
    return pairs

# Using the functions defined above, return a populated voc object and pairs list
def loadPrepareData(datafile, vocabName):
    voc = Voc(vocabName)
    print("Start preparing training data ...")
    pairs = readVocs(datafile)
    print("Read {!s} sentence pairs".format(len(pairs)))
    print("Trimmed to {!s} sentence pairs".format(len(pairs)))
    print("Counting words...")
    for pair in pairs:
        voc.addSentence(pair[0])
        # voc.addSentence(pair[1])
    print("Counted words:", voc.num_words)
    return voc, pairs

def getVocab(vocabName, dataDir):
    voc, pairs = loadPrepareData(dataDir, vocabName)
    return voc