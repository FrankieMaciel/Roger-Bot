import torch
import string

from src.RogerModel.config import MAX_LENGTH, device
from src.RogerModel.functions.normalizeString import normalizeString
from src.RogerModel.functions.tokenizeString import indexesFromSentence

def verificar_pontuacao(texto):
    pontuacoes = string.punctuation
    for caractere in texto:
        if caractere in pontuacoes:
            return True
        else:
            return False

def evaluate(encoder, decoder, searcher, voc, sentence, max_length=MAX_LENGTH):
    ### Format input sentence as a batch
    # words -> indexes
    indexes_batch = [indexesFromSentence(voc, sentence)]
    # Create lengths tensor
    lengths = torch.tensor([len(indexes) for indexes in indexes_batch])
    # Transpose dimensions of batch to match models' expectations
    input_batch = torch.LongTensor(indexes_batch).transpose(0, 1)
    # Use appropriate device
    input_batch = input_batch.to(device)
    lengths = lengths.to("cpu")
    # Decode sentence with searcher
    tokens, scores = searcher(input_batch, lengths, max_length)
    # indexes -> words
    decoded_words = [voc.index2word[token.item()] for token in tokens]
    return decoded_words

def evaluateInput(inputString, encoder, decoder, searcher, voc):
    input_sentence = ''
    try:
        # Get input sentence
        input_sentence = inputString
        # Normalize sentence
        input_sentence = normalizeString(input_sentence)
        print(input_sentence)
        # Evaluate sentence
        output_words = evaluate(encoder, decoder, searcher, voc, input_sentence)
        # Format and print response sentence
        print(output_words)
        output_words[:] = [x for x in output_words if not (x == 'EOS' or x == 'PAD')]

        finalSentece = '';
        output_words[0] = output_words[0].capitalize()
        for word in output_words:
            if verificar_pontuacao(word):
                finalSentece += word
            else:
                finalSentece += ' ' + word

        return finalSentece

    except KeyError:
        print("Error: Encountered unknown word.")

