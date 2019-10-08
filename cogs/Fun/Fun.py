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
from core import jsondb

eightballkey = ['It is certain.','As I see it, yes.','Reply hazy, try again.',"Don't count on it.",'It is decidedly so.',
                'Most likely.','Ask again later.','My reply is no.','Without a doubt.','Outlook good.',
                'Better not tell you now.','My sources say no.','Yes - definitely.','Yes.','Cannot predict now.',
                'Outlook not so good.','You may rely on it.','Signs point to yes.','Concentrate and ask again.','Very doubtful.']
RED = 0xc9330a
GREEN = 0x16820d

import json


def create_embed(atitle,adescription,color):
    embed = discord.Embed(
                title = atitle,
                description = adescription,
                colour = color)
    return embed

class Fun(commands.Cog):
    __slots__ = ('users','items','shop','servers','poll')

        
    def __init__(self,bot):
        self.bot = bot
        self.config= database.get_configs()
        self.cooldown = {}
        self.poll = {}
        self.pollstats={}
        self.pollvoters={}
        self.users = {}
        self.items = {}
        self.shop = {}
        self.servers = {}


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
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        N = randint(0,19)
        await ctx.send(eightballkey[N])

    @commands.command(name="choose")
    async def choose(self,ctx,*,arg):
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        choices = arg.split(';')
        N = randint(0,len(choices)-1)
        await ctx.send(choices[N])

    @commands.command(name="flip")
    async def flip(self,ctx):
        """Flips a coin."""
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
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


        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)

            
        authorid = str(ctx.author.id)

        if left > right:
            embed = create_embed('roll error: Invalid range inputs', 'You must input two ranges, and the first range must be smaller.',RED)
            await ctx.send(embed=embed)
            return

        await jsondb.load_users(self)
        await jsondb.load_items(self)
        await jsondb.load_shop(self)

        try:
            if self.users[authorid]['Rigged']== 1:
                N = right
                self.users[authorid]['Rigged']=0
                await jsondb.save_users(self)
                return await ctx.send(N)
            else:
                N = randint(left,right)
                return await ctx.send(N)
        except KeyError:
            N = randint(left,right)
            return await ctx.send(N)

        

    @commands.command(name="roll3")
    async def roll3(self,ctx):
        """
        Roll 3 6 sided dies.
        """


        N1 = randint(1,6)
        N2 = randint(1,6)
        N3 = randint(1,6)
        authorid = str(ctx.author.id)

        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)

        await jsondb.load_users(self)
        await jsondb.load_items(self)
        await jsondb.load_shop(self)

        try:
            if self.users[authorid]['Rigged']== 1:
                N1 = 6
                N2 = 6
                N3 = 6
                N = str(N1) + " " + str(N2) + " "  + str(N3)
                self.users[authorid]['Rigged']=0
                jsondb.save_users(self)
                return await ctx.send(N)
            else:
                N1 = randint(1,6)
                N2 = randint(1,6)
                N3 = randint(1,6)
                N = str(N1) + " " + str(N2) + " "  + str(N3)
                return await ctx.send(N)
        except KeyError:
            N1 = randint(1,6)
            N2 = randint(1,6)
            N3 = randint(1,6)
            N = str(N1) + " " + str(N2) + " "  + str(N3)
            return await ctx.send(N)




        

    @commands.command(name='poll')
    async def start_poll(self,ctx,*,arg):
        '''
        Creates a poll on the server. Arguments are semicolon separated. 

        Usage:
        !poll question;choice1;choice2;choice3;choice4
        '''


        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        
        
        args = arg.split(';')
        serverid = ctx.message.guild.id
        try:
            if self.poll[serverid] is not None:
                return await ctx.send("There is already a poll going on right now. Please wait for that one to finish.")
        except KeyError:
            if len(args)>5 or len(args)<3:
                return await ctx.send("**{}**, you need to provide at least 1 question and 2 options!")
            results = []
            result = len(args)-1
            while result!=0:
                results.append(0)
                result = result-1
            self.poll[serverid] = args
            self.pollstats[serverid] = results
            self.pollvoters[serverid] = []
            print(self.pollstats[serverid])
            await ctx.send("**{}** has created a new poll, the question is..".format(ctx.author))
            embed = poll(self.poll[serverid],self.pollstats[serverid])
            await ctx.send(embed=embed)

    
    @commands.command(name='pollstats')
    async def poll_stats(self,ctx):
        '''
        Get the current stats of the server poll, if it exists. 

        Usage:
        !pollstats
        '''

        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)


        serverid = ctx.message.guild.id
        try:
            if self.poll[serverid] is not None:
                embed = poll(self.poll[serverid],self.pollstats[serverid])
                return await ctx.send(embed=embed,delete_after=20)    
        except KeyError:
            return await ctx.send("There is no poll going on right now.")

    @commands.command(name='pollend')
    async def poll_end(self,ctx):
        '''
        End the current poll on the server, if it exists.

        Usage:
        !pollend
        '''

        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)


        serverid = ctx.message.guild.id
        try:
            if self.poll[serverid] is not None:
                await ctx.send('The poll has ended! Here are the final results: ')
                embed = poll(self.poll[serverid],self.pollstats[serverid])
                self.poll.pop(serverid,None)
                self.pollstats.pop(serverid,None)
                return await ctx.send(embed=embed,delete_after=20)    
        except KeyError:
            return await ctx.send("There is no poll going on right now.")

    @commands.command(name='vote')
    async def vote(self,ctx,vote:int = 0):
        '''
        Vote on one of the poll options on the server, if the option and poll exists.

        Usage:
        !vote 1
        !vote 4
        '''

        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)



        serverid = ctx.message.guild.id
        authorid = ctx.message.author.id
        try:
            if self.poll[serverid] is not None:
                if authorid in self.pollvoters[serverid]:
                    return await ctx.send('**{}**, you have already voted on this poll. Please wait until the next one.'.format(ctx.message.author),delete_after=10)
                vote = vote - 1
                try:
                   self.pollstats[serverid][vote] = self.pollstats[serverid][vote] + 1
                   self.pollvoters[serverid].append(ctx.message.author.id)
                   return await ctx.send('You have voted on the option: **{}**'.format(self.poll[serverid][vote+1]))
                except IndexError:
                    return await ctx.send('That is not an option on the poll.')
        except KeyError:
            return await ctx.send("There is no poll going on right now.")

    @commands.command(name='avatar')
    async def get_avatar(self,ctx,member:discord.Member = None):
        '''
        Retrieves the avatar of a user.
        '''

        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)


        if member is None:
            avatar_url = ctx.author.avatar_url_as(static_format='png')
        else:
            avatar_url = member.avatar_url_as(static_format='png')
        await ctx.send(avatar_url)
    
    


def poll(arg,results):
    embed=discord.Embed(title='**Question: ' + arg[0]+'**')
    answers= arg[1:]

    i = 0
    max = len(answers)
    while i!=max:
        embed.add_field(name='**Choice {}: **'.format(str(i+1)) + answers[i], value=results[i], inline=False)
        i = i+1
    return embed


