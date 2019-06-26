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
import requests
import cat

from geopy import geocoders
from tzwhere import tzwhere
from youtube_api import YouTubeDataAPI


api_key = 'AIzaSyDGQXcGGIyajK9P7XjQHt2yotAKoiAx1EM'
GREEN = 0x16820d


class Image(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

        #AIzaSyDGQXcGGIyajK9P7XjQHt2yotAKoiAx1EM







    @commands.command(name="cat")
    async def cat(self,ctx):
        """
        Generate a random cat from random.cat/meow
        """
        r = requests.get('http://aws.random.cat/meow')
        print(r)
        js = r.json()
        print(js)
        em = discord.Embed(color=GREEN)
        em.set_image(url=js['file'])
        await ctx.send(embed=em) 


    @commands.command(name="woof")
    async def woof(self,ctx):
        """
        Generate a doggo from dog.ceo
        """
        r = requests.get('https://dog.ceo/api/breeds/image/random')
        js = r.json()
        
        
        em = discord.Embed(color=GREEN)
        em.set_image(url=js['message'])
        await ctx.send(embed=em) 

        
    @commands.command(name="youtube")
    async def youtube(self,ctx,*,arg):
        """
        Searches Youtube for the given search, and returns the first video given.
        """
        yt = YouTubeDataAPI(api_key)
        lmao = yt.search(arg)
        print(lmao[0])
        pog = lmao[0]
        link = 'https://www.youtube.com/watch?v=' + pog['video_id']
        await ctx.send(link)



    @commands.command(name="time")
    async def time(self,ctx,*,arg):
        """
        Retrieves the timezone for the given location. Utilizes geocoders and tzwhere.
        """

        g = geocoders.GoogleV3(api_key=api_key)
        
        place, (lat, lng) = g.geocode(arg)
        tz = tzwhere.tzwhere()
        timezone = g.timezone(lat,lng)

        await ctx.send('The time in **{}** is: **{}**'.format(place,timezone))
        #print (tz.tzNameAt(lat, lng))
