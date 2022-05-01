import os
import re
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
pattern = '^[Hh][Ee][Yy] [Dd][Aa][Dd],?.*'
words = [] # for future key word updates

description = ''

client = discord.Client()

@client.event
async def on_ready():
    print("Daddy is here")

@client.event
async def on_message(message):
    server_name = message.guild.name
    user_name = message.author

    if user_name == client.user:
        return

    elif re.search('^[Mm][Oo]([Mm]|[Tt][Hh][Ee][Rr])', user_name):
        await message.channel.send('Nothing, dear.')
        return

    if re.search(pattern, message.content):
        # TODO forward pass to generate joke here
        msg = generate_joke()
        try:
            with open("logs/{}.txt".format(server_name), "a+") as myfile:
                myfile.write("{}: {}".format(user_name, msg))
            
        except:
            with open("logs/{}.txt".format(server_name), "w") as myfile:
                myfile.write("{}: {}".format(user_name, msg))

        await message.channel.send(msg)
        return
            
client.run(TOKEN)