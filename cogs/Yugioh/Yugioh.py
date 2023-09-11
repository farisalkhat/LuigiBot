import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from itertools import cycle
import random
import copy
import os
import re
from random import randint
import requests
import urllib.parse
#from tzwhere import tzwhere
import tokens
#import pyosu
from core import jsondb
import json

class Yugioh(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.users = {}
        self.items = {}
        self.shop = {}
        self.servers = {}
    
    @commands.command(name="ygologin")
    @commands.dm_only()
    async def ygologin(self,ctx):
        await jsondb.load_users(self)

        await ctx.channel.send("Insert your login info below, separated by a comma.")
        message = await self.bot.wait_for('message')
        if message.content:

            logininfo = message.content.split(';')
            if len(logininfo)!=2:
                await ctx.channel.send("Incorrect login info.")
                return
            else:
                data = {
                    "email":logininfo[0],
                    "password":logininfo[1]
                }


                res = requests.post("http://127.0.0.1:8080/api/loginyugiohdiscord",json=data)
                print(res.status_code)
                if res.status_code==201:



                    print(res.status_code)
                    tokenjson = json.loads(res.text)
                    token = tokenjson['token']
                    authorid = message.author.id
                    self.users[authorid]['YGOProfile']['Token'] = token
                    
                    #TODO: ONCE YOU SUCCESSFULLY LOGIN,
                await ctx.channel.send(data)



            
        