# from src.functions.generateMessage import create
from ..RogerModel.Roger import run, learn
import asyncio

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
emojis = ['👍', '👎']

lastAutor = None
lastAutorMessages = []
messages = ['']

def addMessage(message):
    global lastAutor
    global lastAutorMessages
    global messages

    if message.author.name != lastAutor and lastAutor != None:
        messages.append('<br>'.join(lastAutorMessages))
        lastAutorMessages = []
        lastAutorMessages.append(message.content)
        lastAutor = message.author.name
        learn(messages[len(messages) - 2], messages[len(messages) - 1])
    else:
        lastAutorMessages.append(message.content)


def escrever_para_arquivo(pares, nome_arquivo):
    with open(nome_arquivo, "a") as myfile:
        content = pares[0] + ' ' + str(pares[1]) + '\n'
        print(content)
        myfile.write(content)

def addDataSet(message):

    line = [message.content, 0]
    if message.reactions[0].count > 1:
        line[1] = 1
    elif message.reactions[1].count > 1:
        line[1] = -1
    
    mydir = os.path.join('src', 'RogerModel', 'data', 'finetune.txt')
    escrever_para_arquivo(line, mydir)

@client.event
async def on_ready():
    print(f'{client.user} está ligado.')

lastMessages = ['Oi']

@client.event
async def on_message(message):
    # print(message.channel.type)
    global lastAutor
    global lastMessages
    if message.author == client.user:
        # for emoji in emojis:
        #     await message.add_reaction(emoji)
        # print(message.reactions[0].count)
        # messages.append(message)
        # if len(messages) > 2:
        #     messages.pop(0)
        # if messages[0] != '':
        #     addDataSet(messages[0])
        return
    
    if str(message.channel.type) != 'private':
        # Normal chatbot commands of Roger
        havePrefix = False
        for prefix in prefixes:
            if prefix in message.content.lower(): havePrefix = True
        
        if havePrefix: 
            result = run(message.content)
            if len(result) > 0:
                async with message.channel.typing():
                    for index, r in enumerate(result):
                        if r != '':
                            if index != 0:
                                await message.channel.send(r)
                            else:
                                await message.reply(r, mention_author=False)
                            await asyncio.sleep(1)
                    
        else:
            addMessage(message)

    else:
        result = run(message.content)

        if len(result) > 0:
            # lastAutor = 'Roger'
            async with message.channel.typing():
            # do expensive stuff here
                for r in result:
                    if r != '':
                        await message.channel.send(r)
                        await asyncio.sleep(1)
            # addMessage(message)
            # message.content = result
            # message.author.name = 'Roger'
            # addMessage(message)
            # lastAutor = 'Roger'

    if len(messages) > 5:
        messages.pop(0)

    # System commands of Roger
    haveCommandPrefix = False
    for prefix in CommandPrefixes:
        if prefix in message.content.lower(): haveCommandPrefix = True
    
    if not haveCommandPrefix: return

    if "--Reset" in message.content: lastAutor = 'Roger'

    if "--parar" in message.content: sys.exit()

client.run(TOKEN)