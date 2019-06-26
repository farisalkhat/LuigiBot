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


class Economy(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="h")
    async def createecon(self,ctx,*,arg):
        lmao = gachadatabase.get_hero(arg)
        if not lmao:
            await ctx.send("Hero does not exist!")
        else:

            stats = "HP: " + str(lmao[5]) + " \n" + "ATK" + str(lmao[6]) + " \n" + "DEF" + str(lmao[7]) + " \n" + "SPD" + str(lmao[8]) + " \n"
            
            embed=discord.Embed(title=lmao[0], description="Details")
            embed.set_image(url = lmao[2])
            embed.add_field(name='Creator', value=lmao[1], inline=True)
            embed.add_field(name='Rating', value=lmao[3], inline=True)
            embed.add_field(name='Type', value=lmao[4], inline=True)
            embed.add_field(name='Moves', value='TODO', inline=True)
            embed.add_field(name='Stats', value=stats, inline=True)
            
            await ctx.send(embed=embed)
            

    
