
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
import tokens
import requests
from requests.exceptions import HTTPError
import operator
import json
from PIL import Image
dota_api_key = tokens.dota_api
GREEN = 0x16820d
from core import jsondb



class AmongUs(commands.Cog):
    @commands.command(name='StartAmogus')
    async def startamogus(self,ctx):
        #First, check for permissions.
        #Then, for every user listed, check if they're in the AmongUs User database. If not, then create a file for them.
        #Then, create the AmongUs session in the AmongUs Sessions database. 
        #Now, the rest of the AmongUs commands will work, until the session closes or the bot turns off.
        await ctx.send("Placeholder")

    @commands.command(name='EndAmogus')
    async def endamogus(self,ctx):
        return
    
    @commands.command(name='AddRound')
    async def addround(self,ctx):
        return
    
    @commands.command(name='ListSessions')
    async def listsessions(self,ctx):
        return

    @commands.command(name='LastSession')
    async def lastsession(self,ctx):
        return
    @commands.command(name='ShowRound')
    async def showround(self,ctx):
        return
    @commands.command(name='AmogusStats')
    async def showround(self,ctx):
        return