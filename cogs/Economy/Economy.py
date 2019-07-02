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
from db import database
from core.helper import permission


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
        
        if permission(ctx.message.guild.id,ctx.message.channel.id) is False:
            return await ctx.send("This channel is not allowed to have bot commands.",delete_after=10)
        if not author.guild_permissions.administrator:
            await ctx.send('Sorry good sir, you do not have permission to create an economy!',delete_after=20)
            return

        
        econ_enabled = database.get_economy(guildid)
        if not econ_enabled:
            await ctx.send("Creating economy..",delete_after=20)
            database.create_economy([guildid,'Enabled'])

            for member in memberslist:
                database.add_econ_member([guildid,member.id,25])

            await ctx.send("Economy created!",delete_after=20)

        elif econ_enabled[1] == 'Enabled':
            await ctx.send('Economy already enabled for this server!')
            return
    
    @commands.command(name="balance")
    async def balance(self,ctx):
        authorid = ctx.message.author.id
        guildid = ctx.message.guild.id
        if permission(ctx.message.guild.id,ctx.message.channel.id) is False:
            return await ctx.send("This channel is not allowed to have bot commands.",delete_after=10)
        balance = database.get_balance([guildid,authorid])
        await ctx.send("**{}**, you currently have **{} LuigiCoins!**".format(ctx.message.author,balance[2]))



    

            
