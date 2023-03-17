import os

import discord
from dotenv import load_dotenv

from CreateMsg import create as messageResult

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

    await message.channel.send(messageResult(message))

client.run(TOKEN)