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

def create_embed(atitle,adescription,color):
    embed = discord.Embed(
                title = atitle,
                description = adescription,
                colour = color)
    return embed
RED = 0xc9330a
GREEN = 0x16820d
class Help(commands.Cog):

    def __init__(self,bot):
        self.bot = bot



    @commands.command(name="modules")
    async def modules(self,ctx):
        """Lists all modules for the bot."""
        embed=discord.Embed(title="Server Modules")
        i = 1
        list = ""
        for cog in self.bot.cogs:
            name = str(i) +". "+ cog + "\n"
            list = list + name
            i = i+1
        embed.add_field(name = "Here are the bot's server modules.",value =list)
        await ctx.send(embed=embed)

    @commands.command(name="cmds")
    async def cmds(self,ctx,*,arg):
        """Gets a list of commands for a module."""
        cog = self.bot.get_cog(arg)
        if not cog:
            await ctx.send("Module does not exist!")
            return
        commands = cog.get_commands()
        embed=discord.Embed(title="Server Commands")
        i = 1
        list = ""
        for command in commands:
            name = str(i) +". "+ command.name + "\n"
            list = list + name
            i = i+1
        embed.add_field(name = "Here are the commands for the **{}** module.".format(arg),value =list)
        await ctx.send(embed=embed)
    @commands.command()
    @commands.has_permissions(add_reactions=True,embed_links=True)
    async def help(self,ctx,*, arg):
        for command in self.bot.commands:
            if command.name == arg:
                help = command.help
                if not help:
                    embed = create_embed("No description.","**{}** has no description currently.".format(command.name),RED)
                    await ctx.send(embed=embed,delete_after=20)
                else:
                    embed = create_embed('{}'.format(command.name),help,GREEN)
                    await ctx.send(embed=embed)
