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
    





    @commands.command(name="createeconomy")
    async def createeconomy(self,ctx):
        """
        Sets up the economy for the server.
        """
        guildid = ctx.message.guild.id
        memberslist = ctx.message.guild.members
        author = ctx.message.author
        

        if not author.guild_permissions.administrator:
            await ctx.send('Sorry good sir, you do not have permission to create an economy!',delete_after=20)
            return

        
        econ_enabled = gachadatabase.get_economy(guildid)
        if not econ_enabled:
            await ctx.send("Creating economy..",delete_after=20)
            gachadatabase.create_economy([guildid,'Enabled'])

            for member in memberslist:
                gachadatabase.add_econ_member([guildid,member.id,25])

            await ctx.send("Economy created!",delete_after=20)

        elif econ_enabled[1] == 'Enabled':
            await ctx.send('Economy already enabled for this server!')
            return
    
    @commands.command(name="balance")
    async def balance(self,ctx):
        authorid = ctx.message.author.id
        guildid = ctx.message.guild.id

        balance = gachadatabase.get_balance([guildid,authorid])
        await ctx.send("**{}**, you currently have **{} LuigiCoins!**".format(ctx.message.author,balance[2]))



    

            
