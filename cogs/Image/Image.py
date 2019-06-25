import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import youtube_dl
from itertools import cycle
import random
#import validators
import copy
import os
import re
from random import randint
import requests
import cat

GREEN = 0x16820d


class Image(commands.Cog):

    def __init__(self,bot):
        self.bot = bot


    @commands.command(name="cat")
    async def cat(self,ctx):
        """
        Generate a random cat from random.cat/meow
        """
        r = requests.get('http://aws.random.cat/meow')
        js = r.json()
        em = discord.Embed(color=GREEN)
        em.set_image(url=js['file'])
        await ctx.send(embed=em) 


    @commands.command(name="woof")
    async def woof(self,ctx):
        """
        Generate a doggo from dog.ceo
        """
        r = requests.get('https://dog.ceo/api/breeds/image/random')
        js = r.json()
        em = discord.Embed(color=GREEN)
        em.set_image(url=js['file'])
        await ctx.send(embed=em) 

        



