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
import urllib.parse
from geopy import geocoders
#from tzwhere import tzwhere
from youtube_api import YouTubeDataAPI
import tokens
#import pyosu
import praw
from core import jsondb


google_key = tokens.google_api
# api = pyosu.main(tokens.osu_api)
google_search_key = tokens.google_search_key
urban_search_key = tokens.urban_search_key
google_image_key = tokens.google_image_key

reddit_client = tokens.reddit_client
reddit_secret = tokens.reddit_secret
user_agent = tokens.user_agent

GREEN = 0x16820d


class Search(commands.Cog):

    __slots__ = ('users','items','shop','servers')
    def __init__(self,bot):
        self.bot = bot
        self.users = {}
        self.items = {}
        self.shop = {}
        self.servers = {}

    @commands.command(name="cat")
    async def cat(self,ctx):
        """
        Generate a random cat from random.cat/meow
        """

        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
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
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
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
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        yt = YouTubeDataAPI(google_key)
        lmao = yt.search(arg)
        print(lmao[0])
        pog = lmao[0]
        link = 'https://www.youtube.com/watch?v=' + pog['video_id']
        await ctx.send(link)



    # @commands.command(name="time")
    # async def time(self,ctx,*,arg):
    #     """
    #     Retrieves the timezone for the given location. Utilizes geocoders and tzwhere.
    #     """

    #     await jsondb.load_servers(self)
    #     if jsondb.permission(self,ctx) is False:
    #         return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
    #     g = geocoders.GoogleV3(api_key=google_key)
        
    #     place, (lat, lng) = g.geocode(arg)
    #     tz = tzwhere.tzwhere()
    #     timezone = g.timezone(lat,lng)

    #     await ctx.send('The time in **{}** is: **{}**'.format(place,timezone))
    #     #print (tz.tzNameAt(lat, lng))

    @commands.command(name="google",aliases=['g'])
    async def google(self,ctx,*,arg):
        '''
        Retrieves the first result for the given search. 
        '''
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)

        query = 'https://www.googleapis.com/customsearch/v1?key={}&cx={}&q='.format(google_key,google_search_key) + urllib.parse.quote_plus(arg) + "&start=1"
        
        r = requests.get(query)
        js = r.json()
        
        result = js['items'][0]
        link = result['link']
        await ctx.send(link)


    @commands.command(name='urban',aliases=['u'])
    async def urban(self,ctx,*,arg):
        '''
        Retrieves the first urban dictionary result for the given argument.
        '''
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        query = 'http://api.urbandictionary.com/v0/define?term={}'.format(urllib.parse.quote_plus(arg))
        r = requests.get(query)
        js = r.json()

        result = js['list'][0]['definition']
        await ctx.send('**{}**: '.format(arg)+result)


    @commands.command(name='w2g')
    async def w2g(self,ctx):
        '''
        Creates a watch2gether room.
        '''

        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)

        query = 'https://www.watch2gether.com/rooms/create.json'
        r = requests.post(query)
        js = r.json()

        streamkey = js['streamkey']

        await ctx.send("Watch2gether room created: https://www.watch2gether.com/rooms/{}?lang=en".format(streamkey))





    # @commands.command(name='osu')
    # async def osu(self,ctx,*,arg):
    #     """
    #     Provides basic stats of the given user, if they exist. Uses Renondedju's Osu.py library https://github.com/Renondedju/Osu.py

    #     Example:
    #     !osu Leftyy
    #     """
    #     await jsondb.load_servers(self)
    #     if jsondb.permission(self,ctx) is False:
    #         return await ctx.send(jsondb.NOPERMISSION,delete_after=10)

    #     #recent5 = await api.get_user_recents(user=arg,limit = 5)

    #     user = await api.get_user(user = arg)
    #     if not user:
    #         await ctx.send("Sorry, **{}** is not an Osu Player!".format(arg))
    #         return

    #     playcount = str(user.playcount)
    #     pp_rank = str(user.pp_rank)
    #     level = str(user.level)
    #     accuracy = str(user.accuracy)
    #     image = 'http://s.ppy.sh/a/'  + str(user.user_id)

    #     embed=discord.Embed(title="{}".format(arg), description="osu stats for this user!", color=0x008000)
    #     embed.set_thumbnail(url=image)
    #     embed.add_field(name='Level:', value=level, inline=True)
    #     embed.add_field(name='Playcount:', value=playcount, inline=True)
    #     embed.add_field(name='Rank:', value=pp_rank, inline=True)
    #     embed.add_field(name='Accuracy:', value=accuracy, inline=True)

    #     await ctx.send(embed = embed)


    # @commands.command(name='osu5')
    # async def osu5(self,ctx,*,arg):
    #     """
    #     Find the top 5 beatmaps of the given user. Uses Renondedju's Osu.py library https://github.com/Renondedju/Osu.py

    #     Usage:
    #     !osu5 Leftyy
    #     """
    #     await jsondb.load_servers(self)
    #     if jsondb.permission(self,ctx) is False:
    #         return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
    #     user = await api.get_user(user = arg)
    #     image = 'http://s.ppy.sh/a/'  + str(user.user_id)
        

    #     if not user:
    #         await ctx.send("Sorry, **{}** is not an Osu Player!".format(arg))
    #         return

    #     best5 = await api.get_user_bests(user=arg,limit = 5)
    #     osubest = []

    #     for best in best5:
    #         beatmap = await api.get_beatmap(beatmap_id =best.beatmap_id)
    #         beatmap_title = beatmap.title

    #         beatmap_id = beatmap.beatmapset_id
    #         beatmap_diff = best.beatmap_id
    #         creator = beatmap.creator


    #         osutuple = [beatmap_title,  str(best.score), str(best.maxcombo), str(best.pp), str(beatmap_id), str(beatmap_diff), creator]
    #         osubest.append(osutuple)

    #     embed=discord.Embed(title="{}".format(arg), description="Top 5 Plays!", color=0x008000)
    #     embed.set_thumbnail(url=image)


        

    #     for bestmap in osubest:

    #         link = "https://osu.ppy.sh/beatmapsets/" + bestmap[4]  +"#osu/" + bestmap[5] + ')'
    #         title = bestmap[0] + ' by ' + bestmap[6] + ': '
    #         together = title + link

    #         info = '**Score:** '+ bestmap[1] + '    **Max Combo:** ' + bestmap[2] + '    **PP: **' + bestmap[3]
    #         embed.add_field(name=together, value=info )

    #     await ctx.send(embed = embed)

    # @commands.command(name='osub')
    # async def osub(self,ctx,*,arg):
    #     """
    #     Shows basic information of an osu beatmap. Must provide the link to the beatmap. Uses Renondedju's Osu.py library https://github.com/Renondedju/Osu.py
    #     """
    #     await jsondb.load_servers(self)
    #     if jsondb.permission(self,ctx) is False:
    #         return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
    #     compare = 'https://osu.ppy.sh/beatmapsets/'
    #     if len(arg)>31:
    #         if compare == arg[0:31]:
    #             beatmap_id = arg[31:37]
    #             print(beatmap_id)
    #         beatmap = await api.get_beatmap(beatmapset_id = beatmap_id)
    #         if not beatmap:
    #             await ctx.send('Beatmap does not exist.',delete_after=20)
    #             return
            
    #         title = beatmap.title + " by " + beatmap.artist
    #         length = beatmap.total_length
    #         difficulty = beatmap.difficultyrating
    #         creator = beatmap.creator
    #         bpm = str(beatmap.bpm)
    #         max_combo = str(beatmap.max_combo)
    #         playcount = str(beatmap.playcount)

    #         embed=discord.Embed(title=title, url=arg, description="All the basic information for this song!", color=0xe005ba)
    #         embed.add_field(name='Length', value=length, inline=True)
    #         embed.add_field(name='Difficulty', value=difficulty, inline=True)
    #         embed.add_field(name='Creator', value=creator, inline=True)
    #         embed.add_field(name='BPM', value=bpm, inline=True)
    #         embed.add_field(name='Max Combo', value=max_combo, inline=True)
    #         embed.add_field(name='Playcount', value=playcount, inline=True)
    #         await ctx.send(embed=embed) 
    #         return 

    #     else:
    #         await ctx.send('Invalid format. Try using an actual link.',delete_after=20)
    #         return

    
    @commands.command(name='smashbros')
    async def smashbros(self,ctx, *,arg=None):
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)

        reddit = praw.Reddit(client_id = reddit_client,
        client_secret =reddit_secret,
        user_agent= user_agent)
        titles = []
        links = []
        



        if arg is None:
            for submission in reddit.subreddit('smashbros').hot(limit=5):
                titles.append(submission.title)
                links.append(submission.url)
        elif arg == 'controversial' or arg == 'contro':
            for submission in reddit.subreddit('smashbros').controversial('week',limit=5):
                titles.append(submission.title)
                links.append(submission.url)
        elif arg == 'gild' or arg =='gilded':
            for submission in reddit.subreddit('smashbros').gilded('week',limit=5):
                titles.append(submission.title)
                links.append(submission.url)
        elif arg == 'hot':
            for submission in reddit.subreddit('smashbros').hot(limit=5):
                titles.append(submission.title)
                links.append(submission.url)
        elif arg =='new':
            for submission in reddit.subreddit('smashbros').new('week',limit=5):
                titles.append(submission.title)
                links.append(submission.url)
        elif arg == 'rise' or arg =='rising':
            for submission in reddit.subreddit('smashbros').rising('week',limit=5):
                titles.append(submission.title)
                links.append(submission.url)
        elif arg == 'top':
            for submission in reddit.subreddit('smashbros').top('week',limit=5):
                titles.append(submission.title)
                links.append(submission.url)
        else:
            for submission in reddit.subreddit('smashbros').hot('week',limit=5):
                titles.append(submission.title)
                links.append(submission.url)

        title = ''
        i = 0
        while i!=5:
            title =title+  '**'+titles[i] + ':** ' + links[i] + '\n'
            i = i+1

        title = title + "**This post will be deleted after 30 seconds.**"
        await ctx.send(title)



    @commands.command(name='smashrand')
    async def smashrand(self,ctx):
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        reddit = praw.Reddit(client_id = reddit_client,
        client_secret =reddit_secret,
        user_agent= user_agent)
        titles = []
        links = []
        for submission in reddit.subreddit('smashbros').top('week',limit=20):
                titles.append(submission.title)
                links.append(submission.url)
        print(titles)
        print(links)
        r = randint(0,10)
        title = titles[r]
        link = links[r]

        result = '**'+title + ':** ' + link
        await ctx.send(result)

    

    @commands.command(name='dota2rand')
    async def dota2rand(self,ctx):
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        reddit = praw.Reddit(client_id = reddit_client,
        client_secret =reddit_secret,
        user_agent= user_agent)
        titles = []
        links = []
        for submission in reddit.subreddit('dota2').hot(limit=20):
                titles.append(submission.title)
                links.append(submission.url)
        print(titles)
        print(links)
        r = randint(0,10)
        title = titles[r]
        link = links[r]

        result = '**'+title + ':** ' + link
        await ctx.send(result)


    @commands.command(name='gamingrand')
    async def gamingrand(self,ctx):
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        reddit = praw.Reddit(client_id = reddit_client,
        client_secret =reddit_secret,
        user_agent= user_agent)
        titles = []
        links = []
        for submission in reddit.subreddit('gaming').hot(limit=20):
                titles.append(submission.title)
                links.append(submission.url)
        print(titles)
        print(links)
        r = randint(0,10)
        title = titles[r]
        link = links[r]

        result = '**'+title + ':** ' + link
        await ctx.send(result)
    
    @commands.command(name='wholesomerand')
    async def wholesomerand(self,ctx):
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        reddit = praw.Reddit(client_id = reddit_client,
        client_secret =reddit_secret,
        user_agent= user_agent)
        titles = []
        links = []
        for submission in reddit.subreddit('wholesomememes').hot(limit=20):
                titles.append(submission.title)
                links.append(submission.url)
        print(titles)
        print(links)
        r = randint(0,10)
        title = titles[r]
        link = links[r]

        result = '**'+title + ':** ' + link
        await ctx.send(result)
    
    @commands.command(name='fehrand')
    async def fehrand(self,ctx):
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        reddit = praw.Reddit(client_id = reddit_client,
        client_secret =reddit_secret,
        user_agent= user_agent)
        titles = []
        links = []
        for submission in reddit.subreddit('fireemblemheroes').hot(limit=20):
                titles.append(submission.title)
                links.append(submission.url)
        print(titles)
        print(links)
        r = randint(0,10)
        title = titles[r]
        link = links[r]

        result = '**'+title + ':** ' + link
        await ctx.send(result)


    @commands.command(name='w2g')
    async def w2g(self,ctx):
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        await ctx.send('https://w2g.tv/rooms/gayroom-ld5v722axyy28alfgs?lang=en')
