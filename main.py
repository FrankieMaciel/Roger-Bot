import os

import discord
from dotenv import load_dotenv

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

    if message.content == 'teste':
        await message.channel.send('Testado!')

client.run(TOKEN)