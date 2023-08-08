import torch
import os

# Default word tokens
PAD_token = 0  # Used for padding short sentences
SOS_token = 1  # Start-of-sentence token
EOS_token = 102  # End-of-sentence token
DEL_token = 3  # End-of-sentence token

USE_CUDA = torch.cuda.is_available()
device = torch.device("cuda" if USE_CUDA else "cpu")

# Configure model
model_name = 'Roger'
attn_model = 'dot' # dot, general, concat
hidden_size = 512
encoder_n_layers = 2
decoder_n_layers = 2
dropout = 0.1
batch_size = 1

MAX_LENGTH = 200  # Maximum sentence length to consider

MIN_COUNT = 0    # Minimum word count threshold for trimming

# Configure training/optimization
clip = 50.0
teacher_forcing_ratio = 1.0
learning_rate = 0.0001
decoder_learning_ratio = 5.0
n_iteration = 4000
print_every = 1
save_every = 500

save_dir = os.path.join('src','RogerModel',"saves")