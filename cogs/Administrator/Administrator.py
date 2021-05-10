import discord
from discord.ext.commands import Bot, has_permissions, CheckFailure, BadArgument
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
import json
from core import jsondb
from datetime import datetime



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


def logs_embed(username,date,enforcer,reason):
    embed=discord.Embed(title="**{}**'s Logs".format(username), color=0x008000)
    embed.add_field(name='Date', value=date, inline=True)
    embed.add_field(name='Enforcer', value=enforcer, inline=True)
    embed.add_field(name='Reason', value=reason, inline=True)
    return embed

def all_logs_embed(server, members, warnings):
    embed=discord.Embed(title="**{}**'s Logs".format(server), color=0x008000)
    embed.add_field(name='Members', value=members, inline=True)
    embed.add_field(name='Warnings', value=warnings, inline=True)
    return embed

class ServerTools:
    __slots__ = ('bot','guild','channel','emoteroles',
    'reportlogs','greetmsg','greetdmmsg')

    def __init__(self,bot):
        self.bot = bot
        self.guild = bot.guild
        self.channel = bot.channel
        self.emoteroles = {}
        self.reportlogs={}

        
        
        
        


class Administrator(commands.Cog):

    __slots__ = ('bot','tools',
    'users','items','shop','servers')


    def __init__(self,bot):
        self.bot = bot
        self.tools = {}

        self.users = {}
        self.items = {}
        self.shop = {}
        self.servers = {}
        



        


     





    @staticmethod
    async def errorreport(ctx, message: str, **kwargs):
        await ctx.send(message.format(**kwargs))
    
    @commands.command(name='addrole')
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, member: discord.Member = None, rolename: discord.Role = None):
        """
        Adds a role to a user.
        If the user field is left blank, it will default to the author who issued the command.
        Usage: !addrole @Lefty @King of Games
        Requirement: Both the author and bot must have admin privileges

        """

        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)

        try:
            if member is None:
                member = ctx.message.author
            await member.add_roles(rolename)
            embed = create_embed('Role successfully added!', "The **{}** role was successfully added to **@{}**.".format(rolename,member),GREEN)
            await ctx.send(embed=embed,delete_after=20)

        except discord.Forbidden:
            await ctx.send(jsondb.NOPERMISSION, delete_after = 20)

    @commands.command(name='removerole', pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def deleterole(self, ctx, member: discord.Member = None, rolename: discord.Role = None):
        """
        Deletes a role off a user.
        If user field is left blank, it will default to the author who issued the command.
        Usage: !removerole @Lefty @King of Games
        Requirement: Both the author and bot must have admin privileges
        """

        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        try:
            if member is None:
                member = ctx.message.author
            await member.remove_roles(rolename)
            embed = create_embed('Role successfully deleted!', "The **{}** role was successfully deleted from **@{}**.".format(rolename,member),GREEN)
            await ctx.send(embed=embed,delete_after=20)

        except discord.Forbidden:
            await ctx.send(jsondb.NOPERMISSION, delete_after = 20)

    # @commands.command(name='cleanmessages')
    # @commands.has_permissions(administrator=True)
    # async def clean_messages(self,ctx,amount:int = 1):
    #     """
    #     Removes messages from the channel. By default, it removes a single message. 
    #     Usage: !cleanmessages, !cleanmessages 10
    #     Requirements: Both the author and the bot must have admin privileges. 
        
    #     """
    #     await jsondb.load_servers(self)
    #     if jsondb.permission(self,ctx) is False:
    #         return await ctx.send(jsondb.NOPERMISSION)

    #     channel = ctx.message.channel


    #     try:
    #         messages = await channel.history(limit = amount).flatten()
    #         await channel.delete_messages(messages)

    #     except discord.Forbidden:
    #         await ctx.send(jsondb.NOPERMISSION, delete_after = 10)
       
    @commands.command(name='editrolecolor')
    @commands.has_permissions(administrator=True)
    async def editcolorrole(self,ctx,*,arg):
        """
        Edits the color of a role. Role name must be surrounded by parentheses.
        Role color must be in hex format.
        !Usage: !editrolecolor "King of Games" 0xc9330a
        Requirements: Both the author and the bot must have admin privileges. 
        """

        #TODO Code works, but looks gross. Fix in the future
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
         
        arg = shlex.split(arg)
        roleName = arg[0]
        roleName = discord.utils.get(ctx.message.guild.roles, name=roleName)
        color = arg[1]
        colorString = color
        color = re.search(r'^0x(?:[0-9a-fA-F]{3}){1,2}$', color)
        if not color:
            embed = create_embed('!editrolecolor error: Incorrect hex format.','You did not provide a color in its correct format.\n Format: !editrolecolor "King of Games" 0xc9330a',RED)
            await ctx.send(embed=embed, delete_after = 20)

        if roleName:
            colorString = int(colorString,16)
            colorString = discord.Colour(colorString)
            await roleName.edit(color=colorString)
            embed = create_embed('Role color changed!','I have successfully changed **{}** to the new color.'.format(roleName),GREEN)
            await ctx.send(embed=embed,delete_after=10)
        else:
            embed = create_embed('!editrolecolor error: ','The role **{}** does not exist on this server'.format(roleName),RED)
            await ctx.send(embed=embed,delete_after=10)

    @commands.command(name='kick', pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self,ctx, user: discord.Member = None,*, reason='No reason given.'):
        """
        Kicks the user from the server.
        Author can optionally provide a reason for the kick.
        Kick is logged and can be viewed at any time.

        Usage:
        !kick @Lefty#6430 You're an idiot
        !kick @Lefty#6430

        Requirements: Both the author and bot must have permissions to kick members.
        """

        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        try:
            date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            userid = str(user.id)
            jsondb.log_kick(self,ctx,userid,date,reason)
            jsondb.save_servers(self)
            await ctx.guild.kick(user,reason = reason)
            embed = create_embed('**{}** has kicked **{}**'.format(ctx.message.author,user), '**Reason:** {}'.format(reason),GREEN)
            await ctx.send(embed=embed,delete_after=10)
        except discord.Forbidden:
            await ctx.send(jsondb.NOPERMISSION,delete_after=10)

    @commands.command(name='ban', pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx, user: discord.Member = None,*, reason='No reason given.',days: int = 0):
        """
        Bans a user from the server. Requires both the bot and author to have admin permissions.
        Author can optionally set a reason for the ban.
        Author can optionally set a number, which will delete all messages from the user from that many days.

        Usage:
        !ban @Lefty#6430 You're an idiot 3
        !ban @Lefty#6430 3
        !ban @Lefty#6430 You're an idiot
        !ban @Lefty#6430

        Requirements: Both the author and bot must have permissions to ban members.
        """
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        try:
            date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            userid = str(user.id)
            jsondb.log_ban(self,ctx,userid,date,reason)
            jsondb.save_servers(self)
            embed = create_embed('**{}** has banned **{}**.'.format(ctx.message.author,user), '**Reason:** {}'.format(reason),GREEN)
            await ctx.send(embed=embed,delete_after=20)
            await ctx.guild.ban(user,reason = reason,delete_message_days = days)
        except discord.Forbidden:
            await ctx.send(jsondb.NOPERMISSION,delete_after=10)

    @commands.command(name='unban', pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self,ctx, user: discord.Member = None,*, reason='No reason given.'):
        """
        Unbans a user from the server. Requires both the bot and author to have admin permissions.
        Author can optionally set a reason for the unban.

        Usage:
        !unban @Lefty#6430 Hey you're pretty cool : )
        !unban @Lefty#6430

        Requirements: Both the author and bot must have permission to ban members. 
        """
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        try:
            await ctx.guild.unban(user,reason = reason)
            embed = create_embed('**{}** has unbanned **{}**.'.format(ctx.message.author,user), '**Reason:** {}'.format(reason),GREEN)
            await ctx.send(embed=embed,delete_after=20)
        except discord.Forbidden:
            await ctx.send(jsondb.NOPERMISSION,delete_after=20)


    @commands.command(name='warn')
    @commands.has_permissions(kick_members=True)
    async def warn(self,ctx,user: discord.Member = None, *, reason='No reason given.'):
        ''' 
        Warns a user.
        Usage: !warn @Lefty You're a jerk
        Requirement: Author must be able to kick members
        '''
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        userid = str(user.id)
        date =  datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        jsondb.log_warning(self,ctx,userid,date,reason)
        await jsondb.save_servers(self)
        await ctx.send("{} has been warned.".format(user),delete_after=10)


    
    @commands.command(name='warnlog')
    @commands.has_permissions(administrator=True)
    async def warnlog(self,ctx,user: discord.Member = None):
        '''Sees a list of warnings of a certain user.
        Usage: !warnlog @Lefty
        Requirement: Author must have admin privileges. 
        '''
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        date, enforcer, reason = jsondb.return_warning_logs(self,ctx,str(user.id))
        if date is None:
            return await ctx.send("{} has no warnings logged.".format(user))
        embed = logs_embed(user.display_name,date,enforcer,reason)
        await ctx.send(embed=embed)


    @commands.command(name='kicklog')
    @commands.has_permissions(administrator=True)
    async def kicklog(self,ctx,user: discord.Member = None):
        '''Sees a list of kicks given to certain user.
        Usage: !kicklog @Lefty
        Requirement: Author must have admin privileges. 
        '''
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        date, enforcer, reason = jsondb.return_kick_logs(self,ctx,str(user.id))
        if date is None:
            return await ctx.send("{} has no kicks logged.".format(user))
        embed = logs_embed(user.display_name,date,enforcer,reason)
        await ctx.send(embed=embed)

    @commands.command(name='banlog')
    @commands.has_permissions(administrator=True)
    async def banlog(self,ctx,user: discord.Member = None):
        '''Sees a list of bans given to a certain user.
        Usage: !banlog @Lefty
        Requirement: Author must have admin privileges. 
        '''
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        date, enforcer, reason = jsondb.return_ban_logs(self,ctx,str(user.id))
        if date is None:
            return await ctx.send("{} has no bans logged.".format(user))
        embed = logs_embed(user.display_name,date,enforcer,reason)
        await ctx.send(embed=embed)
    
    @commands.command(name='warnlogall')
    @commands.has_permissions(kick_members=True)
    async def warnlogall(self,ctx):
        '''Sees a list of all warnings on the server.
        Usage: !warnlogall
        Requirement: Author must have the ability to kick members.
        '''
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        member, warnings = jsondb.return_allwarn_logs(self,ctx)
        embed = all_logs_embed(ctx.guild.name,member,warnings)
        await ctx.send(embed=embed)
 
    @commands.command(name='warnclear')
    @commands.has_permissions(kick_members=True)
    async def warnclear(self,ctx,user: discord.Member = None, clear: int = 0):
        '''
        Clears all warnings from a certain user. You can specify a number to clear a specific one.
        Usage: !warnclear @lefty 3
        !warnclear @lefty
        Requirement: Author must have the ability to kick members.
        '''
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        try:
            if clear-1 < 0:
                return await ctx.send("{} has no warnings at that location.".format(user.name))
            self.servers[str(ctx.guild.id)]['Warnings'][str(user.id)].pop(clear-1)
            await jsondb.save_servers(self)
            return await ctx.send("Warning has been deleted.")
        except IndexError:
            return await ctx.send("{} has no warnings at that location.".format(user.name))

 

    @commands.command(name='setbotcommands')
    @commands.has_permissions(administrator=True)
    async def setbotcommands(self,ctx):
        """
        Sets the channel for botcommands to occur.
        """

        serverid = str(ctx.message.guild.id)
        channelid = str(ctx.channel.id)
        await jsondb.load_servers(self)
        try:
            server = self.servers[serverid]
            for cid in server['Channel_Permissions']:
                if cid == channelid:
                    return await ctx.send("This channel already has permission to use bot commands.",delete_after = 10)
            server['Channel_Permissions'].append(channelid)
            await jsondb.save_servers(self)
            await ctx.send("**{}** channel is now allowed to bot commands.".format(ctx.message.channel),delete_after = 10)
        except KeyError:
            return await ctx.send("Server info has not been created yet. Use the **!createserverinfo** command first.")

    
    @commands.command(name='createserverinfo')
    @commands.has_permissions(administrator=True)
    async def createserverinfo(self,ctx):
        '''
        Creates basic info for the server. This command must be used in order to use LuigiBot.
        Usage: !createserverinfo
        Requirement: Admin privileges
        '''
        await jsondb.load_servers(self)
        server = ctx.guild
            
        if str(server.id) not in self.servers:
            self.servers[str(server.id)] = {
                'Server_Name': server.name,
                'Server_Owner': server.owner.name, 
                'Server_Info':'',
                'User_Count': len(server.members),
                'Warnings': {},
                'Kicks':{},
                'Bans':{},
                'Channel_Permissions':[],
                "Greets":{
                    "Enabled": 0,
                    "Greet_Channel": "",
                    "Greet_Message": "Welcome to the server!"
                },
                'Reaction_Messages':{}
            }
            await jsondb.save_servers(self)
            return await ctx.send("Server info has been created for **{}**.".format(server.name))
        else:
            return await ctx.send("Server info has already been created. Use **!serverinfo** to see it, and **!serverhelp** to see how to modify it.")
        

    @commands.command(name='reactionroles')
    @commands.has_permissions(administrator=True)
    async def reactionroles(self,ctx,*,args):
        '''
        Specify role names and server emojis with which they're represented, 
        the bot will then add those emojis to the previous message in the channel, 
        and users will be able to get the roles by clicking on the emoji.

        Usage: !reactionroles king of games :clap:; queen of games :cowboy:;
        '''
        
        arg = args.split(';')
        print(arg)
        for reaction in arg:
            reactionlist = reaction.split('<')
            print(reactionlist)

    
    @commands.command(name="kill")
    @commands.is_owner()
    async def shutdown(self,ctx):
        await ctx.bot.logout()

        





    @commands.command(name='greet')
    @commands.has_permissions(administrator=True)
    async def greet(self,ctx):
        '''Enables or disables the bot from greeting a user. When the bot is enabled, the greet message will be sent on whatever channel the command was used.
        Usage: !greet
        Requirements: Author must have admin privileges.'''

        await jsondb.load_servers(self)
        server = str(ctx.guild.id)
        try:
            if self.servers[server]['Greets']['Enabled'] == 0 or self.servers[server]['Greets']['Enabled'] == 2:
                self.servers[server]['Greets']['Enabled'] = 1
                self.servers[server]['Greets']['Greet_Channel'] = str(ctx.channel.id)
                await jsondb.save_servers(self)
                return await ctx.send("Greets have now been enabled, and will be sent out on this channel.")
            else:
                self.servers[server]['Greets']['Enabled'] = 0
                self.servers[server]['Greets']['Greet_Channel'] = ''
                await jsondb.save_servers(self)
                return await ctx.send("Greets have now been disabled.")
        except KeyError:
            return await ctx.send("Your server info could not be found. Use the **!createserverinfo** command to get started.")

    @commands.command(name='greetdm')
    @commands.has_permissions(administrator=True)
    async def greetdm(self,ctx):
        '''Enables or disables the bot from greeting new users through direct messaging. 
        Usage: !greetdm
        Requirements: Author must have admin privileges.'''

        await jsondb.load_servers(self)
        server = str(ctx.guild.id)
        try:
            if self.servers[server]['Greets']['Enabled'] == 0 or self.servers[server]['Greets']['Enabled'] == 1:
                self.servers[server]['Greets']['Enabled'] = 2
                await jsondb.save_servers(self)
                return await ctx.send("Greetdm has now been enabled.")
            else:
                self.servers[server]['Greets']['Enabled'] = 0
                self.servers[server]['Greets']['Greet_Channel'] = ''
                await jsondb.save_servers(self)
                return await ctx.send("Greets have now been disabled.")
        except KeyError:
            await ctx.send("Your server info could not be found. Use the **!createserverinfo** command to get started.")

    @commands.command(name='greetmsg')
    @commands.has_permissions(administrator=True)
    async def greetmsg(self,ctx,*,message = ''):
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        
        self.servers[str(ctx.guild.id)]['Greets']['Greet_Message'] = message
        await jsondb.save_servers(self)
        await ctx.send("Greet message has been saved!")

    @commands.command(name='info')
    async def info(self,ctx,user: discord.Member = None):
        '''
        Gets the basic info of a user. If no user is provided, returns author's info.
        Usage: !info, !info @Lefty
        Requirements: None
        '''

    @commands.command(name='uptime')
    async def uptime(self,ctx):
        '''
        Shows LuigiBot's uptime on the server.
        Usage: !uptime
        Requirements: None
        '''

    @commands.Cog.listener()
    async def on_member_join(self,user):
        server = str(user.guild.id)
        guild = user.guild
        await jsondb.load_servers(self)
        try:
            if self.servers[server]['Greets']['Enabled'] == 1:
                channel = guild.get_channel(int(self.servers[server]['Greets']['Greet_Channel']))
                await channel.send(self.servers[server]['Greets']['Greet_Message'])
            elif(self.servers[server]['Greets']['Enabled']==2):
                await user.send(self.servers[server]['Greets']['Greet_Message'])           
        except KeyError:
            print('KeyError. Run normally')


    











    '''
    
    def get_tools(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            tool = self.tools[ctx.guild.id]

        except KeyError:
            tool = ServerTools(ctx)
            self.tools[ctx.guild.id] = tool
        return tool3
    @commands.command(name='setemoterole', pass_context=True)
    async def setemoterole(self,ctx,emote: discord.Emoji = None,*,arg):
        """
        Attaches a role to an emote. When a user reacts with the emote, it will give them a new role.

        Example:
        !setemoterole :smORc: "King of Games"
        """


        author = ctx.message.author
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        serverid = str(ctx.guild.id)
        channelid = str(ctx.channel.id)
        
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
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        serverid = str(ctx.guild.id)
        channelid = str(ctx.channel.id)
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
        serverid = str(ctx.guild.id)
        channelid = str(ctx.channel.id)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
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
    async def greet(self,ctx):
        """
        Enables the bot to greet new users.
        0 = Greet is disabled.
        1 = Greet is enabled.

        It must also take a single int, the channel ID for which channel the greet will be sent.
        The user can use the channelid command to get the ID of the channel they're in.
        """
        channelid = ctx.channel.id
        channel = ctx.message.guild.get_channel(channelid)
        author = ctx.message.author
        serverid = ctx.message.guild.id
        await self.load_servers(self)
        serverid = str(ctx.guild.id)
        channelid = str(ctx.channel.id)
        try:
            if self.servers[serverid]['Channelid'] != channelid:
                return await ctx.send("This channel is not allowed to have bot commands.",delete_after=10)
        except KeyError:
            return await ctx.send("You have not set a channel for botcommands.",delete_after=10)
        if not author.guild_permissions.administrator:
            embed = create_embed('greet error: No permission', 'You do not have permission to modify greets',RED)
            await ctx.send(embed=embed,delete_after=20)
            return
        if not channel:
            await ctx.send("Please provide us with a channel id..")
            return


        greetmsg = database.get_greet(serverid)
        if not greetmsg:
            database.create_greet([serverid,channelid])
            await ctx.send("Bot greeting is now enabled!")
            print('if')
            #await ctx.send("Bot greeting is now enabled! Bot will currently say the following line when a user joins: **{}**".format(greetmsg[1]))
        else:
            print(greetmsg)
            if greetmsg[0] == 1:
                update = [serverid,0]
                database.update_greet(update)
                await ctx.send("Bot greeting is now disabled!")
                print('else1')
            elif greetmsg[0] == 0:
                update = [serverid,1]
                database.update_greet(update)
                await ctx.send("Bot greeting is now enabled!")
                print('else2')
        print('end')
    @commands.command(name='greetmsg', pass_context=True)
    async def greetmsg(self,ctx,*,arg):
        """Modifies the greet message."""

        author = ctx.message.author
        await self.load_servers(self)
        serverid = str(ctx.guild.id)
        channelid = str(ctx.channel.id)
        try:
            if self.servers[serverid]['Channelid'] != channelid:
                return await ctx.send("This channel is not allowed to have bot commands.",delete_after=10)
        except KeyError:
            return await ctx.send("You have not set a channel for botcommands.",delete_after=10)
        if not author.guild_permissions.administrator:
            embed = create_embed('greetmsg error: No permission', 'You do not have permission to modify greet messages.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return

        serverid = ctx.guild.id
        msg = arg
        database.update_greetmsg([serverid,msg])
        await ctx.send("Greet message is now set!",delete_after=20)
    @commands.command(name='greetdm', pass_context=True)
    async def greetdm(self,ctx):
        """
        Changes whether the bot will greet new users through DM.
        0 = greetdm is disabled.
        1 = greetdm is enabled.
        """
        channelid = ctx.channel.id
        author = ctx.message.author
        serverid = ctx.guild.id

        await self.load_servers(self)
        serverid = str(ctx.guild.id)
        channelid = str(ctx.channel.id)
        try:
            if self.servers[serverid]['Channelid'] != channelid:
                return await ctx.send("This channel is not allowed to have bot commands.",delete_after=10)
        except KeyError:
            return await ctx.send("You have not set a channel for botcommands.",delete_after=10)
        if not author.guild_permissions.administrator:
            embed = create_embed('greetdm error: No permission', 'You do not have permission to modify greet dms.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return


        serverid = ctx.guild.id
        greetdm = database.get_greetdm(serverid)
        if not greetdm:
            database.create_greet([serverid,channelid])
            update = [serverid,1]
            database.update_greetdm(update)
            await ctx.send("DM Greeting is now enabled!")
            #await ctx.send("DM Greeting is now enabled! Bot will currently say the following line when a user joins: **{}**".format(greetmsg[1]))
        else:
            if greetdm[0] == 1:
                update = [serverid,0]
                database.update_greetdm(update)
                await ctx.send("DM Greets are now disabled!")
            elif greetdm[0] == 0:
                update = [serverid,1]
                database.update_greetdm(update)
                await ctx.send("DM Greets are now enabled!")
    @commands.command(name='greetdmmsg', pass_context=True)
    async def greetdmmsg(self,ctx,*,arg):
        author = ctx.message.author
        await self.load_servers(self)
        serverid = str(ctx.guild.id)
        channelid = str(ctx.channel.id)
        try:
            if self.servers[serverid]['Channelid'] != channelid:
                return await ctx.send("This channel is not allowed to have bot commands.",delete_after=10)
        except KeyError:
            return await ctx.send("You have not set a channel for botcommands.",delete_after=10)
        if not author.guild_permissions.administrator:
            embed = create_embed('greetdmmsg error: No permission', 'You do not have permission to modify greet dms.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return

        serverid = ctx.guild.id
        msg = arg
        #database.update_greetdmmsg([serverid,msg])
        await ctx.send("Greetdm is now set!",delete_after=20)
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






    '''
