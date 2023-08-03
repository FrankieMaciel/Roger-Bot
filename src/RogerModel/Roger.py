import os

from src.RogerModel.functions.createVocab import getVocab
from src.RogerModel.functions.tokenizeString import tokenize

from src.RogerModel.interact import train, testModel, saveModel

voc = getVocab('Roger_Vocab')

def ler_linhas_e_separar(arquivo):
    linhas_array = []
    with open(arquivo, 'r') as file:
        linhas = file.readlines()

    for i in range(len(linhas) - 1):
        linha_atual = linhas[i].strip()
        proxima_linha = linhas[i + 1].strip()
        linhas_array.append([linha_atual, proxima_linha])

    return linhas_array

def run(inputString):

  response = testModel(inputString)

  return response

def learn(response, output):

  batches = [[response, output]]
  tokenizedInput = tokenize(batches, voc)
  print(tokenizedInput)

  train(tokenizedInput)

def preTrain():
  resultFile = os.path.join('src','RogerModel','data','basedata.txt');
  linhas_separadas = ler_linhas_e_separar(resultFile)
  batches = [tokenize([line], voc) for line in linhas_separadas]
  finalLoss = train(batches)
  saveModel(finalLoss)

# for i in range(0, 10):
#   preTrain()