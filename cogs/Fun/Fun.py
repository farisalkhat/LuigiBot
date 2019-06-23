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
