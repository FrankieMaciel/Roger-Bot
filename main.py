import os

import discord
import torch
from dotenv import load_dotenv

from CreateMsg import create as messageResult
from model.model import RogerModel

contextSize = 600
contextMessages = ''

model = RogerModel()

isExist = os.path.exists('./RogerModel.pth')
# Verifica se existe um modelo já treinado, caso contrário, inicializa o treino.
if isExist:
    model.load_state_dict(torch.load('./RogerModel.pth'))

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} está ligado.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    global contextMessages
    contextMessages += message.content + '\n'
    if len(contextMessages) > contextSize:
        contextMessages = contextMessages[-contextSize:]
    
    result = messageResult(model, contextMessages, contextSize)
    print(result)

    # await message.channel.send(messageResult(contextMessages, contextSize))

client.run(TOKEN)