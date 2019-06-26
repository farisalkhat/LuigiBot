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

from pyosu import OsuApi



api = OsuApi(api_key)

class Osu(commands.Cog):
    __slots__ = ('bot')
    def __init__(self,bot):
        self.bot = bot


    @commands.command(name='osu')
    async def osu(self,ctx,*,arg):
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


        
        '''

        for recent in recent5:
            beatmap = await api.get_beatmap(beatmap_id =best.beatmap_id)
            beatmap_title = beatmap.title

            osutuple = ["Beatmap " +beatmap_title, "Score: " + str(best.score),"Max Combo: " + str(best.maxcombo),"PP: " + str(best.pp)]
            osurecent.append(osutuple)

        '''




           

        #await ctx.send(best5)
        #await ctx.send(recent5)

        
    
