# from src.functions.generateMessage import create
from ..RogerModel.Roger import run

from dotenv import load_dotenv
import discord
import sys
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

prefixes = ['roger ', ' roger']
CommandPrefixes = ['!roger ', ' !roger']

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} está ligado.')

@client.event
async def on_message(message):
    print(message.channel.type)
    if message.author == client.user:
        return
    
    if str(message.channel.type) != 'private':
        # Normal chatbot commands of Roger
        havePrefix = False
        for prefix in prefixes:
            if prefix in message.content.lower(): havePrefix = True
        
        if not havePrefix: return

    prompt = message.content.replace('roger',"")
    prompt = prompt.replace('Roger',"")

    print(prompt)
    result = run(prompt)
    print(result)
    if result != '':
        await message.channel.send(result);

    # System commands of Roger
    haveCommandPrefix = False
    for prefix in CommandPrefixes:
        if prefix in message.content.lower(): haveCommandPrefix = True
    
    if not haveCommandPrefix: return

    if "--parar" in message.content: sys.exit()

client.run(TOKEN)