import os

import discord
from dotenv import load_dotenv

from CreateMsg import create as messageResult

contextSize = 600
contextMessages = ''

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

    await message.channel.send(messageResult(contextMessages, contextSize))

client.run(TOKEN)