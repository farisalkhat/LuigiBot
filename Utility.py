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

class Utility:
    def __init__(self,client):
        self.client = client'

    @commands.command(pass_context=True)
    async def whosplaying(self,ctx):
        """Shows a list of users who are playing the specified game."""

    @commands.command(pass_context=True)
    async def inrole(self,ctx):
        """Lists every person from the specified role on this server.
        You can use role ID, role name."""

    @commands.command(pass_context=True)
    async def roles(self,ctx):
        """List roles on this server or roles of a user if specified. Paginated, 20 roles per page."""

    @commands.command(pass_context=True)
    async def savechat(self,ctx):
        """Saves a number of messages to a text file and sends it to you. .savechat 150"""

    @commands.command(pass_context=True)
    async def calculate(self,ctx):
        "Evaluate a mathematical expression."""

    @commands.command(pass_context=True)
    async def remind(self,ctx):
        """Sends a message to you or a channel after certain amount of time (max 2 months).
        First parameter is me/here/'channelname'.
        Second parameter is time in a descending order (mo>w>d>h>m) example: 1w5d3h10m.
        Third parameter is a (multiword) message."""
        #Extra commands: remindlist, reminddel, remindtemplate
        
    @commands.command(pass_context=True)
    async def convert(self,ctx):
        """Convert quantities.
        Use .convertlist to see supported dimensions and currencies."""
        #Extra commands: convertlist

        
    @commands.command(pass_context=True)
    async def togethertube(self,ctx):
        """Creates a new room on https://togethertube.com and shows the link in the chat."""
        
    @commands.command(pass_context=True)
    async def KH(self,ctx):
        
    @commands.command(pass_context=True)
    async def KH(self,ctx):
        
        

        
def setup(client):
    client.add_cog(Utility(client))
