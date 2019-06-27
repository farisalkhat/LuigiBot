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



class Gacha(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='rhero')
    async def rhero(self,ctx,*,arg):
        author = ctx.message.author
        SERVERID = str(ctx.message.guild.id)

        if not author.guild_permissions.administrator:
            await ctx.send('Sorry good sir, you do not have permission to create an economy!',delete_after=20)
            return
        lmao = gachadatabase.get_hero([arg,ctx.message.guild.id])
        if not lmao:
            await ctx.send("Hero does not exist!")
        else:
            HERONAME = lmao[1]
            gachadatabase.remove_hero([SERVERID,HERONAME])
            await ctx.send("Hero has been deleted!")


    @commands.command(name='gcreate')
    async def gcreate(self,ctx,*,arg):
        SERVERID = str(ctx.message.guild.id)
        gacha = arg.split(';')
        author = ctx.message.author

        if not author.guild_permissions.administrator:
            await ctx.send('Sorry good sir, you do not have permission to create an economy!',delete_after=20)
            return

        if len(arg)<11:
            await ctx.send('Sorry, you need to provide at least 11 arguments to create a new gacha hero.')
            return

        gachas = gacha[:5]
        gachaints = gacha[5:11]
        gachas.insert(0,SERVERID)

        T2 = [int(x) for x in gachaints]
        for intboy in T2:
            gachas.append(intboy)
        
        gachadatabase.create_hero(gachas)
        await ctx.send("**{}** has created the hero: **{}**".format(ctx.message.author,gachas[1]))

    @commands.command(name="hero",aliases=['h'])
    async def get_hero_data(self,ctx,*,arg):
        lmao = gachadatabase.get_hero([arg,ctx.message.guild.id])
        if not lmao:
            await ctx.send("Hero does not exist!")
        else:
            stats = "HP: " + str(lmao[7]) + " \n" + "ATK: " + str(lmao[8]) + " \n" + "DEF: " + str(lmao[9]) + " \n" + "SPDEF:"+ str(lmao[10])+ " \n" + "SPD: " + str(lmao[11]) + " \n"
            embed=discord.Embed(title=lmao[1], description=lmao[3])
            embed.set_image(url = lmao[2])
            embed.add_field(name='Creator', value=lmao[4], inline=True)
            embed.add_field(name='Rating', value=lmao[6], inline=True)
            embed.add_field(name='Type', value=lmao[5], inline=True)
            embed.add_field(name='Moves', value='TODO', inline=True)
            embed.add_field(name='Stats', value=stats, inline=True)
            await ctx.send(embed=embed)