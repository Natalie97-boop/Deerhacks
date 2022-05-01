import os
import re
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
pattern = '^[Hh][Ee][Yy] [Dd][Aa][Dd],?.*'
words = []

description = ''

client = discord.Client()

@client.event
async def on_ready():
    print("Daddy is here")

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if re.search(pattern, message.content):
        msg = generate_joke()
        await message.channel.send(msg)
            
client.run(TOKEN)