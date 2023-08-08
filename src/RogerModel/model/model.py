import torch
import torch.nn as nn
import numpy as np
from src.RogerModel.config import SOS_token, device, EOS_token

def valor_randomico_do_tensor(tensor):
    # Converte o tensor para um array numpy
    array_tensor = np.array(tensor)
    # Obtém a forma (shape) do array
    shape = array_tensor.shape
    # Gera uma tupla de índices aleatórios dentro do shape do array
    random_indices = tuple(np.random.randint(0, dim) for dim in shape)
    # Obtém o valor aleatório do tensor/array usando os índices gerados
    valor_randomico = array_tensor[random_indices]
    
    return valor_randomico

class GreedySearchDecoder(nn.Module):
    def __init__(self, encoder, decoder):
        super(GreedySearchDecoder, self).__init__()
        self.encoder = encoder
        self.decoder = decoder

    def forward(self, input_seq, input_length, max_length, K=1):
        # Forward input through encoder model
        encoder_outputs, encoder_hidden = self.encoder(input_seq, input_length)
        # Prepare encoder's final hidden layer to be first hidden input to the decoder
        decoder_hidden = encoder_hidden[:self.decoder.n_layers]
        # Initialize decoder input with SOS_token
        newDecoderInput = torch.ones(1, 1, device=device, dtype=torch.long) * SOS_token
        # Initialize tensors to append decoded words to
        all_tokens = torch.zeros([0], device=device, dtype=torch.long)
        all_scores = torch.zeros([0], device=device)
        # Iteratively decode one word token at a time
        for _ in range(max_length):
            # Forward pass through decoder
            decoder_output, decoder_hidden = self.decoder(newDecoderInput, decoder_hidden, encoder_outputs)
            # Obtain most likely word token and its softmax score
            decoder_scores, decoder_input = torch.topk(decoder_output, K, dim=1)
            newDecoderInput = valor_randomico_do_tensor(decoder_input)
            newDecoderInput = torch.tensor([newDecoderInput])
            # Record token and score
            all_tokens = torch.cat((all_tokens, newDecoderInput), dim=0)

            if (newDecoderInput == EOS_token):
                break
            
            # Prepare current token to be next decoder input (add a dimension)
            newDecoderInput = torch.unsqueeze(newDecoderInput, 0)
        # Return collections of word tokens and scores
        return all_tokens