import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import youtube_dl
from itertools import cycle
import random
import validators
import copy



Pugna=['https://d1u5p3l4wpay3k.cloudfront.net/dota2_gamepedia/d/d4/Pugna_move_11.mp3','https://d1u5p3l4wpay3k.cloudfront.net/dota2_gamepedia/4/4d/Pugna_attack_09.mp3',
       'https://d1u5p3l4wpay3k.cloudfront.net/dota2_gamepedia/0/0b/Pugna_spawn_01.mp3','https://d1u5p3l4wpay3k.cloudfront.net/dota2_gamepedia/e/ec/Pugna_level_09.mp3',
       'https://d1u5p3l4wpay3k.cloudfront.net/dota2_gamepedia/9/95/Pugna_kill_10.mp3','https://d1u5p3l4wpay3k.cloudfront.net/dota2_gamepedia/f/f2/Pugna_deny_11.mp3']
Wizball = 'https://www.youtube.com/watch?v=sFYzjU-C3mA'
Utada = 'https://www.youtube.com/watch?v=yKgBhxWMTGM'
players = {}
queues = {}
queueURLs = {}
dupqueues = {}

current_playlist = {}
saved_playlist = {}

songs = 0

commandplayer = 0
'''
# Hello World program in Python

players = dict()
queues = {}

Aid = 'lma1'
url ='link'


lmao = players.get(Aid,False)
#Checking if there are any players
if lmao == False: #If there are no players, we will setup the Player and Queue
    players[Aid]=[url]
    queues[Aid]=[url]
else:
    queues[Aid].append[url]
print (players)
print (queues)
'''
'''
async def errorchecks(self,ctx):
    id = ctx.message.server.id
    channel = ctx.message.author.voice.voice_channel
    server = ctx.message.server
    checker = players.get(id,False)
    checker2 = queues.get(id,False)

    if channel is None:
        embed = create_embed('!playlist error:','Not connected to a voice channel.')
        await self.client.say(embed=embed)
        return False

    if self.client.is_voice_connected(server)==False:
        embed = create_embed('!playlist error:','LuigiBot not connected to a voice channel.')
        await self.client.say(embed=embed)
        return False

    if checker == False:
        embed = create_embed('!playlist error:','LuigiBot is not playing anything.')
        await self.client.say(embed=embed)
        return False
    return True
'''

def check_queue(id):
    global songs
    test = 0
    while test <=songs:
        #print ('We are in the while loop')
        #print (queues[id][test])
        if queues[id][test]==players[id]:
            #print('Hello world!')
            #print(test+1)
            #print(songs)
            if test+1 > songs:
                print('There are no more songs in queue')
                players.pop(id)
                break
            else:
                player=queues[id][test+1]
                players[id]=player
                player.start()
                print('Started the next song in the queue.')
                break
        else:
            test=test+1
            #print('test is updated.')

    print('check_queue has ended.')

def commandplayers():
    global commandplayer
    if commandplayer==1:
        commandplayer=0

def create_embed(atitle,adescription):
    embed = discord.Embed(
                title = atitle,
                description = adescription,
                colour = discord.Colour.blue())
    return embed

