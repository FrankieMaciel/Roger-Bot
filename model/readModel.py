import torch
import numpy as np

class ReadModel(torch.nn.Module):
   def __init__(self):
      super(ReadModel, self).__init__()

      self.encoder = torch.nn.Sequential(
         torch.nn.Linear(600, 150),
         torch.nn.ReLU(),
         torch.nn.Linear(150, 64),
         torch.nn.ReLU(),
      )

      self.decoder = torch.nn.Sequential(
         torch.nn.Linear(64, 100),
         torch.nn.ReLU(),
         torch.nn.Linear(100, 128),
         torch.nn.ReLU(),
      )
      
   def forward(self, x):
      encoder = self.encoder(x)
      decoded = self.decoder(encoder)
      return decoded