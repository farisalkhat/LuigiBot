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

default_ban_message = 'You have been banned, '
default_kick_message = ' has been kicked.'
king_of_games= '144694253631700992'
smuckers_goober = '144697844110983168'
admins = [king_of_games,smuckers_goober]
kick_reason = 'not specified.'


serverAdmins = {}


NOPERMISSION = ("I attempted to {} the **{}** role to **@{}**, "
"but I do not have the permission to do so."
"Please try again when I have more power.")

INVALIDROLE = ("Sorry sir! The **{}** role does not exist on this server!")



        
RED = 0xc9330a
GREEN = 0x16820d



def create_embed(atitle,adescription,color):
    embed = discord.Embed(
                title = atitle,
                description = adescription,
                colour = color)
    return embed


    


class Admin(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @staticmethod
    async def errorreport(ctx, message: str, **kwargs):
        await ctx.send(message.format(**kwargs))
        
        
    @commands.command(name='addrole', pass_context=True)
    async def addrole(self, ctx, rolename: discord.Role = None,member: discord.Member = None):
        """
        Adds a role to a user.
        If the user field is left blank, it will default to the author who issued the command.
        """
        try: 
            member = ctx.message.author
            await member.add_roles(rolename)
            embed = create_embed('Role successfully added!', "The **{}** role was successfully added to **@{}**.".format(rolename,member),GREEN)
            await ctx.send(embed=embed,delete_after=20)

        except discord.Forbidden:
            if not rolename:
                embed = create_embed('addrole error:',NOPERMISSION.format(rolename,RED))
                await ctx.send(embed=embed, delete_after = 20)
            else:
                embed = create_embed('addrole error:',NOPERMISSION.format('add',rolename,member),RED)
                await ctx.send(embed=embed, delete_after = 20)


    
    @commands.command(name='deleterole', pass_context=True)
    async def deleterole(self, ctx, rolename: discord.Role = None, member: discord.Member = None):
        """
        Deletes a role off a user.
        If user field is left blank, it will default to the author who issued the command.
        """

        if member is None:
            member = ctx.message.author

        try: 
            await member.remove_roles(rolename)
            embed = create_embed('Role successfully deleted!', "The **{}** role was successfully deleted from **@{}**.".format(rolename,member),GREEN)
            await ctx.send(embed=embed,delete_after=20)

        except discord.Forbidden:
            if not rolename:
                embed = create_embed('deleterole error:',NOPERMISSION.format(rolename,RED))
                await ctx.send(embed=embed, delete_after = 20)
            else:
                embed = create_embed('deleterole error:',NOPERMISSION.format('delete',rolename,member),RED)
                await ctx.send(embed=embed, delete_after = 20)

                
        
    @commands.command(name='editrolecolor', pass_context=True)
    async def editcolorrole(self,ctx,*,arg):
        """
        Edits the color of a role. Role name must be surrounded by parentheses.
        Role color must be in hex format.

        Example:
        !editrolecolor "King of Games" 0xc9330a
        """
        
        arg = shlex.split(arg)
        roleName = arg[0]
        roleName = discord.utils.get(ctx.message.guild.roles, name=roleName)


        color = arg[1]
        colorString = color
        color = re.search(r'^0x(?:[0-9a-fA-F]{3}){1,2}$', color)
        if not color:
            embed = create_embed('!editrolecolor error: Incorrect hex format.','You did not provide a color in its correct format.\n Format: !editrolecolor "King of Games" 0xc9330a',RED)
            await ctx.send(embed=embed, delete_after = 20)

        elif(roleName):
            colorString = int(colorString,16)
            colorString = discord.Colour(colorString)
            print(colorString)
            await roleName.edit(color=colorString)
            embed = create_embed('Role color changed!','I have successfully changed **{}** to the new color.'.format(roleName),GREEN)  
            await ctx.send(embed=embed,delete_after=20)
        else:
            embed = create_embed('!editrolecolor error: ','The role **{}** does not exist on this server'.format(roleName),RED)
            await ctx.send(embed=embed,delete_after=20)
            












    
    @commands.command(name='kick', pass_context=True)
    async def kick(self,ctx, user: discord.Member = None,*,arg=None):

        author = ctx.message.author
        server= ctx.guild
        if not arg:
            arg = 'No reason given.'
        if not user:
            embed = create_embed('!kick error: No member selected.', 'You did not provide a username to kick.',RED)
            await ctx.send(embed=embed,delete_after=20)
        if not author.guild_permissions.administrator:
            embed = create_embed('!kick error: No permission', 'You do not have permission to kick.',RED)
            await ctx.send(embed=embed,delete_after=20)
        embed = create_embed('**{}** has kicked **{}**'.format(author,user), '**Reason:** {}'.format(arg),GREEN)
        
        await ctx.send(embed=embed,delete_after=20)
        await ctx.guild.kick(user,reason = arg)
        
        
    '''    
    @commands.command(name='editrolecolor', pass_context=True)
    async def ban(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def unban(self,ctx,*,arg):
        
    @commands.command(name='editrolecolor', pass_context=True)
    async def setemoterole(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def renamerole(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def removeallroles(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def mentionrole(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def autoassignrole(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def logevents(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def prune(self,ctx,*,arg):
    
    async def setmuterole(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def mute(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def unmute(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def chatmute(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def chatunmute(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def voicemute(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def voiceunmute(self,ctx,*,arg):



    @commands.command(name='editrolecolor', pass_context=True)
    async def reactionroles(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def reactionroleslist(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def reactionrolesremove(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def voiceunmute(self,ctx,*,arg):

    @commands.command(name='editrolecolor', pass_context=True)
    async def setbotname(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def restart(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def setbotstatus(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def setbotavatar(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def setbotgame(self,ctx,*,arg):

        




    @commands.command(name='editrolecolor', pass_context=True)
    async def greet(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def greetmsg(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def greetdm(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def greetdmmsg(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def bye(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def byemsg(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def byedel(self,ctx,*,arg):


        
    @commands.command(name='editrolecolor', pass_context=True)
    async def warn(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def warnlog(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def warnlogall(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def warnclear(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def warnpunish(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def warnpunishlist(self,ctx,*,arg):


    @commands.command(name='editrolecolor', pass_context=True)
    async def delvoichanl(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def createvoichanl(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def deltxtchanl(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def creatxtchanl(self,ctx,*,arg):
    @commands.command(name='editrolecolor', pass_context=True)
    async def setchanlname(self,ctx,*,arg):
    '''
