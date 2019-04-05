import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import youtube_dl
from itertools import cycle
import random

Pugna=['https://d1u5p3l4wpay3k.cloudfront.net/dota2_gamepedia/d/d4/Pugna_move_11.mp3','https://d1u5p3l4wpay3k.cloudfront.net/dota2_gamepedia/4/4d/Pugna_attack_09.mp3',
       'https://d1u5p3l4wpay3k.cloudfront.net/dota2_gamepedia/0/0b/Pugna_spawn_01.mp3','https://d1u5p3l4wpay3k.cloudfront.net/dota2_gamepedia/e/ec/Pugna_level_09.mp3',
       'https://d1u5p3l4wpay3k.cloudfront.net/dota2_gamepedia/9/95/Pugna_kill_10.mp3','https://d1u5p3l4wpay3k.cloudfront.net/dota2_gamepedia/f/f2/Pugna_deny_11.mp3']

players = {}
queues = {}
counter = 0

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        player[id]=player
        player.start()

        
class MusicBot:
    def __init__(self,client):
        self.client = client

    @commands.command(pass_context=True)
    async def pause(self,ctx):
        id = ctx.message.server.id
        players[id].pause()

    @commands.command(pass_context=True)
    async def stop(self,ctx):
        id = ctx.message.server.id
        players[id].stop()

    @commands.command(pass_context=True)
    async def resume(self,ctx):
        id = ctx.message.server.id
        players[id].resume()

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        id = ctx.message.server.id
        player= players[id]
        if player.is_playing():
            self.client.say('Skipping song..')
            player.skip()
        else:
            self.client.say('No song is currently playing..')
        
		

    @commands.command(pass_context=True)
    async def play(self,ctx,url):
        channel = ctx.message.author.voice.voice_channel
        
        if channel is None:
            await self.client.say('Join a voice chat and call me again.')
        else:

            await self.client.join_voice_channel(channel)
	
            server = ctx.message.server
            voice_client = self.client.voice_client_in(server)
            

            
            player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
            players[server.id]=player
            player.start()


    @commands.command(pass_context=True)
    async def queue(self,ctx,url):
        server = ctx.message.server
        voice_client = self.client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url,after=lambda: check_queue(server.id))

        if server.id in queues:
            queues[server.id].append(player)
        else:
            queues[server.id] = [player]
        await self.client.say('Video Queued')

    
    @commands.command(pass_context=True)
    async def leave(self,ctx):
        server=ctx.message.server
        voice_client = self.client.voice_client_in(server)
        if voice_client:
            await voice_client.disconnect()
            print('Bot left the voice channel')
        else:
            print('Bot was not in a channel')


    @commands.command(pass_context=True)
    async def pugna(self,ctx):
        channel = ctx.message.author.voice.voice_channel
        if channel is None:
            await self.client.say('Do not call for Pugna when you are not in a voice chat. That only makes him angry.')
        else:
            await self.client.join_voice_channel(channel)
            server = ctx.message.server
            voice_client = self.client.voice_client_in(server)
            voiceline = random.randint(0,5)
            pugna = Pugna[voiceline]
            player = await voice_client.create_ytdl_player(pugna, after=lambda: check_queue(server.id))
            player.start()
            while not player.is_done():
                await asyncio.sleep(1)

            player.stop()
            await voice_client.disconnect()
            voiceline = random.randint(0,5)
            pugna = Pugna[voiceline]
                                                 
def setup(client):
    client.add_cog(MusicBot(client))
