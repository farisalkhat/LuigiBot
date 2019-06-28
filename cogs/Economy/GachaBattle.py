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
import datetime
import threading

class Hero:
    def __init__(self,hero,moves):
        Owner = hero[]

        HeroName = hero[]
        Description = hero[]

        HP = hero[]
        ATK = hero[]
        DEF = hero[]
        SDEF = hero[]
        SPD =  hero[]

        Move1 = moves[0]
        Move2 = moves[1]
        Move3 = moves[2]
        Move4 = moves[3]

        Status = []

class Battle:

    def __init__(self,ctx,p1,p2):
        self.bot = ctx.bot
        self.guild = ctx.guild
        self.channel = ctx.channel
        self.p1 = p1    #Player 1 ID
        self.p2 = p2    #Player 2 ID


        self.p1_hero = gachadatabase.get_primary_hero([serverid,p1]) #Player 1 Hero Stats and Type
        self.p2_hero = gachadatabase.get_primary_hero([serverid,p2]) #Player 2 Hero Stats and Type
        self.turn = self.compare_hero_speeds() #Compare hero speeds for who goes first
        self.p1_moves = gachadatabase.get_primary_moves([self.guild.id,p1_hero[1]])
        self.p2_moves = gachadatabase.get_primary_moves([self.guild.id,p2_hero[1]])

        Hero1 = Hero(p1_hero,p1_moves)
        Hero2 = Hero(p2_hero,p2_moves)

    def start_battle():
        print("The battle has started!")
        while True:
            if turn==1:
                print("It is **{}**'s turn to attack!").format(p1.hero[0])
                #Wait for user move, 1,2,3,4
                #Wait for forfeit
                #Wait for force forfeit
                if input == 1 or input == 2 or input == 3 or input == 4:
                    execute_move(self.Hero1,self.Hero2,input)
                turn = 2
            if turn==2:
                print("It is **{}**'s turn to attack!").format(p2.hero[0])

                #Wait for forfeit
                if input == 'f':
                    return print('{} has forfeited. {} wins the battle!')
                #Wait for force forfeit
                if input == 'ff':
                #Wait for user move, 1,2,3,4
                if input == 1 or input == 2 or input == 3 or input == 4:
                    execute_move(self.Hero2,self.Hero1,input)
                turn = 1

    def execute_move(hero1,hero2,input):
        if input == 1:
            move = hero1.Move1
        if input==2:
            move = hero1.Move2
        if input==3:
            move=hero1.Move3
        if input==4:
            move=hero1.Move4

        Status1 = move[]
        Status2 = move[]






    def compare_hero_speeds():
        if self.p1_hero[5] > self.p2_hero[5]:
            return 1
        return 2







class GachaBattle(commands.Cog):
    __slots__ = ('bot','battles',)
    def __init__(self,bot):
        self.bot = bot
        self.battles = {}





    '''
    @commands.command(name='race')
    async def race(self,ctx):
        author = ctx.message.author
        wait = 20

        msg = await ctx.send("!!!The Great Animal Race is here!!! Do '!race enter' to join! \n"
        "You have {} seconds to join!".format(wait))

        await asyncio.sleep(wait)

        cache_msg = await ctx.fetch_message(msg.id)

        reactions = cache_msg.reactions
        for reaction in reactions:
            async for user in reaction.users():
                print("Hello!")
    '''
