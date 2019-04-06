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
                colour = 0x16820d)
    return embed

class Fun:
    def __init__(self,client):
        self.client = client

    @commands.command(pass_context=True)
    async def cat(self,ctx):
        args = ctx.message.content.split(' ')
        if len(args)>1:
            embed = create_embed('!cat does not need an input','Just type in !cat.')
            await self.client.say(embed=embed)
            return
        imgList = os.listdir("./Images") # Creates a list of filenames from your folder

        imgString = random.choice(imgList) # Selects a random element from the list

        path = "./Images/" + imgString # Creates a string for the path to the file

        await self.client.send_file(ctx.message.channel, path) # Sends the image in the channel the command was used
        
    @commands.command(pass_context=True)
    async def avi(self,ctx):
        author = ctx.message.author
        server = ctx.message.server
        args = ctx.message.content.split(' ')
        if len(args)==1:
            userid = author.id
            user = server.get_member(userid)
        elif len(args)==2:
            if not ctx.message.mentions:
                embed = create_embed('!avi error','Could not find user.')
                await self.client.say(embed=embed)
                return
            userid = ctx.message.mentions[0].id
            user = server.get_member(userid)
        else:
            embed = create_embed('!avi error','Incorrect input. Only takes 0 or 1 arguments.')
            await self.client.say(embed=embed)
            return

        pfp = user.avatar_url
        embed=discord.Embed(title='' , color=0x16820d)
        embed.set_image(url=(pfp))
        await self.client.say(embed=embed)




def setup(client):
    client.add_cog(Fun(client))
