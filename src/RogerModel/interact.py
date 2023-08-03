from torch import optim
import torch.nn as nn
import torch
import os

from src.RogerModel.config import model_name,save_dir, learning_rate, decoder_learning_ratio, hidden_size, dropout, encoder_n_layers, decoder_n_layers, attn_model, device, batch_size, clip
from src.RogerModel.model.encoder import EncoderRNN
from src.RogerModel.model.decoder import LuongAttnDecoderRNN
from src.RogerModel.model.model import GreedySearchDecoder
from src.RogerModel.evaluate import evaluateInput

from src.RogerModel.train import trainIters

from src.RogerModel.functions.createVocab import getVocab
voc = getVocab('Roger_Vocab')

loadFilename = os.path.join(save_dir, '{}_checkpoint.tar'.format(model_name))

# Load model if a ``loadFilename`` is provided
if os.path.exists(loadFilename):
    # If loading on same machine the model was trained on
    checkpoint = torch.load(loadFilename)
    # If loading a model trained on GPU to CPU
    #checkpoint = torch.load(loadFilename, map_location=torch.device('cpu'))
    encoder_sd = checkpoint['en']
    decoder_sd = checkpoint['de']
    encoder_optimizer_sd = checkpoint['en_opt']
    decoder_optimizer_sd = checkpoint['de_opt']
    embedding_sd = checkpoint['embedding']
    voc.__dict__ = checkpoint['voc_dict']

print('Building encoder and decoder ...')
# Initialize word embeddings
embedding = nn.Embedding(voc.num_words, hidden_size)
if os.path.exists(loadFilename):
    embedding.load_state_dict(embedding_sd)
# Initialize encoder & decoder models
encoder = EncoderRNN(hidden_size, embedding, encoder_n_layers, dropout)
decoder = LuongAttnDecoderRNN(attn_model, embedding, hidden_size, voc.num_words, decoder_n_layers, dropout)
if os.path.exists(loadFilename):
    encoder.load_state_dict(encoder_sd)
    decoder.load_state_dict(decoder_sd)
# Use appropriate device
encoder = encoder.to(device)
decoder = decoder.to(device)
print('Models built and ready to go!')

# Initialize optimizers
print('Building optimizers ...')
encoder_optimizer = optim.Adam(encoder.parameters(), lr=learning_rate)
decoder_optimizer = optim.Adam(decoder.parameters(), lr=learning_rate * decoder_learning_ratio)
if os.path.exists(loadFilename):
    encoder_optimizer.load_state_dict(encoder_optimizer_sd)
    decoder_optimizer.load_state_dict(decoder_optimizer_sd)


def train(batches):
    loss = trainIters(model_name, voc, batches, encoder, decoder, encoder_optimizer, decoder_optimizer,
                embedding, save_dir, batch_size, clip)
    return loss

def testModel(inputString):
    # Initialize search module
    searcher = GreedySearchDecoder(encoder, decoder)

    # Begin chatting (uncomment and run the following line to begin)
    response = evaluateInput(inputString, encoder, decoder, searcher, voc)
    return response

def saveModel(loss):
    directory = save_dir
    if not os.path.exists(directory):
        os.makedirs(directory)
    torch.save({
        'en': encoder.state_dict(),
        'de': decoder.state_dict(),
        'en_opt': encoder_optimizer.state_dict(),
        'de_opt': decoder_optimizer.state_dict(),
        'loss': loss,
        'voc_dict': voc.__dict__,
        'embedding': embedding.state_dict()
    }, os.path.join(directory, '{}_{}.tar'.format(model_name, 'checkpoint')))
