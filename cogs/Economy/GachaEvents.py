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


class GachaEvents(commands.Cog):
    __slots__ = ('bot','tools')
    def __init__(self,bot):
        self.bot = bot
        self.tools = {}


    '''
    @commands.Cog.listener
    async def on_message(self,message):
        print('lmao!')
    '''

    @commands.Cog.listener()
    async def on_member_update(self,before, after):
        if str(before.status) == "offline":
            if str(after.status) == "online":
                print("{} is now {}. Tracking time online.".format(after.name,after.status))

        if after.voice:
            print("{} is in a voice channel.".format(after.name))



        #time = datetime.datetime.now().time
        #user = self.id


        '''
        await bot.wait_until_ready()
        msgs = cycle(status)

        while not bot.is_closed():
            current_status = next(msgs)
            activity = discord.Game(name=current_status)
            await bot.change_presence(status=discord.Status.idle, activity=activity)
            await asyncio.sleep(60*60)
        '''