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
from discord.utils import get


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='luigibot',aliases=['Luigibot','LuigiBot','serverinfo'])
    async def serverinfo(self,ctx):
        msg = '''LuigiBot is a general purpose, self hosting bot. It was created by Faris Al-khatahtbeh.
If you'd like to see more from Faris, here is his GitHub: https://github.com/farisalkhat?tab=repositories

Here is the LuigiBot documentation, meant to easily setup LuigiBot and understand how all of the commands work: https://docs.google.com/document/d/17XkK43XTfauNpPQ7Hl4PxTw5Q4f2dwAuRE3rmYC87eI/edit?usp=sharing
        '''
        await ctx.send(msg,delete_after=30)

    '''
    @commands.command(name='setprofile')
    async def setprofile(self,ctx,*,arg):

    @commands.command(name='setosu')
    async def setosu(self,ctx,*,arg):

    @commands.command(name='viewprofile')
    async def viewprofile(self,ctx, member:discord.Member=None):
    
    @commands.command(name='viewosu')
    async def viewosu(self,ctx, member:discord.Member=None):

    @commands.command(name='setdesc')
    async def setdesc(self,ctx,*,arg):

    
    @commands.command(name='addtwitch')
    async def addtwitch(self,ctx,*,arg):

    @commands.command(name='deltwitch')
    async def deltwitch(self,ctx,*,arg):

    @commands.command(name='viewtwitch')
    async def viewtwitch(self,ctx,*,arg):

    
    '''




    