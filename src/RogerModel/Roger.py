from src.RogerModel.functions.createVocab import getVocab
from src.RogerModel.functions.tokenizeString import tokenize

from src.RogerModel.interact import train, testModel

voc = getVocab('Roger_Vocab')
lastResponse = 'Oiee'

buffer = []

def run(inputString):

  global lastResponse
  global buffer

  buffer.append([[lastResponse, inputString]])
  batches = []
  for response in buffer:
    batches.append(tokenize(response, voc))

  print('Batata')
  print(buffer)

  train(batches)
  response = testModel(inputString)

  lastResponse = response

  return response