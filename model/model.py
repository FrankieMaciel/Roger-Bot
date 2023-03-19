import torch

class RogerModel(torch.nn.Module):
   def __init__(self):
      super(RogerModel, self).__init__()

      self.encoder = torch.nn.Sequential(
         torch.nn.Linear(600, 128),
         torch.nn.ReLU(),
         torch.nn.Linear(128, 64),
      )

      self.decoder = torch.nn.Sequential(
         torch.nn.Linear(64, 82),
         torch.nn.ReLU(),
         torch.nn.Linear(82, 127),
         torch.nn.Sigmoid()
      )
      
   def forward(self, x):
      encoded = self.encoder(x)
      decoded = self.decoder(encoded)
      return decoded