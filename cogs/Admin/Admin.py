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
from core.helper import permission
from db import database

default_ban_message = 'You have been banned, '
default_kick_message = ' has been kicked.'
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




class ServerTools:
    __slots__ = ('bot','guild','channel','emoteroles','reportlogs','greetmsg','greetdmmsg')

    def __init__(self,ctx):
        self.bot = ctx.bot
        self.guild = ctx.guild
        self.channel = ctx.channel
        self.emoteroles = {}
        self.reportlogs={}
        self.greetmsg = [0,"Welcome to the server!",None]
        self.greetdmmsg = [0,"Psst. Welcome! :3",None]


class Admin(commands.Cog):

    __slots__ = ('bot','tools')
    def __init__(self,bot):
        self.bot = bot
        self.tools = {}

    @commands.Cog.listener()
    async def on_member_join(self,member):
        guild = member.guild
        try:
            tool = self.tools[guild.id]
            greet = tool.greetmsg
            greetdm = tool.greetdmmsg

            if greet[0] == 1:
                channel = guild.get_channel(greet[2])
                await channel.send(greet[1])

            if greetdm[0] == 1:
                await member.send(greetdm[1])

        except KeyError:
            print('KeyError. Run normally')




    def get_tools(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            tool = self.tools[ctx.guild.id]

        except KeyError:
            tool = ServerTools(ctx)
            self.tools[ctx.guild.id] = tool
        return tool



    @staticmethod
    async def errorreport(ctx, message: str, **kwargs):
        await ctx.send(message.format(**kwargs))

    @commands.command(name='createtools')
    async def createtools(self,ctx):
        tools = self.get_tools(ctx)
        print("Tools added.")

    @commands.command(name='setbotcommands')
    async def setbotcommands(self,ctx):
        """
        Sets the channel for botcommands to occur.
        """
        author = ctx.message.author
        SERVERID = str(ctx.message.guild.id)
        CHANNELID = str(ctx.message.channel.id)

        if not author.guild_permissions.administrator:
            await ctx.send('Sorry good sir, you do not have permission to modify the database!',delete_after=10)
            return
        database.set_botchannel([SERVERID,CHANNELID])
        await ctx.send("Botcommands have been set to the **{}** channel.".format(ctx.message.channel),delete_after = 10)





    @commands.command(name='addrole', pass_context=True)
    async def addrole(self, ctx, rolename: discord.Role = None,member: discord.Member = None):
        """
        Adds a role to a user.
        If the user field is left blank, it will default to the author who issued the command.
        """

        author = ctx.message.author

        if permission(ctx.message.guild.id,ctx.message.channel.id) is False:
            return await ctx.send("This channel is not allowed to have bot commands.",delete_after=10)

        if not author.guild_permissions.manage_roles:
            embed = create_embed('addrole error: No permission', 'You do not have permission to add roles.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return



        try:
            member = ctx.message.author
            await member.add_roles(rolename)
            embed = create_embed('Role successfully added!', "The **{}** role was successfully added to **@{}**.".format(rolename,member),GREEN)
            await ctx.send(embed=embed,delete_after=20)

        except discord.Forbidden:
            if not rolename:
                embed = create_embed('addrole error: Role does not exist!',"This role does not exist!",RED)
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
        author = ctx.message.author

        if member is None:
            member = ctx.message.author

        if permission(ctx.message.guild.id,ctx.message.channel.id) is False:
            return await ctx.send("This channel is not allowed to have bot commands.",delete_after=10)

        if not author.guild_permissions.manage_roles:
            embed = create_embed('delete error: No permission', 'You do not have permission to remove roles.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return

        try:
            await member.remove_roles(rolename)
            embed = create_embed('Role successfully deleted!', "The **{}** role was successfully deleted from **@{}**.".format(rolename,member),GREEN)
            await ctx.send(embed=embed,delete_after=20)

        except discord.Forbidden:
            if not rolename:
                embed = create_embed('deleterole error: Role does not exist.',"This role does not exist!",RED)
                await ctx.send(embed=embed, delete_after = 20)
            else:
                embed = create_embed('deleterole error:',NOPERMISSION.format('delete',rolename,member),RED)
                await ctx.send(embed=embed, delete_after = 20)



    @commands.command(name='kill')
    async def kill(self,ctx):
        if permission(ctx.message.guild.id,ctx.message.channel.id) is False:
            return await ctx.send("This channel is not allowed to have bot commands.",delete_after=10)
        if ctx.message.author.id == 88047132937822208:
            await ctx.send("Bot is shutting down. Good night!")
            
            exit()



        
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
        author = ctx.message.author

        if permission(ctx.message.guild.id,ctx.message.channel.id) is False:
            return await ctx.send("This channel is not allowed to have bot commands.",delete_after=10)
        
        if not author.guild_permissions.manage_roles:
            embed = create_embed('editrolecolor error: No permission', 'You do not have permission to edit roles.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return


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
    async def kick(self,ctx, user: discord.Member = None,reason: str = None):
        """
        Kicks the user if the author has admin permissions.
        Author can optionally provide a reason for the kick.


        Example:
        !kick @Lefty#6430 You're an idiot
        !kick @Lefty#6430
        """
        author = ctx.message.author
        server= ctx.guild
        if permission(ctx.message.guild.id,ctx.message.channel.id) is False:
            return await ctx.send("This channel is not allowed to have bot commands.",delete_after=10)
        if not user:
            embed = create_embed('!kick error: No member selected.', 'You did not provide a username to kick.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return
        if not author.guild_permissions.administrator:
            embed = create_embed('!kick error: No permission', 'You do not have permission to kick.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return
        if not reason:
            reason = 'No reason given.'
        try:
            await ctx.guild.kick(user,reason = reason)
            embed = create_embed('**{}** has kicked **{}**'.format(author,user), '**Reason:** {}'.format(reason),GREEN)
            await ctx.send(embed=embed,delete_after=20)
        except discord.Forbidden:
            embed = create_embed('!kick error: No permission', 'I do not have permission to kick. Try again when I have more power.',RED)
            await ctx.send(embed=embed,delete_after=20)




    @commands.command(name='ban', pass_context=True)
    async def ban(self,ctx, user: discord.Member = None,reason: str = None,days: int = 0):
        """
        Bans a user from the server. Requires both the bot and author to have admin permissions.
        Author can optionally set a reason for the ban.
        Author can optionally set a number, which will delete all messages from the user from that many days.

        Example:
        !ban @Lefty#6430 You're an idiot 3
        !ban @Lefty#6430 3
        !ban @Lefty#6430 You're an idiot
        !ban @Lefty#6430
        """
        if permission(ctx.message.guild.id,ctx.message.channel.id) is False:
            return await ctx.send("This channel is not allowed to have bot commands.",delete_after=10)
        author = ctx.message.author
        server= ctx.guild
        if not user:
            embed = create_embed('!ban error: No member selected.', 'You did not provide a username to kick.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return
        if not author.guild_permissions.administrator:
            embed = create_embed('!ban error: No permission', 'You do not have permission to ban.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return
        if not reason:
            reason = 'No reason given.'
        try:
            embed = create_embed('**{}** has banned **{}**.'.format(author,user), '**Reason:** {}'.format(reason),GREEN)
            await ctx.send(embed=embed,delete_after=20)
            await server.ban(user,reason = reason,delete_message_days = days)
        except discord.Forbidden:
            embed = create_embed('!ban error: No permission', 'I do not have permission to do this. Try again when I have more power.',RED)
            await ctx.send(embed=embed,delete_after=20)



    @commands.command(name='unban', pass_context=True)
    async def unban(self,ctx, user: discord.Member = None,reason:str = None):
        """
        Unbans a user from the server. Requires both the bot and author to have admin permissions.
        Author can optionally set a reason for the unban.

        Example:
        !unban @Lefty#6430 Hey you're pretty cool : )
        !unban @Lefty#6430
        """
        if permission(ctx.message.guild.id,ctx.message.channel.id) is False:
            return await ctx.send("This channel is not allowed to have bot commands.",delete_after=10)
        author = ctx.message.author
        server= ctx.guild
        if not user:
            embed = create_embed('!ban error: No member selected.', 'You did not provide a username to kick.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return
        if not author.guild_permissions.administrator:
            embed = create_embed('!ban error: No permission', 'You do not have permission to ban.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return
        if not reason:
            reason = 'No reason given.'
        try:
            await server.unban(user,reason = reason)
            embed = create_embed('**{}** has unbanned **{}**.'.format(author,user), '**Reason:** {}'.format(reason),GREEN)
            await ctx.send(embed=embed,delete_after=20)
        except discord.Forbidden:
            embed = create_embed('!ban error: No permission', 'I do not have permission to do this. Try again when I have more power.',RED)
            await ctx.send(embed=embed,delete_after=20)

    @commands.command(name='setemoterole', pass_context=True)
    async def setemoterole(self,ctx,emote: discord.Emoji = None,*,arg):
        """
        Attaches a role to an emote. When a user reacts with the emote, it will give them a new role.

        Example:
        !setemoterole :smORc: "King of Games"
        """


        author = ctx.message.author
        if permission(ctx.message.guild.id,ctx.message.channel.id) is False:
            return await ctx.send("This channel is not allowed to have bot commands.",delete_after=10)
        if not emote:
            embed = create_embed('setemoterole error:','You did not specify an emote.',RED)
            await ctx.send(embed=embed, delete_after = 20)
            return
        if not author.guild_permissions.administrator:
            embed = create_embed('!setemoterole error: No permission', 'You do not have permission to ban.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return

        arg = shlex.split(arg)
        roleName = arg[0]
        role = discord.utils.get(ctx.message.guild.roles, name=roleName)

        if not role:
            embed = create_embed('setemoterole error:','The role **{}** does not exist on this server.'.format(roleName),RED)
            await ctx.send(embed=embed, delete_after = 20)
            return
        tool = self.get_tools(ctx)

        try:
            roleexist = tool.emoteroles[emote.name]
            embed = create_embed('setemoterole error: Emote already set.',"Fool I have the **{}** role set to this emote already!".format(roleexist),RED)
            await ctx.send(embed=embed, delete_after = 20)

        except KeyError:
            tool.emoteroles[emote.name] = role
            embed = create_embed('Role now set!','The role **{}** can now be set by reacting with **{}**'.format(roleName,emote.name),GREEN)
            await ctx.send(embed=embed)

    @commands.command(name='removeemoterole', pass_context=True)
    async def removeemoterole(self,ctx,emote: discord.Emoji = None):
        """
        Removes a role attached to an emote.

        Example:
        !removeemoterole :smORc:
        """


        author = ctx.message.author
        if permission(ctx.message.guild.id,ctx.message.channel.id) is False:
            return await ctx.send("This channel is not allowed to have bot commands.",delete_after=10)
        if not emote:
            embed = create_embed('setemoterole error:','You did not specify an emote.',RED)
            await ctx.send(embed=embed, delete_after = 20)
            return
        if not author.guild_permissions.administrator:
            embed = create_embed('!setemoterole error: No permission', 'You do not have permission to ban.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return

        tool = self.get_tools(ctx)

        try:
            roleName = tool.emoteroles[emote.name]
            tool.emoteroles.pop(emote.name,None)
            embed = create_embed('Successfully removed ', 'The **{}** role has been removed from **{}**'.format(roleName,emote.name),GREEN)
            await ctx.send(embed=embed)

        except KeyError:
            embed = create_embed('!removeemoterole error: No role set', 'The emote does not have a role set to it!',RED)
            await ctx.send(embed=embed,delete_after=20)





    @commands.command(name='renamerole', pass_context=True)
    async def renamerole(self,ctx,*,arg):
        """
        Renames a role. Roles must be surrounded by quotes, and author must have admin privileges.

        Example:
        !renamerole "King of Games" "Queen of Games"
        """
        author = ctx.message.author
        arg = shlex.split(arg)
        if permission(ctx.message.guild.id,ctx.message.channel.id) is False:
            return await ctx.send("This channel is not allowed to have bot commands.",delete_after=10)
        if len(arg) <=1:
            embed = create_embed('renamerole error: Not enough arguments ','You must provide 2 arguments for this command.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return
        role1N = arg[0]
        role2N = arg[1]
        role1 = discord.utils.get(ctx.message.guild.roles, name=role1N)

        if not role1:
            embed = create_embed('renamerole error: ','The role **{}** does not exist on this server'.format(role1N),RED)
            await ctx.send(embed=embed,delete_after=20)
            return
        if not author.guild_permissions.administrator:
            embed = create_embed('renamerole error: No permission', 'You do not have permission to ban.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return

        await role1.edit(name = role2N)
        embed = create_embed('Role has been renamed!', 'The **{}** role has been renamed to **{}**'.format(role1N,role2N),GREEN)
        await ctx.send(embed=embed)



    @commands.command(name='greet', pass_context=True)
    async def greet(self,ctx, channelid: int = 0):
        """
        Enables the bot to greet new users.
        0 = Greet is disabled.
        1 = Greet is enabled.

        It must also take a single int, the channel ID for which channel the greet will be sent.
        The user can use the channelid command to get the ID of the channel they're in.
        """
        guild = ctx.message.guild
        channel = ctx.message.guild.get_channel(channelid)
        author = ctx.message.author
        if permission(ctx.message.guild.id,ctx.message.channel.id) is False:
            return await ctx.send("This channel is not allowed to have bot commands.",delete_after=10)
        if not author.guild_permissions.administrator:
            embed = create_embed('greet error: No permission', 'You do not have permission to modify greets',RED)
            await ctx.send(embed=embed,delete_after=20)
            return
        if not channel:
            await ctx.send("Please provide us with a channel id..")
            return

        tool = self.get_tools(ctx)
        if tool.greetmsg[0] == 0:
            tool.greetmsg[0] = 1
            tool.greetmsg[2] = channelid
            await ctx.send("Bot greeting is now enabled! Bot will currently say the following line when a user joins: **{}**".format(tool.greetmsg[1]))
        else:
            tool.greetmsg[0] = 0
            await ctx.send("Bot greeting is now disabled!")

    @commands.command(name='greetmsg', pass_context=True)
    async def greetmsg(self,ctx,*,arg):
        """Modifies the greet message."""

        author = ctx.message.author
        if permission(ctx.message.guild.id,ctx.message.channel.id) is False:
            return await ctx.send("This channel is not allowed to have bot commands.",delete_after=10)
        if not author.guild_permissions.administrator:
            embed = create_embed('greetmsg error: No permission', 'You do not have permission to modify greet messages.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return

        tool = self.get_tools(ctx)
        tool.greetmsg[1] = arg
        await ctx.send("Greet message is now set!",delete_after=20)


    @commands.command(name='greetdm', pass_context=True)
    async def greetdm(self,ctx):
        """
        Changes whether the bot will greet new users through DM.
        0 = greetdm is disabled.
        1 = greetdm is enabled.
        """

        author = ctx.message.author
        if permission(ctx.message.guild.id,ctx.message.channel.id) is False:
            return await ctx.send("This channel is not allowed to have bot commands.",delete_after=10)
        if not author.guild_permissions.administrator:
            embed = create_embed('greetdm error: No permission', 'You do not have permission to modify greet dms.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return


        tool = self.get_tools(ctx)
        if tool.greetdmmsg[0] == 0:
            tool.greetdmmsg[0] = 1
            await ctx.send("DM greeting is now enabled! Bot will currently say the following line when a user joins: **{}**".format(tool.greetdmmsg[1]))
        else:
            tool.greetdmmsg[0] = 0
            await ctx.send("Bot greeting is now disabled!")



    @commands.command(name='greetdmmsg', pass_context=True)
    async def greetdmmsg(self,ctx,*,arg):
        author = ctx.message.author
        if permission(ctx.message.guild.id,ctx.message.channel.id) is False:
            return await ctx.send("This channel is not allowed to have bot commands.",delete_after=10)
        if not author.guild_permissions.administrator:
            embed = create_embed('greetdmmsg error: No permission', 'You do not have permission to modify greet dms.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return

        tool = self.get_tools(ctx)
        tool.greetdmmsg[1] = arg
        await ctx.send("Greetdm is now set!",delete_after=20)



    '''
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
