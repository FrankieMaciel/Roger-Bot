from Project.config.bot import PAD_token, EOS_token

import torch
import random
import itertools

def getWordVoc(word, voc):
    if word in voc.word2index:
        return voc.word2index[word]
    else:
        return PAD_token

def indexesFromSentence(voc, sentence):
    return [getWordVoc(word, voc) for word in sentence.split(' ')] + [EOS_token]

def zeroPadding(l, fillvalue=PAD_token):
    return list(itertools.zip_longest(*l, fillvalue=fillvalue))

def binaryMatrix(l, value=PAD_token):
    m = []
    for i, seq in enumerate(l):
        m.append([])
        for token in seq:
            if token == PAD_token:
                m[i].append(0)
            else:
                m[i].append(1)
    return m

def removeRandomIndexes(indexes):
    # Gere uma lista de índices aleatórios a serem removidos
    random_indexes = random.sample(range(len(indexes)), k=random.randint(0, round(len(indexes) / 3)))
    
    # Remova os índices aleatórios da sequência
    indexes = [index for i, index in enumerate(indexes) if i not in random_indexes]
    
    return indexes

# Returns padded input sequence tensor and lengths
def inputVar(l, voc):
    indexes_batch = [removeRandomIndexes(indexesFromSentence(voc, sentence)) for sentence in l]
    lengths = torch.tensor([len(indexes) for indexes in indexes_batch])
    padList = zeroPadding(indexes_batch)
    padVar = torch.LongTensor(padList)
    return padVar, lengths

# Returns padded target sequence tensor, padding mask, and max target length
def outputVar(l, voc):
    indexes_batch = [indexesFromSentence(voc, sentence) for sentence in l]
    max_target_len = max([len(indexes) for indexes in indexes_batch])
    padList = zeroPadding(indexes_batch)
    mask = binaryMatrix(padList)
    mask = torch.BoolTensor(mask)
    padVar = torch.LongTensor(padList)
    return padVar, mask, max_target_len

# Returns all items for a given batch of pairs
def batch2TrainData(voc, pair_batch):
    pair_batch.sort(key=lambda x: len(x[0].split(" ")), reverse=True)
    input_batch, output_batch = [], []
    for pair in pair_batch:
        input_batch.append(pair[0])
        output_batch.append(pair[1])

    inp, lengths = inputVar(input_batch, voc)
    output, mask, max_target_len = outputVar(output_batch, voc)
    return inp, lengths, output, mask, max_target_len

def tokenize(pair, voc):
    # Example for validation
    batches = batch2TrainData(voc, pair)
    return batches