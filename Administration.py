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
import os



default_ban_message = 'You have been banned, '
default_kick_message = ' has been kicked.'
king_of_games= '144694253631700992'
smuckers_goober = '144697844110983168'
admins = [king_of_games,smuckers_goober]
kick_reason = 'not specified.'


def create_embed(atitle,adescription):
    embed = discord.Embed(
                title = atitle,
                description = adescription,
                colour = discord.Colour.blue())
    return embed


class Administration:
    def __init__(self,client):
        self.client = client

    @commands.command(pass_context=True)
    async def kick(self,ctx):
        global default_kick_message
        global kick_reason
        author = ctx.message.author
        server = ctx.message.server
        args = ctx.message.content.split(' ')

        if len(args)==1:
            embed = create_embed('!kick error:','You need to specify a user and then optionally a reason.')
            await self.client.say(embed=embed)
            return
        if not ctx.message.mentions:
            embed = create_embed('!kick error:','You did not mention a user or the user is no longer on the server.')
            await self.client.say(embed=embed)
            return
        userid = ctx.message.mentions[0].id
        member = server.get_member(userid)
        if len(args) > 2:
            kick_reason = args[2:]



        if ctx.message.author.id == userid: #Making sure user doesn't kick himself.
            embed = create_embed('!kick error:','You cannot kick yourself, fool!')
            await self.client.say(embed=embed)
            return

        for admin in admins: #Goes through list of roles allowed to touch this command to make sure user can do it.
            if  admin in [role.id for role in ctx.message.author.roles]:
                await self.client.kick(member)
                embed = create_embed('User kicked by {}'.format(author),'@{} {} The reason for the kick was {}'.format(member,default_kick_message,kick_reason))
                await self.client.say(embed=embed)











    @commands.command(pass_context=True)
    async def unban(self,ctx):
        userid = ctx.message.mentions
        server = ctx.message.server
        if ctx.message.author == self.client.user:
            return
        client.unban(server,userid)


    '''
    async def softban(self,ctx):
    @commands.command(pass_context=True)
    async def kick(self,ctx):
    @commands.command(pass_context=True)
    async def togglexclsar(self,ctx):
    @commands.command(pass_context=True)
    '''
    '''
    @commands.command(pass_context=True)
    async def deafen(self,ctx):


    @commands.command(pass_context=True)
    async def undeafen(self,ctx):


    @commands.command(pass_context=True)
    async def delvoichanl(self,ctx):


    @commands.command(pass_context=True)
    async def createvoichanl(self,ctx):


    @commands.command(pass_context=True)
    async def deltxtchanl(self,ctx):


    @commands.command(pass_context=True)
    async def setchanlname(self,ctx):


    @commands.command(pass_context=True)
    async def setmuterole(self,ctx):


    @commands.command(pass_context=True)
    async def mute(self,ctx):


    @commands.command(pass_context=True)
    async def unmute(self,ctx):


    @commands.command(pass_context=True)
    async def chatmute(self,ctx):

    @commands.command(pass_context=True)
    async def chatmute(self,ctx):

    @commands.command(pass_context=True)
    async def chatunmute(self,ctx):

    @commands.command(pass_context=True)
    async def voicemute(self,ctx):
    @commands.command(pass_context=True)
    async def voiceunmute(self,ctx):
    @commands.command(pass_context=True)
    async def prune(self,ctx):
    @commands.command(pass_context=True)
    async def setrole(self,ctx):
    @commands.command(pass_context=True)
    async def removerole(self,ctx):
    @commands.command(pass_context=True)
    async def renamerole(self,ctx):
    @commands.command(pass_context=True)
    async def removeallroles(self,ctx):
    @commands.command(pass_context=True)
    async def createrole(self,ctx):
    @commands.command(pass_context=True)
    async def deleterole(self,ctx):
    @commands.command(pass_context=True)
    async def rolehoist(self,ctx):
    @commands.command(pass_context=True)
    async def rolecolor(self,ctx):
    @commands.command(pass_context=True)
    async def asar(self,ctx):
    @commands.command(pass_context=True)
    async def rsar(self,ctx):
    @commands.command(pass_context=True)
    async def iam(self,ctx):
    @commands.command(pass_context=True)
    async def lsar(self,ctx):
    @commands.command(pass_context=True)
    async def togglexclsar(self,ctx):
    @commands.command(pass_context=True)
    async def die(self,ctx):
    @commands.command(pass_context=True)
    async def restart(self,ctx):
    @commands.command(pass_context=True)
    async def setstatus(self,ctx):
    @commands.command(pass_context=True)
    async def greet(self,ctx):
    @commands.command(pass_context=True)
    async def greetmsg(self,ctx):
    @commands.command(pass_context=True)
    async def greetdm(self,ctx):
    @commands.command(pass_context=True)
    async def greetdmmsg(self,ctx):
    @commands.command(pass_context=True)
    '''






def setup(client):
    client.add_cog(Administration(client))