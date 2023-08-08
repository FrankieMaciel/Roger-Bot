import os

from src.RogerModel.functions.createVocab import getVocab
from src.RogerModel.functions.tokenizeString import tokenize

from src.RogerModel.interact import train, testModel, saveModel, voc
from src.RogerModel.config import model_name

# sample = 'vai se fuder seu arrombado do caralho skdiuf'
# encoding = tokenizer.encode(sample)
# print(encoding)
# print(tokenizer.convert_ids_to_tokens(encoding))

# print(voc.word2index)

def ler_linhas_e_separar(arquivo):
    linhas_array = []
    with open(arquivo, 'r') as file:
        linhas = file.readlines()

    for i in range(len(linhas) - 1):
        linha_atual = linhas[i].strip()
        proxima_linha = linhas[i + 1].strip()
        a1 = linha_atual.split(' ')[0] != ''
        a2 = proxima_linha.split(' ')[0] != ''
        if a1 and a2:
          linhas_array.append([linha_atual, proxima_linha])

    return linhas_array

def run(inputString):

  response = testModel(inputString)

  return response

def learn(response, output):

  print(response)
  print(output)
  batches = [[response, output]]
  tokenizedInput = tokenize(batches, voc)
  finalLoss = train([tokenizedInput])
  saveModel(finalLoss, model_name)

def preTrain():
  resultFile = os.path.join('src','RogerModel','data','basedata.txt');
  linhas_separadas = ler_linhas_e_separar(resultFile)
  batches = [tokenize([line], voc) for line in linhas_separadas]
  finalLoss = train(batches)
  saveModel(finalLoss, model_name + '_Default')

# for i in range(0, 10):
#   print('Epoch: ' + str(i))
#   preTrain()