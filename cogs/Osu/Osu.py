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
import shlex
from db import database
import requests
import tokens

from pyosu import OsuApi


api = OsuApi(tokens.osu_api)

class Osu(commands.Cog):
    __slots__ = ('bot')
    def __init__(self,bot):
        self.bot = bot


    @commands.command(name='osu')
    async def osu(self,ctx,*,arg):
        """
        Provides basic stats of the given user, if they exist. Uses Renondedju's Osu.py library https://github.com/Renondedju/Osu.py

        Example:
        !osu Leftyy
        """

        #recent5 = await api.get_user_recents(user=arg,limit = 5)

        user = await api.get_user(user = arg)
        if not user:
            await ctx.send("Sorry, **{}** is not an Osu Player!".format(arg))
            return

        playcount = str(user.playcount)
        pp_rank = str(user.pp_rank)
        level = str(user.level)
        accuracy = str(user.accuracy)
        image = 'http://s.ppy.sh/a/'  + str(user.user_id)

        embed=discord.Embed(title="{}".format(arg), description="osu stats for this user!", color=0x008000)
        embed.set_thumbnail(url=image)
        embed.add_field(name='Level:', value=level, inline=True)
        embed.add_field(name='Playcount:', value=playcount, inline=True)
        embed.add_field(name='Rank:', value=pp_rank, inline=True)
        embed.add_field(name='Accuracy:', value=accuracy, inline=True)

        await ctx.send(embed = embed)


    @commands.command(name='osu5')
    async def osu5(self,ctx,*,arg):
        """
        Find the top 5 beatmaps of the given user. Uses Renondedju's Osu.py library https://github.com/Renondedju/Osu.py

        Usage:
        !osu5 Leftyy
        """
        user = await api.get_user(user = arg)
        image = 'http://s.ppy.sh/a/'  + str(user.user_id)
        

        if not user:
            await ctx.send("Sorry, **{}** is not an Osu Player!".format(arg))
            return

        best5 = await api.get_user_bests(user=arg,limit = 5)
        osubest = []

        for best in best5:
            beatmap = await api.get_beatmap(beatmap_id =best.beatmap_id)
            beatmap_title = beatmap.title

            beatmap_id = beatmap.beatmapset_id
            beatmap_diff = best.beatmap_id
            creator = beatmap.creator


            osutuple = [beatmap_title,  str(best.score), str(best.maxcombo), str(best.pp), str(beatmap_id), str(beatmap_diff), creator]
            osubest.append(osutuple)

        embed=discord.Embed(title="{}".format(arg), description="Top 5 Plays!", color=0x008000)
        embed.set_thumbnail(url=image)


        

        for bestmap in osubest:

            link = "https://osu.ppy.sh/beatmapsets/" + bestmap[4]  +"#osu/" + bestmap[5] + ')'
            title = bestmap[0] + ' by ' + bestmap[6] + ': '
            together = title + link

            info = '**Score:** '+ bestmap[1] + '    **Max Combo:** ' + bestmap[2] + '    **PP: **' + bestmap[3]
            embed.add_field(name=together, value=info )

        await ctx.send(embed = embed)

    @commands.command(name='osub')
    async def osub(self,ctx,*,arg):
        """
        Shows basic information of an osu beatmap. Must provide the link to the beatmap. Uses Renondedju's Osu.py library https://github.com/Renondedju/Osu.py
        """
        compare = 'https://osu.ppy.sh/beatmapsets/'
        if len(arg)>31:
            if compare == arg[0:31]:
                beatmap_id = arg[31:37]
                print(beatmap_id)
            beatmap = await api.get_beatmap(beatmapset_id = beatmap_id)
            if not beatmap:
                await ctx.send('Beatmap does not exist.',delete_after=20)
                return
            
            title = beatmap.title + " by " + beatmap.artist
            length = beatmap.total_length
            difficulty = beatmap.difficultyrating
            creator = beatmap.creator
            bpm = str(beatmap.bpm)
            max_combo = str(beatmap.max_combo)
            playcount = str(beatmap.playcount)

            embed=discord.Embed(title=title, url=arg, description="All the basic information for this song!", color=0xe005ba)
            embed.add_field(name='Length', value=length, inline=True)
            embed.add_field(name='Difficulty', value=difficulty, inline=True)
            embed.add_field(name='Creator', value=creator, inline=True)
            embed.add_field(name='BPM', value=bpm, inline=True)
            embed.add_field(name='Max Combo', value=max_combo, inline=True)
            embed.add_field(name='Playcount', value=playcount, inline=True)
            await ctx.send(embed=embed) 
            return 

        else:
            await ctx.send('Invalid format. Try using an actual link.',delete_after=20)
            return

           
        
        







        
        '''

        for recent in recent5:
            beatmap = await api.get_beatmap(beatmap_id =best.beatmap_id)
            beatmap_title = beatmap.title

            osutuple = ["Beatmap " +beatmap_title, "Score: " + str(best.score),"Max Combo: " + str(best.maxcombo),"PP: " + str(best.pp)]
            osurecent.append(osutuple)

        '''




           

        #await ctx.send(best5)
        #await ctx.send(recent5)

        
    
