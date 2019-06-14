"""
Please understand Music bots are complex, and that even this basic example can be daunting to a beginner.

For this reason it's highly advised you familiarize yourself with discord.py, python and asyncio, BEFORE
you attempt to write a music bot.

This example makes use of: Python 3.6

For a more basic voice example please read:
    https://github.com/Rapptz/discord.py/blob/rewrite/examples/basic_voice.py

This is a very basic playlist example, which allows per guild playback of unique queues.
The commands implement very basic logic for basic usage. But allow for expansion. It would be advisable to implement
your own permissions and usage logic for commands.

e.g You might like to implement a vote before skipping the song or only allow admins to stop the player.

Music bots require lots of work, and tuning. Goodluck.
If you find any bugs feel free to ping me on discord. @Eviee#0666
"""
import discord
from discord.ext import commands

import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL



class Audio(commands.Cog):

    #__slots__ = ('bot', 'players')

    def __init__(self,bot):
        self.bot = bot
        self.players = {}

    def get_player(self, ctx):
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player
        return player

    @commands.command(name ='connect', aliases = ['join'])
    async def connect_(self,ctx,*,channel: discord.VoiceChannel=None):
        if not channel:
            channel = ctx.author.voice.channel

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'lmao')

        await ctx.send(f'Connected to: **{channel}**', delete_after=20)
    
        
    @commands.command(name='play', aliases=['sing'])
    async def play_(self,ctx,*,search:str):

        await ctx.trigger_typing()
        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        #player = self.get_player(ctx)

        #source = await YTDLSource.create_source(ctx,search, loop = self.bot.loop, download=False)
        #await player.queue.put(source)
        