class MusicBot:
    def __init__(self,client):
        self.client = client

    @commands.command(pass_context=True)
    async def pause(self,ctx):
        """Pauses song currently playing."""
        id = ctx.message.server.id
        channel = ctx.message.author.voice.voice_channel
        server = ctx.message.server
        checker = players.get(id,False)

        if channel is None:
            embed = create_embed('!playing error:','Not connected to a voice channel.')
            await self.client.say(embed=embed)
            return

        if self.client.is_voice_connected(server)==False:
            embed = create_embed('!playing error:','LuigiBot not connected to a voice channel.')
            await self.client.say(embed=embed)
            return

        if checker == False:
            embed = create_embed('!playing error:','LuigiBot is not playing anything.')
            await self.client.say(embed=embed)
            return
        player = players[id]
        if player.is_playing()==False:
            await self.client.say('Bot is already paused')

        player.pause()
    '''
    @commands.command(pass_context=True)
    async def stop(self,ctx):
        id = ctx.message.server.id
        players[id].stop()
        players[id].clear()
    '''
    @commands.command(pass_context=True)
    async def resume(self,ctx):
        """Resumes a song that is paused."""
        id = ctx.message.server.id
        channel = ctx.message.author.voice.voice_channel
        server = ctx.message.server
        checker = players.get(id,False)

        if channel is None:
            embed = create_embed('!playing error:','Not connected to a voice channel.')
            await self.client.say(embed=embed)
            return

        if self.client.is_voice_connected(server)==False:
            embed = create_embed('!playing error:','LuigiBot not connected to a voice channel.')
            await self.client.say(embed=embed)
            return

        if checker == False:
            embed = create_embed('!playing error:','LuigiBot is not playing anything.')
            await self.client.say(embed=embed)
            return
        player = players[id]
        if player.is_playing():
            await self.client.say('Bot is already playing something!')
        player.resume()



    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """Skips the song that is currently playing."""
        id = ctx.message.server.id
        channel = ctx.message.author.voice.voice_channel
        server = ctx.message.server
        checker = players.get(id,False)

        if channel is None:
            embed = create_embed('!playing error:','Not connected to a voice channel.')
            await self.client.say(embed=embed)
            return

        if self.client.is_voice_connected(server)==False:
            embed = create_embed('!playing error:','LuigiBot not connected to a voice channel.')
            await self.client.say(embed=embed)
            return

        if checker == False:
            embed = create_embed('!playing error:','LuigiBot is not playing anything.')
            await self.client.say(embed=embed)
            return

        player= players[id]
        if player.is_playing():
            self.client.say('Skipping song..')
            player.stop()
        else:
            self.client.say('No song is currently playing..')

    @commands.command(pass_context=True, no_pm=True)
    async def playing(self, ctx):
        """Shows info about the currently played song."""
        id = ctx.message.server.id
        channel = ctx.message.author.voice.voice_channel
        server = ctx.message.server
        checker = players.get(id,False)

        if channel is None:
            embed = create_embed('!playing error:','Not connected to a voice channel.')
            await self.client.say(embed=embed)
            return

        if self.client.is_voice_connected(server)==False:
            embed = create_embed('!playing error:','LuigiBot not connected to a voice channel.')
            await self.client.say(embed=embed)
            return

        if checker == False:
            embed = create_embed('!playing error:','LuigiBot is not playing anything.')
            await self.client.say(embed=embed)
            return
        else:
            player = players[id]
            embed = create_embed('Now Playing:','{}'.format(player.title))
            await self.client.say(embed=embed)



    @commands.command(pass_context=True)
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def playlist(self,ctx):
        """Shows the queue of songs."""



        id = ctx.message.server.id
        channel = ctx.message.author.voice.voice_channel
        server = ctx.message.server
        checker = players.get(id,False)
        checker2 = queues.get(id,False)

        if channel is None:
            embed = create_embed('!playlist error:','Not connected to a voice channel.')
            await self.client.say(embed=embed)
            return

        if self.client.is_voice_connected(server)==False:
            embed = create_embed('!playlist error:','LuigiBot not connected to a voice channel.')
            await self.client.say(embed=embed)
            return

        if checker == False:
            embed = create_embed('!playlist error:','LuigiBot is not playing anything.')
            await self.client.say(embed=embed)
            return

        if checker2 == False:
            embed = create_embed('!playlist error:','There is no queue.')
            await self.client.say(embed=embed)
            return




        id = ctx.message.server.id
        playlist = []
        for x in queues[id]:
            playlist.append(x.title)
        embed = discord.Embed(
            colour = discord.Colour.blue())

        song = ''

        total = 0
        label = 1
        while total!=len(playlist):
            label_str = str(label)
            song += label_str + '. ' + playlist[total] + '\n'
            total = total + 1
            label = label +1
        embed.add_field(name='Current Playlist',value = song,inline=True)
        await self.client.say(embed=embed)









    @commands.command(pass_context=True)
    async def vol(self,ctx):
        """Changes the volume of the song currently playing."""
        id = ctx.message.server.id
        channel = ctx.message.author.voice.voice_channel
        args = ctx.message.content.split(' ')
        checker = players.get(id,False)

        if len(args)==1:
            embed = create_embed('!vol does not have an input','!vol requires a value from 0 to 1.')
            await self.client.say(embed=embed)
            return

        if len(args)>2:
            embed = create_embed('!vol incorrect format: Not a float.','!vol requires a value from 0 to 1.')
            await self.client.say(embed=embed)
            return

        value = args[1]
        try:
            val = float(value)
        except ValueError:
            embed = create_embed('!vol incorrect format: Not a float.','!vol requires a value from 0 to 1.')
            await self.client.say(embed=embed)
            return

        if channel is None:
            embed = create_embed('!vol cannot work!','LuigiBot is not in a voice chat.')
            await self.client.say(embed=embed)
            return


        if checker==False:
                embed = create_embed('!vol error!','LuigiBot is not playing anything.')
                await self.client.say(embed=embed)
                return

        val = float(value)
        if val > 1:
            embed = create_embed('!vol incorrect format: Value too large.','!vol requires a value from 0 to 1. Example: .45')
            await self.client.say(embed=embed)
            return
        if val < 0:
            embed = create_embed('!vol incorrect format: Value is a negative.','!vol requires a value from 0 to 1.')
            await self.client.say(embed=embed)
            return
        else:
            player = players[id]
            player.volume = val
            return









    @commands.command(pass_context=True)
    async def play(self,ctx):
        """Plays or queues up a song on LuigiBot."""
        global songs
        global commandplayer
        #Gathering essential information
        channel = ctx.message.author.voice.voice_channel
        server = ctx.message.server
        args = ctx.message.content.split(" ")


        #If the bot is not in a voice channel, then dont do anything.
        if channel is None:
            await self.client.say('Join a voice chat and call me again.')
            return



        if len(args)==1: #We check if the user only typed !play
                         #If that is the case, we will check if players is empty.
                         #The only case where players would be empty is when the queue has finished,
                         #Where check_queue sets players to empty.

            #test holds whatever player is in the playerdict at the server.id. If it has nothing, we return false.
            #Normally, players holds whatever player is currently playing at the time. If it's empty, then that means
            #that the queue has either finished or it has no queue.
            test = players.get(server.id,False)
            print(test)
            if test==False:
                #The player is not playing, so now we will check if there is a queue.
                test2 = queues.get(server.id,False)
                print (test2)
                if test2:
                    #If there is a queue, we will see if the user is in a voice channel.
                    if channel is None:
                        await self.client.say('Join a voice chat and call me again.')
                        return

                    #This if-else statement is just checks if the bot is in the channel, and if he isn't, bring the bot in it.
                    if self.client.is_voice_connected(server)==True:
                        await self.client.say('I am already in voice chat. I will see if I can restart the queue..')
                    else:
                        await self.client.join_voice_channel(channel)


                    #This is the voiceclient of the bot. We will use this to play songs from.
                    voice_client = self.client.voice_client_in(server)
                    first_check = 0
                    queues[server.id].clear()
                    #These ytdl players have been used, and we need to remake them. Clear it first.
                    #It's fine to clear it, because queueURLs saves all the URLs posted for the queues, in the correct order as well.

                    for x in queueURLs[server.id]:
                        #This first check is just setting up the new player to be in the front.
                        if first_check == 0:
                            player = await voice_client.create_ytdl_player(x, after=lambda: check_queue(server.id))
                            first_check=first_check+1
                            queues[server.id]=[player]
                        else:
                            #Now we just append every time after that.
                            player = await voice_client.create_ytdl_player(x, after=lambda: check_queue(server.id))
                            queues[server.id].append(player)
                    print('Post dupqueues creation.')
                    player = queues[server.id][0]
                    #After remaking the queue, we set our player to be the very front one.

                    #Finally, we place the player into the players dict. Again, whenever there is a ytdl_player in the players dict,
                    #That means it is currently playing a song.
                    players[server.id]=player
                    await self.client.say('Queue starting over!')
                    player.start()
                    #We start the queue over.
                    return
                else:
                    await self.client.say('No song queued yet.')
                    return
            else: #Otherwise, we will check if the bot is doing anything.
                  #If the bot isn't doing anything, then we know the bot is
                  #In a state where the user had used the !stop command, and start
                  #Over the video that was previously stopped, and continue the queue.

                #if players[server.id].


                await self.client.say('Do not interrupt the bot. He is doing something.')
                return



        url = args[1]
        print (url)
        if not validators.url(url):
            await self.client.say('You did not submit a valid url. Try again.')
            return
        else:
            if self.client.is_voice_connected(server)==True:
                await self.client.say('I am already in voice chat. I will see if I can play a song..')
            else:
                await self.client.join_voice_channel(channel)
            print(commandplayer)
            if commandplayer == 1:
                await self.client.say('Playing a command, please wait until it is done.')
                return
            voice_client = self.client.voice_client_in(server)
            try:
                player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
            except Exception as e:
                print(debugging.ERROR + "ERROR in 'play' command: " + str(e))
                return


            checker = players.get(server.id,False)#We will check if there is already a player.
                                        #If there is one, then we queue, if not, we setup the queue and player stuff.
            if checker == False:
                players[server.id]=player
                queues[server.id]=[player]
                queueURLs[server.id]=[url]
                print('Initialized players and queues.')
                player.start()
            else:
                queues[server.id].append(player)
                queueURLs[server.id].append(url)
                songs = songs+1
                print('Added a song to queue, songs has been updated.')
                await self.client.say('Video Queued.')
                if(players[server.id].is_playing()==False):
                    players[server.id]=player
                    player.start()











    @commands.command(pass_context=True)
    async def queue(self,ctx,url):
        """Do not use this pls """
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
        """Forces LuigiBot to leave the voice channel :("""

        server=ctx.message.server
        voice_client = self.client.voice_client_in(server)
        if voice_client:
            await voice_client.disconnect()
            print('Bot left the voice channel')
        else:
            print('Bot was not in a channel')

    @commands.command(pass_context=True)
    async def join(self,ctx):
        """Forces LuigiBot to join the voice channel."""
        channel = ctx.message.author.voice.voice_channel
        server = ctx.message.server
        if channel is None:
            await self.client.say('Join a voice chat and call me again.')
        if self.client.is_voice_connected(server)==True:
            await self.client.say('I am already in voice chat. I will see if I can play a song..')
        else:
            await self.client.join_voice_channel(channel)





    @commands.command(pass_context=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def pugna(self,ctx):
        """Plays a random Pugna voiceline."""
        global commandplayer
        args = ctx.message.content.split(' ')
        if len(args)>1:
            embed = create_embed('!pugna does not need an input','Pugna will have your head for that.')
            await self.client.say(embed=embed)
            return

        id = ctx.message.server.id
        channel = ctx.message.author.voice.voice_channel
        server = ctx.message.server

        if channel is None:
            await self.client.say('Do not call for Pugna when you are not in a voice chat. That only makes him angry.')


        else:
            if self.client.is_voice_connected(server)==False:
                await self.client.join_voice_channel(channel)

            checker = players.get(id,False)

            if checker:
                embed = create_embed('!pugna error!','LuigiBot is currently playing something.')
                await self.client.say(embed=embed)
                return

            server = ctx.message.server
            voice_client = self.client.voice_client_in(server)
            voiceline = random.randint(0,5)
            pugna = Pugna[voiceline]
            commandplayer = 1
            player = await voice_client.create_ytdl_player(pugna,after=lambda: commandplayers)
            players[id]=player
            player.start()
            while not player.is_done():
                await asyncio.sleep(1)

            player.stop()
            players.pop(id)
            voiceline = random.randint(0,5)
            pugna = Pugna[voiceline]
            commandplayer = 0

    @commands.command(pass_context=True)
    async def wizball(self,ctx):
        global commandplayer
        """Plays a random wizball song xd"""
        args = ctx.message.content.split(' ')
        if len(args)>1:
            embed = create_embed('!wizball does not need an input','You knew that, so do it correctly this time.')
            await self.client.say(embed=embed)
            return

        id = ctx.message.server.id
        channel = ctx.message.author.voice.voice_channel
        server = ctx.message.server

        if channel is None:
            await self.client.say('Wizball is going to continue playing Wizball until you join a call.')


        else:
            if self.client.is_voice_connected(server)==False:
                await self.client.join_voice_channel(channel)

            checker = players.get(id,False)

            if checker:
                embed = create_embed('!wizball error!','LuigiBot is currently playing something.')
                await self.client.say(embed=embed)
                return

            server = ctx.message.server
            voice_client = self.client.voice_client_in(server)
            wizball = Wizball
            player = await voice_client.create_ytdl_player(wizball, after=lambda: commandplayers)
            players[id]=player
            commandplayer = 1
            player.start()
            while not player.is_done():
                await asyncio.sleep(1)

            player.stop()
            players.pop(id)

    @commands.command(pass_context=True)
    async def KH(self,ctx):
        global commandplayer
        """Plays a random utada song xd"""
        args = ctx.message.content.split(' ')
        if len(args)>1:
            embed = create_embed('!KH does not need an input','You knew that, so do it correctly this time.')
            await self.client.say(embed=embed)
            return

        id = ctx.message.server.id
        channel = ctx.message.author.voice.voice_channel
        server = ctx.message.server

        if channel is None:
            await self.client.say('WHEN YOU ARE NOT IN A VOICE CHAT, THIS WILL NOT WORK.')


        else:
            if self.client.is_voice_connected(server)==False:
                await self.client.join_voice_channel(channel)

            checker = players.get(id,False)

            if checker:
                embed = create_embed('!KH error!','LuigiBot is currently playing something.')
                await self.client.say(embed=embed)
                return

            server = ctx.message.server
            voice_client = self.client.voice_client_in(server)
            utada = Utada
            player = await voice_client.create_ytdl_player(utada, after=lambda: commandplayers)
            players[id]=player
            commandplayer = 1
            player.start()
            while not player.is_done():
                await asyncio.sleep(1)

            player.stop()
            players.pop(id)


def setup(client):
    client.add_cog(MusicBot(client))
