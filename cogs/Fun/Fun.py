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
from db import database

eightballkey = ['It is certain.','As I see it, yes.','Reply hazy, try again.',"Don't count on it.",'It is decidedly so.',
                'Most likely.','Ask again later.','My reply is no.','Without a doubt.','Outlook good.',
                'Better not tell you now.','My sources say no.','Yes - definitely.','Yes.','Cannot predict now.',
                'Outlook not so good.','You may rely on it.','Signs point to yes.','Concentrate and ask again.','Very doubtful.']
RED = 0xc9330a
GREEN = 0x16820d



def create_embed(atitle,adescription,color):
    embed = discord.Embed(
                title = atitle,
                description = adescription,
                colour = color)
    return embed

class Fun(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.config= database.get_configs()
        self.cooldown = {}




    

    @commands.group(pass_context=True)
    async def race(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("You need to do something, sir.")
    
    @commands.group(pass_context=True)
    async def setrace(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("You need to do something, sir.")

    @setrace.command(name='create')
    async def create(self,ctx):
        serverid= ctx.message.guild.id
        author = ctx.message.author
        if not author.guild_permissions.administrator:
            return await ctx.send("You do not have permission to do this.")
        
        config = database.get_config(serverid)
        if config:
            return await ctx.send("You already have a configuration.")
        database.create_config(serverid)
        await ctx.send("Configuration created!")

    @setrace.command(name='prize')
    async def set_prize(self,ctx,minimum: int, maximum:int):
        author = ctx.message.author
        if not author.guild_permissions.administrator:
            return await ctx.send("You do not have permission to do this.")
        if minimum > maximum:
            return await ctx.send("The minimum is greater than the maximum. Are you dumb?")
        server = ctx.message.guild.id
        settings = database.get_config(server)
        if not settings:
            return await ctx.send("You do not have any race configutarions set. Try to create configs first.")

        database.set_prize([server,minimum,maximum])
        await ctx.send("The minimum and maximum prize range for races have been set.")




    @race.command(name='start')
    async def start_race(self,ctx):
        author = ctx.message.author
        serverid= ctx.message.guild.id
        race_configs = database.get_config(serverid)

        if not race_configs:
            return await ctx.send("This server has no configurations. Try to create them first.")

        wait = race_configs[4]
        prize = randint(race_configs[1],race_configs[2])
        cost = race_configs[3]

        msg = await ctx.send("!!!The Great Animal Race is here!!! Do '!race enter' to join! \n"
        "You have {} seconds to join!".format(wait))

        emojis = ctx.message.guild.emojis
        
        emoji1= ''
        emoji2= ''
        emoji3= ''
        emoji4= ''


        for emoji in emojis:
            if emoji.name == 'cowboy':
                emoji1 = emoji
            if emoji.name == 'kissing_heart':
                emoji2 = emoji
            if emoji.name == 'rage':
                emoji3 = emoji
            if emoji.name == 'poop':
                emoji4 = emoji



        await msg.add_reaction(emoji1)
        await msg.add_reaction(emoji2)
        await msg.add_reaction(emoji3)
        await msg.add_reaction(emoji4)


        await asyncio.sleep(wait)

        cache_msg = await ctx.fetch_message(msg.id)

        user_list = []
        reactions = cache_msg.reactions
        for reaction in reactions:
            async for user in reaction.users():
                user_list.append([user,reaction])
        
        print(user_list)
                







    @commands.command(name="8ball")
    async def ball(self,ctx, *, arg):
        N = randint(0,19)
        await ctx.send(eightballkey[N])

    @commands.command(name="choose")
    async def choose(self,ctx,*,arg):
        choices = arg.split(';')
        N = randint(0,len(choices)-1)
        await ctx.send(choices[N])

    @commands.command(name="flip")
    async def flip(self,ctx):
        """Flips a coin."""
        N = randint(1,2)
        if N == 1:
            await ctx.send("_**Heads.**_")
        else:
            await ctx.send("_**Tails.**_")

    @commands.command(name="roll")
    async def roll(self,ctx,left: int = 1,right:int = 100):
        """
        Randomly generate a number between two given ranges. By default, it rolls between 1-100.
        You can provide two different integers to randomly select a number between them.

        Example:
        !roll
        !roll 1000 2000
        """

        if left > right:
            embed = create_embed('roll error: Invalid left range', 'The left range is greater than the right range.',RED)
            await ctx.send(embed=embed)
            return

        N = randint(left,right)
        await ctx.send(N)

    @commands.command(name="roll3")
    async def roll3(self,ctx):
        """
        Roll 3 6 sided dies.
        """


        N1 = randint(1,6)
        N2 = randint(1,6)
        N3 = randint(1,6)

        N = str(N1) + " " + str(N2) + " "  + str(N3)
        await ctx.send(N)




