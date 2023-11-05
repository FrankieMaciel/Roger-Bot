from Project.config.bot import save_dir, SOS_token ,EOS_token, device, hidden_size, learning_rate, decoder_n_layers, decoder_learning_ratio, dropout, encoder_n_layers, attn_model, MAX_LENGTH, batch_size, clip
from Project.models.decoder import LuongAttnDecoderRNN
from Project.models.encoder import EncoderRNN
from Project.train.train import trainIters
from Project.vocab.create import getVocab
from Project.data.process import processLines
from Project.vocab.tokenizer import indexesFromSentence
from Project.vocab.normalize import normalizeString
from Project.vocab.format import format_phrase

from torch import optim
import torch.nn as nn
import torch
import os

class chatbot(nn.Module):

    def __init__(self, name, dataDir):
        super(chatbot, self).__init__()

        self.name = name
        self.dataDir = dataDir
        self.voc = getVocab(self.name, self.dataDir)

        self.embedding = nn.Embedding(self.voc.num_words, hidden_size)

        self.encoder = EncoderRNN(
            hidden_size, 
            self.embedding, 
            encoder_n_layers, 
            dropout
        )
        self.decoder = LuongAttnDecoderRNN(
            attn_model, 
            self.embedding, 
            hidden_size, 
            self.voc.num_words, 
            decoder_n_layers, 
            dropout
        )
        self.encoder_optimizer = optim.Adam(
            self.encoder.parameters(), 
            lr=learning_rate
        )
        self.decoder_optimizer = optim.Adam(
            self.decoder.parameters(),
            lr=learning_rate * decoder_learning_ratio
        )
        # Use appropriate device
        self.encoder = self.encoder.to(device)
        self.decoder = self.decoder.to(device)

        self.train()

    def forward(self, input_seq, input_len, max_len):
        
        encoder_outputs, encoder_hidden = self.encoder(input_seq, input_len)
        decoder_hidden = encoder_hidden[:self.decoder.n_layers]
        
        decoder_input = torch.ones(1, 1, device=device, dtype=torch.long) * SOS_token

        all_tokens = torch.zeros([0], device=device, dtype=torch.long)
        all_scores = torch.zeros([0], device=device)

        for _ in range(max_len):
            decoder_output, decoder_hidden = self.decoder(
                decoder_input, 
                decoder_hidden, 
                encoder_outputs
            )
            decoder_scores, decoder_input = torch.max(decoder_output, dim=1)

            if (decoder_input == EOS_token): break

            all_tokens = torch.cat((all_tokens, decoder_input), dim=0)
            all_scores = torch.cat((all_scores, decoder_scores), dim=0)

            decoder_input = torch.unsqueeze(decoder_input, 0)

        return all_tokens, all_scores
    
    def train(self):
        loadFilename = os.path.join(
            save_dir, 
            '{}_Model.tar'.format(self.name)
        )

        if os.path.exists(loadFilename): 
            print('Trainning canceled! A checkpoint already exist.')
            self.loadModel()
            return

        linhas_separadas = processLines(self.dataDir)
        # batches = [tokenize([line], self.voc) for line in linhas_separadas]
        finalLoss = trainIters(
            self.voc,
            linhas_separadas,
            self.encoder,
            self.decoder,
            self.encoder_optimizer,
            self.decoder_optimizer,
            self.embedding,
            batch_size,
            clip
            )
        self.saveModel(finalLoss, self.name)

    def saveModel(self, loss, name):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        torch.save({
            'en': self.encoder.state_dict(),
            'de': self.decoder.state_dict(),
            'en_opt': self.encoder_optimizer.state_dict(),
            'de_opt': self.decoder_optimizer.state_dict(),
            'loss': loss,
            'voc_dict': self.voc.__dict__,
            'embedding': self.embedding.state_dict()
        }, os.path.join(save_dir, '{}_Model.tar'.format(name)))
    
    def loadModel(self):

        loadFilename = os.path.join(
            save_dir, 
            '{}_Model.tar'.format(self.name)
        )

        if os.path.exists(loadFilename):
            # If loading on same machine the model was trained on
            checkpoint = torch.load(loadFilename)

            self.encoder.load_state_dict(checkpoint['en'])
            self.decoder.load_state_dict(checkpoint['de'])
            self.encoder_optimizer.load_state_dict(checkpoint['en_opt'])
            self.decoder_optimizer.load_state_dict(checkpoint['de_opt'])
            self.embedding.load_state_dict(checkpoint['embedding'])
            self.voc.__dict__ = checkpoint['voc_dict']
    
    def run(self, sentence):

        normalizedText = normalizeString(sentence)

        indexes_batch = [indexesFromSentence(self.voc, normalizedText)]
        lengths = torch.tensor([len(indexes) for indexes in indexes_batch])
        input_batch = torch.LongTensor(indexes_batch).transpose(0, 1)
        input_batch = input_batch.to(device)
        lengths = lengths.to("cpu")

        tokens, scores = self.forward(input_batch, lengths, MAX_LENGTH)
        
        decoded_words = [self.voc.index2word[token.item()] for token in tokens]
        response = format_phrase(decoded_words)

        return response



