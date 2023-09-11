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
from discord.utils import get
from datetime import datetime

from core import jsondb


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='luigibot',aliases=['Luigibot','LuigiBot','serverinfo'])
    async def serverinfo(self,ctx):
        msg = '''LuigiBot is a general purpose, self hosting bot. It was created by Faris Al-khatahtbeh.
If you'd like to see more from Faris, here is his GitHub: https://github.com/farisalkhat?tab=repositories

Here is the LuigiBot documentation, meant to easily setup LuigiBot and understand how all of the commands work: https://docs.google.com/document/d/17XkK43XTfauNpPQ7Hl4PxTw5Q4f2dwAuRE3rmYC87eI/edit?usp=sharing
        '''
        await ctx.send(msg,delete_after=30)



    @commands.command(name='joinmusic')
    async def joinmusic(self,ctx):
        """
        Sets the channel for botcommands to occur.
        """
        userid = str(ctx.author.id)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        
        serverid = str(ctx.message.guild.id)
        channelid = str(ctx.channel.id)
        try:
            server = self.servers[serverid]
            for uid in server['Music_Users']:
                if uid == userid:
                    return await ctx.send("You have already opted in!",delete_after = 10)
            server['Music_Users'].append(userid)
            await jsondb.save_servers(self)
            await ctx.send("You have opted in for the music stuff :3.".format(ctx.message.channel))
        except KeyError:
            return await ctx.send("Server info has not been created yet. Use the **!createserverinfo** command first.")
        
    @commands.command(name='leavemusic')
    async def leavemusic(self,ctx):
        """
        Sets the channel for botcommands to occur.
        """
        userid = str(ctx.author.id)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        
        serverid = str(ctx.message.guild.id)
        channelid = str(ctx.channel.id)
        try:
            server = self.servers[serverid]
            server['Music_Users'].remove(userid)
            await jsondb.save_servers(self)
            await ctx.send("You have opted out of music stuff".format(ctx.message.channel),delete_after = 10)
        except ValueError:
            return await ctx.send("You haven't opted in, dingus")

    @commands.command(name='rollusers')
    async def rollusers(self,ctx,members: commands.Greedy[discord.Member]):
        userid = str(ctx.author.id)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        
        if len(members)<=1:
            return await ctx.send("Not enough users")
        serverid = str(ctx.message.guild.id)
        channelid = str(ctx.channel.id)
        try:
            uid = random.choice(members)
            print(uid.id)
            await ctx.send("<@{}>, it's your turn baby!".format(uid.id))
        except KeyError:
            return await ctx.send("Server info has not been created yet. Use the **!createserverinfo** command first.")
    


    @commands.command(name='musictime')
    @commands.has_permissions(administrator=True)
    async def musictime(self,ctx):
        userid = str(ctx.author.id)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        
        serverid = str(ctx.message.guild.id)
        channelid = str(ctx.channel.id)
        try:
            server = self.servers[serverid]
            random.seed(datetime.now())
            uid = random.choice(server['Music_Users'])
            print(uid)


            if len(server['Music_Users_Done'])!=0:
                while uid in server['Music_Users_Done']:
                    random.seed(datetime.now())
                    uid = random.choice(server['Music_Users'])

            server['Music_Man'] = uid
            server['Music_Users_Done'].append(uid)
            await ctx.send("<@{}>, it's your turn baby!".format(uid))
            
            

            if len(server['Music_Users_Done'])==len(server['Music_Users']):
                await ctx.send("Everyone was a musicman once. Time for a reset!")
                server['Music_Users_Done'] = []
            
            await jsondb.save_servers(self)
            
        except KeyError:
            return await ctx.send("Server info has not been created yet. Use the **!createserverinfo** command first.")
    
    @commands.command(name='checkmusic')
    @commands.has_permissions(administrator=True)
    async def checkmusic(self,ctx):
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        
        serverid = str(ctx.message.guild.id)
        channelid = str(ctx.channel.id)
        try:
            server = self.servers[serverid]
            users = 'Users who havent gone yet: '
            doneusers = "Users who have gone already: " 
            for user in server['Music_Users']:
                if user not in server["Music_Users_Done"]:
                    member = await self.bot.fetch_user(user)
                    users = users + member.name + ', '

            for user in server["Music_Users_Done"]:
                member = await self.bot.fetch_user(user)
                doneusers = doneusers + member.name + ', '
            users = users[:-2]
            doneusers = doneusers[:-2]

            users += "\n"
            users+=doneusers
            
            await ctx.send(users)
            
        except KeyError:
            return await ctx.send("Server info has not been created yet. Use the **!createserverinfo** command first.")

    
    @commands.command(name="musicletter")
    @commands.has_permissions(administrator=True)
    async def musicletter(self,ctx):
        """
        Randomly generate a number between two given ranges. By default, it rolls between 1-100.
        You can provide two different integers to randomly select a number between them.

        Example:
        !letter
        """

        alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)

        random.seed(datetime.now())
        letter = random.choice(alphabet)
        serverid = str(ctx.message.guild.id)
        server = self.servers[serverid]
        while letter in server['Used_Letters']:
            letter = random.choice(alphabet)

        server['Used_Letters'].append(letter)


        match letter:
            case 'A':
                await ctx.send("Ayyyy, it's fuckin A")
            case 'B':
                await ctx.send("Sup boners. You got B" )
            case 'C':
                await ctx.send("Yo, yo, yo! My brother, Carlton! You got C")
            case 'D':
                await ctx.send("D? How 'bout deez nutz? Sorry")
            case 'E':
                await ctx.send("You got E for Extra Fuel")
            case 'F':
                await ctx.send("F is for football (I chiseled it)")
            case 'G':
                await ctx.send("G for Green Mario! That'sa me!" )
            case 'H':
                await ctx.send("Let me pop a quick H on this box so we all know its filled with hornets. You got H")
            case 'I':
                await ctx.send("I'm going to love what album you choose next. You got I")
            case 'J':
                await ctx.send("J. You're going for that Jesus-on-the-cross look")
            case 'K':
                await ctx.send("Go get them killer. You got K")
            case 'L':
                await ctx.send("You took an L ;)")
            case 'M':
                await ctx.send("Mammia Mia! You got M")
            case 'N':
                await ctx.send("Nooooooooo it's N" )
            case 'O':
                await ctx.send("Oooooooooooo it's O")
            case 'P':
                await ctx.send("P for poop. lol")
            case 'Q':
                await ctx.send("Quiver as you attempt to find an album Quickly for this Quirky Quesadilla letter: Q")
            case 'R':
                await ctx.send("You got Rick Rolled. By that I mean, you got R" )
            case 'S':
                await ctx.send("You got S! I hope she made lotsa spaghetti! :D")
            case 'T':
                await ctx.send("Don't test me. You got T" )
            case 'U':
                await ctx.send("U for u suck. just kidding")
            case 'V':
                await ctx.send("You got V. Oops lol" )
            case 'W':
                await ctx.send("W. That means you win :)")
            case 'X':
                await ctx.send("You're gonna need a Xanax for this one. You get X!")
            case 'Y':
                await ctx.send("Y for you suck. just kidding")
            case 'Z':
                await ctx.send("Zoinks that's a shit letter. Z")
            



        if len(server['Used_Letters'])==26:
            server['Used_Letters']=[]
        await jsondb.save_servers(self)
        

        
    @commands.command(name="resetmusicletters")
    @commands.has_permissions(administrator=True)
    async def resetmusicletters(self,ctx):
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)

        
        serverid = str(ctx.message.guild.id)
        server = self.servers[serverid]
        server['Used_Letters'] = []

        await jsondb.save_servers(self)
        return await ctx.send("Music letters reset")

    @commands.command(name="checkmusicletters")
    async def checkmusicletters(self,ctx):
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)

        
        serverid = str(ctx.message.guild.id)
        server = self.servers[serverid]
        alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        


        usedletters = ''
        unusedletters = ''
        for letter in alphabet:
            if letter in server['Used_Letters']:
                usedletters= usedletters +letter
            else:
                unusedletters=unusedletters+letter

        await ctx.send("Used letters:{}".format(usedletters))
        return await ctx.send("Unused letters:{}".format(unusedletters))
    




    @commands.command(name='userid', aliases=['uid'])
    async def userid(self,ctx,user: discord.Member = None):
        ''' Shows user ID. 
        Usage: !uid, !uid @Lefty
        '''
    
    @commands.command(name='whosplaying', aliases=['whpl'])
    async def whosplaying(self,ctx,*,arg):
        '''Shows a list of users who are playing the specified game.
        Usage: !whpl Dota 2
        '''


    @commands.command(name='roleid', aliases=['rid'])
    async def roleid(self,ctx,*,arg):
        '''Shows the id of the specified role.
        Usage: !rid Some Role
        '''
    
    @commands.command(name='channelid', aliases=['cid'])
    async def channelid(self,ctx):
        '''Shows current channel ID.
        Usage: !cid'''

    
    @commands.command(name='serverid', aliases=['sid'])
    async def serverid(self,ctx):
        '''Shows current server ID.
        Usage: !sid'''

    @commands.command(name='listservers')
    async def listservers(self,ctx):
        '''Lists servers the bot is on with some basic info. 
        Usage: !listservers

        Requirement: Bot Owner only.
        '''

    @commands.command(name='savechat')
    async def savechat(self,ctx, messages: int = 15):
        '''Saves a number of messages to a text file and sends it to you. 
        If no number is given, default is 15 messages.

        Usage: !savechat 15

        Requirement: Bot Owner only.
        '''

    @commands.command(name='streamrole')
    async def streamrole(self,ctx, *, args):
        '''
        Sets a role which is monitored for streamers (FromRole), and a role to add if a user from 'FromRole' is streaming (AddRole). 
        When a user from 'FromRole' starts streaming, they will receive an 'AddRole'. Provide no parameters to disable.

        Usage:  !streamrole "Eligible Streamers" "Featured Streams"

        Requirement: Manage Roles Server Permissions
        '''

    @commands.command(name='remind')
    async def remind(self,ctx, *, args):
        '''
        Sends a message to you or a channel after certain amount of time (max 2 months). First parameter is me/here/'channelname'. 
        Second parameter is time in a descending order (mo>w>d>h>m) example: 1w5d3h10m. Third parameter is a (multiword) message.

        Usage:
        !remind me 1d5h Do something
        !remind #general 1m Start now!
        '''


    @commands.command(name='remindlist')
    async def remindlist(self,ctx):    
        '''
        Lists all reminders you created.

        Usage: !remindlist 
        '''

    @commands.command(name='reminddel')
    async def reminddel(self,ctx, *, args): 
        '''
        Deletes a reminder on the specified index.
        
        Usage: !reminddel 3
        '''
    
    @commands.command(name='convert')
    async def convert(self,ctx, *, args):
        '''
        Convert quantities. Use .convertlist to see supported dimensions and currencies.

        Usage: !convert m km 1000
        '''
    
    @commands.command(name='convertlist')
    async def convertlist(self,ctx):
        '''
        List of the convertible dimensions and currencies.

        Usage: !convertlist
        '''

    @commands.command(name='invitecreate')
    async def invitecreate(self,ctx):
        '''
        Creates a new invite which has infinite max uses and never expires.
        Options --max-uses (-m) Maximum number of times the invite can be used. Default 0 (never).
        --unique (-u) Not setting this flag will result in bot getting the existing invite with the same settings if it exists, instead of creating a new one.
        --temporary (-t) If this flag is set, the user will be kicked from the guild once they close their client.
        --expire (-e) Time in seconds to expire the invite. Default 0 (no expiry). 

        Usage: !invc
        Requirement: CreateInstantInvite Channel Permission
        '''


      


    



    



        



    '''
    @commands.command(name='setprofile')
    async def setprofile(self,ctx,*,arg):

    @commands.command(name='setosu')
    async def setosu(self,ctx,*,arg):

    @commands.command(name='viewprofile')
    async def viewprofile(self,ctx, member:discord.Member=None):
    
    @commands.command(name='viewosu')
    async def viewosu(self,ctx, member:discord.Member=None):

    @commands.command(name='setdesc')
    async def setdesc(self,ctx,*,arg):

    
    @commands.command(name='addtwitch')
    async def addtwitch(self,ctx,*,arg):

    @commands.command(name='deltwitch')
    async def deltwitch(self,ctx,*,arg):

    @commands.command(name='viewtwitch')
    async def viewtwitch(self,ctx,*,arg):

    
    '''




    