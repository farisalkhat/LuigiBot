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
from core import jsondb

def create_embed(atitle,adescription,color):
    embed = discord.Embed(
                title = atitle,
                description = adescription,
                colour = color)
    return embed
RED = 0xc9330a
GREEN = 0x16820d
class Help(commands.Cog):

    __slots__ = ('users','items','shop','servers')
    def __init__(self,bot):
        self.bot = bot
        self.users = {}
        self.items = {}
        self.shop = {}
        self.servers = {}
    '''
    @commands.command(name="guide")
    async def guide(self,ctx):
        msg = 'Hello, this is LuigiBot! I am a general purpose bot with a plethora '
    '''


    @commands.command(name="help")
    async def help(self,ctx,*,arg=None):
        """Lists all modules for the bot."""
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        
        author = ctx.author
        if arg is None:
            embed=discord.Embed(title="Server Modules")
            list = ""
            for cog in self.bot.cogs:
                name =  cog + "\n"
                list = list + name
            embed.add_field(name = "Here are the bot's server modules. Do !help modulename to get all of their commands and a description. ",value =list)
            return await author.send(embed=embed)   
        
        cog = self.bot.get_cog(arg)
        if not cog:
            return await ctx.send("Module does not exist!")
        commands = cog.get_commands()
        embed=discord.Embed(title="Server Commands")
        i = 1
        list = ""
        for command in commands:
            name = str(i) +". **"+ command.name +'** ' + "\n"
            list = list + name
            i = i+1
        embed.add_field(name = "Here are the commands for the **{}** module.".format(arg),value =list)
        await author.send(embed=embed)   

    @commands.command(name='command')
    @commands.has_permissions(add_reactions=True,embed_links=True)
    async def command(self,ctx,*, arg):
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)


        for command in self.bot.commands:
            if command.name == arg:
                help = command.help
                if not help:
                    embed = create_embed("No description.","**{}** has no description currently.".format(command.name),RED)
                    return await ctx.send(embed=embed,delete_after=20)
                else:
                    embed = create_embed('{}'.format(command.name),help,GREEN)
                    return await ctx.send(embed=embed)



    
