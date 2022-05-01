import os
import re
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from dotenv import load_dotenv
import torch
import numpy as np
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from torch.utils.data import Dataset, DataLoader
import torch.optim as optim

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
pattern = '^[Hh][Ee][Yy] [Dd][Aa][Dd],?.*'
words = [] # for future key word updates
tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')
model = GPT2LMHeadModel.from_pretrained('gpt2-medium')
device = 'cpu'
if torch.cuda.is_available():
    device = 'cuda'
model = model.to(device)


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
            with open(os.path.join('logs', '{}.txt'.format(server_name)), 'a+') as myfile:
                myfile.write('{}: {}'.format(user_name, msg))
            
        except:
            with open(os.path.join('logs', '{}.txt'.format(server_name)), 'w') as myfile:
                myfile.write('{}: {}'.format(user_name, msg))

        await message.channel.send(msg)
        return
            
client.run(TOKEN)

def choose_from_top(probs, n=5):
    ind = np.argpartition(probs, -n)[-n:]
    top_prob = probs[ind]
    top_prob = top_prob / np.sum(top_prob) # Normalize
    choice = np.random.choice(n, 1, p = top_prob)
    token_id = ind[choice][0]
    return int(token_id)

def generate_joke():
    
    # Due to time constraints we  used the first epoch
    model_path = os.path.join("trained_models", f"gpt2_medium_joker_1.pt")
    model.load_state_dict(torch.load(model_path))

    model.eval()
    if os.path.exists(jokes_output_file_path):
        os.remove(jokes_output_file_path)
        
    with torch.no_grad():
   
        for joke_idx in range(1000):
        
            joke_finished = False

            cur_ids = torch.tensor(tokenizer.encode("JOKE:")).unsqueeze(0).to(device)

            for i in range(100):
                outputs = model(cur_ids, labels=cur_ids)
                loss, logits = outputs[:2]
                softmax_logits = torch.softmax(logits[0,-1], dim=0) #Take the first(from only one in this case) batch and the last predicted embedding
                if i < 3:
                    n = 20
                else:
                    n = 3
                next_token_id = choose_from_top(softmax_logits.to('cpu').numpy(), n=n) #Randomly(from the topN probability distribution) select the next word
                cur_ids = torch.cat([cur_ids, torch.ones((1,1)).long().to(device) * next_token_id], dim = 1) # Add the last word to the running sequence

                if next_token_id in tokenizer.encode('<|endoftext|>'):
                    joke_finished = True
                    break

            
            if joke_finished:
                
                joke_num = joke_num + 1
                
                output_list = list(cur_ids.squeeze().to('cpu').numpy())
                output_text = tokenizer.decode(output_list)

               
                return f"{output_text}"
                    
