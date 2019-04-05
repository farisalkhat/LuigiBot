import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import youtube_dl
from itertools import cycle
import random
import validators
import copy

import os
'''
@client.command()
async def ping():
    await client.say('Pong!') #say can only be used in client commands, where say is similar to send_message, except it knows what channel to send the message to. 
'''
#Echo
def create_embed(atitle,adescription):
    embed = discord.Embed(
                title = atitle,
                description = adescription,
                colour = discord.Colour.blue())
    return embed

class Searches:
    def __init__(self,client):
        self.client = client
        

        
def setup(client):
    client.add_cog(Searches(client))
