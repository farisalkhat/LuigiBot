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
import os,csv,sys
import re
from random import randint
import requests
from requests.exceptions import HTTPError
import cat
import urllib.parse
from geopy import geocoders
from tzwhere import tzwhere
from youtube_api import YouTubeDataAPI
import tokens
from pyosu import OsuApi
import praw
from core import jsondb
import random
from pathlib import Path

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

GREEN = 0x16820d

website = "https://farisalkhat.github.io/DrWilyDB/home"


class DrWilyDB(commands.Cog):
    @commands.command(name='drwilydb')
    async def drwilydb(self,ctx):
        """
        Simply sends the link to the Dr.Wily Database site. Made by Faris Al-khatahtbeh :3

        Usage:
        !drwilydb
        """
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)

            await ctx.send('Invalid format. Try using an actual link.',delete_after=20)
            return
        


        await ctx.send(website) 
        return 

    @commands.command(name='dailyrm')
    async def dailyrm(self,ctx):
        """
        Provides the robot master of the day from Dr.Wily's Database.

        Usage: 
        !dailyrm
        """
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)

            await ctx.send('Invalid format. Try using an actual link.',delete_after=20)
            return
        


        try:
            response = requests.get('https://mm8bitdm-v2.herokuapp.com/api/dailyrm')
            js = response.json()
            print(js)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  
            return await ctx.send("The STEAMID you provided does not exist.")
       
        link = js['image'].replace(" ", "%20").replace('\\',"/")
        image = 'https://farisalkhat.github.io/DrWilyDB/' + link
        url = 'https://farisalkhat.github.io/DrWilyDB/robotmasters/' + str(js['id'])


        embed=discord.Embed(title="{}".format(js['name']), description="The Daily Robot Master Pog",url=url, color=0x008000)
        embed.set_image(url=image)
        embed.add_field(name='Origin:', value=js['origin'], inline=True)
        embed.add_field(name='Primary Class:', value=js['primaryclass'], inline=True)

        await ctx.send(embed=embed) 
        return 

    @commands.command(name='recentmatch')
    async def recentmatch(self,ctx):
        """
        Get the last recorded match from the Dr.Wily Database.

        Usage:
        !recentmatch
        """
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)

            await ctx.send('Invalid format. Try using an actual link.',delete_after=20)
            return
        try:
            response = requests.get('https://mm8bitdm-v2.herokuapp.com/api/recentmatch')
            js = response.json()
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  
            return await ctx.send("Random match having some issue.")
       
        

        link = js['image'].replace(" ", "%20").replace('\\',"/")
        image = 'https://farisalkhat.github.io/DrWilyDB/' + link
        match_url = 'https://farisalkhat.github.io/DrWilyDB/matches/' + str(js['matchid'])

        stage = js['stage']
        stageid = js['stageid']
        

        embed=discord.Embed(title="{}".format(js['gametitle']), description=js['gamemode'],url=match_url, color=0x008000)
        embed.set_image(url=image)
        embed.add_field(name='Total Players:', value=js['totalplayers'], inline=True)
        embed.add_field(name='Stage:', value="[{}](https://farisalkhat.github.io/DrWilyDB/stages/{})".format(stage,stageid),inline=True)

        await ctx.send(embed=embed) 
        return 

    @commands.command(name='randommatch')
    async def randommatch(self,ctx):
        """
        Get a random match from the Dr.Wily Database.

        Usage:
        !recentmatch
        """
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)

            await ctx.send('Invalid format. Try using an actual link.',delete_after=20)
            return
        try:
            response = requests.get('https://mm8bitdm-v2.herokuapp.com/api/randommatch')
            js = response.json()
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  
            return await ctx.send("Random match having some issue.")
       
        

        link = js['image'].replace(" ", "%20").replace('\\',"/")
        image = 'https://farisalkhat.github.io/DrWilyDB/' + link
        match_url = 'https://farisalkhat.github.io/DrWilyDB/matches/' + str(js['matchid'])

        stage = js['stage']
        stageid = js['stageid']


        embed=discord.Embed(title="{}".format(js['gametitle']), description='Game Mode: {}'.format(js['gamemode']),url=match_url, color=0x008000)
        embed.set_image(url=image)
        embed.add_field(name='Total Players:', value=js['totalplayers'], inline=True)
        embed.add_field(name='Stage:', value="[{}](https://farisalkhat.github.io/DrWilyDB/stages/{})".format(stage,stageid),inline=True)

        await ctx.send(embed=embed) 
        return 
    
    @commands.command(name='rm')
    async def rm(self,ctx,*,arg):
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)

            await ctx.send('Invalid format. Try using an actual link.',delete_after=20)
            return
        try:
            response = requests.get('https://mm8bitdm-v2.herokuapp.com/api/robotmasters/name/{}'.format(arg))
            js = response.json()
            print(js)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  
            return await ctx.send("The robot master you provided does not exist.")
       
        robotmaster = requests.get('https://mm8bitdm-v2.herokuapp.com/api/robotmaster/{}'.format(js['id']))
        js = response.json()

        link = js['image'].replace(" ", "%20").replace('\\',"/")
        image = 'https://farisalkhat.github.io/DrWilyDB/' + link
        url = 'https://farisalkhat.github.io/DrWilyDB/robotmasters/' + str(js['id'])


        embed=discord.Embed(title="{}".format(js['name']), description="Beep Boop",url=url, color=0x008000)
        embed.set_image(url=image)
        embed.add_field(name='Origin:', value=js['origin'], inline=True)
        embed.add_field(name='Primary Class:', value=js['primaryclass'], inline=True)

        await ctx.send(embed=embed) 
        return 

    @commands.command(name='player')
    async def player(self,ctx,*,arg):
        print('frog lol')

    @commands.command(name='stage')
    async def stage(self,ctx,*,arg):
        print('frog lol')
    

    @commands.command(name='rmtrivia')
    async def rmtrivia(self,ctx):
        path = Path(__file__).parent / "../../core/RM_Trivia.csv"
        with path.open(encoding="utf8") as f:

            a = [{k: v for k, v in row.items()}
                for row in csv.DictReader(f, skipinitialspace=True)]

            random_trivia = random.randint(0,len(a)-1)
            while a[random_trivia]['Trivia']=='':
                random_trivia = random.randint(0,len(a)-1)

            
            string = a[random_trivia]['Robot Master']+': '+a[random_trivia]['Trivia']
            return await ctx.send(string) 
    
    
    