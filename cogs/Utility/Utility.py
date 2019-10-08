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

    @commands.command(name='invitecreate' aliases=['invc'])
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




    