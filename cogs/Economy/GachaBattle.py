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
from db import gachadatabase
import datetime
import threading


#class Battle:
    #__slots__ = ('Player1','Player2','')



class GachaBattle(commands.Cog):
    __slots__ = ('bot','battles',)
    def __init__(self,bot):
        self.bot = bot
        self.battles = {}


                


    '''
    @commands.command(name='race')
    async def race(self,ctx):
        author = ctx.message.author
        wait = 20

        msg = await ctx.send("!!!The Great Animal Race is here!!! Do '!race enter' to join! \n"
        "You have {} seconds to join!".format(wait))

        await asyncio.sleep(wait)

        cache_msg = await ctx.fetch_message(msg.id)

        reactions = cache_msg.reactions
        for reaction in reactions:
            async for user in reaction.users():
                print("Hello!")
    '''