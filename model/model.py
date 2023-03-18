import torch

class RogerModel(torch.nn.Module):
   def __init__(self):
      super().__init__()

      self.encoder = torch.nn.Sequential(
         torch.nn.Linear(600, 128),
         torch.nn.ReLU(),
         torch.nn.Linear(128, 64),
      )

      self.decoder = torch.nn.Sequential(
         torch.nn.Linear(9, 18),
         torch.nn.ReLU(),
         torch.nn.Linear(18, 36),
         torch.nn.ReLU(),
         torch.nn.Linear(36, 64),
         torch.nn.ReLU(),
         torch.nn.Linear(64, 128),
         torch.nn.ReLU(),
         torch.nn.Linear(128, 28 * 28),
         torch.nn.Sigmoid()
      )
      
   def forward(self, x):
      encoded = self.encoder(x)
      decoded = self.decoder(encoded)
      return decoded