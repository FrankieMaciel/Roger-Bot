import os

import matplotlib.pyplot as plt
from dotenv import load_dotenv
import discord
import torch

from CreateMsg import create as messageResult
from model.readModel import ReadModel

contextSize = 600
contextMessages = ''

losses = []

model = ReadModel()

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
    
    isToGenerate = False
    if "!Roger " in message.content: isToGenerate = True

    if isToGenerate and '--info' in message.content:
        plt.plot(losses)
        plt.title('Nivel de aprendizado')
        plt.xlabel('Por mensagem')
        plt.ylabel('Quão errado')
        plt.savefig('grafico.png')

        with open('grafico.png', 'rb') as imagem:
            await message.channel.send('//Gráfico//', file=discord.File(imagem))
        
        isToGenerate = False

    try:
        result, loss = messageResult(model, contextMessages, contextSize, isToGenerate)
        losses.append(loss)
        if len(losses) > 50:
            losses.pop(0)
        # print(result)
        if isToGenerate:
            await message.channel.send(result)
        print(losses)
    except Exception as e:
        await message.channel.send('//Error//: ' + str(e))


client.run(TOKEN)