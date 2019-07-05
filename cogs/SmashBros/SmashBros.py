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
import json

RED = 0xc9330a
GREEN = 0x16820d
Smash_Characters = ['Mario','Luigi','Peach','Bowser','Dr.Mario','Rosalina & Luma','Bowser Jr.','Yoshi','ZSS','Jiggs','MK','dedede','ddd','trainer,'
                            'Donkey Kong','Diddy Kong','Link','Zelda','Sheik','Young Link','Ganondorf','Toon Link','Falcon','Wii Fit','Mii',
                            'Samus','Zero Suit Samus','Kirby','Meta Knight','King Dedede','Fox','Falco','Wolf',
                            'Pikachu','Jigglypuff','Pichu','Mewtwo','Pokemon Trainer',
                            'Lucario','Greninja','Captain Falcon','Ness','Lucas','Ice Climbers','Marth','Roy',
                            'Ike','Lucina','Robin','Corrin','Mr.Game&Watch','Pit','Palutena','Dark Pit',
                            'Wario','Olimar','ROB','R.O.B.','Villager','Wii Fit Trainer','Little Mac','Shulk','Duck Hunt',
                            'Snake','Sonic','Mega Man','Pac-Man','Ryu','Cloud','Bayonetta', 'Pac Man' 'Pacman', 'King k rool','King K Rool'
                            'Mii Brawler','Mii Swordfighter','Mii Gunner','Daisy','Piranha Plant','King K. Rool',
                            'Ridley','Dark Samus','Incineroar','Chrom','Isabelle','Inkling','Ken','Simon','Richter',
                            'Joker','Hero','Banjo & Kazooie','Banjo','Banjo-Kazooie','Belmont','MegaMan']





def create_embed(atitle,adescription,color):
    embed = discord.Embed(
                title = atitle,
                description = adescription,
                colour = color)
    return embed

def csmash_embed(name,switchcode,main,servername):
    embed=discord.Embed(title="**{}** Smash Players!".format(servername), color=0x008000)
    embed.add_field(name='Player', value=name, inline=True)
    embed.add_field(name='Switch Code', value=switchcode, inline=True)
    embed.add_field(name='Main', value=main, inline=True)



    return embed
def profile_embed(name,switchcode,main,secondaries):
    embed=discord.Embed(title="Smash Profiles", description="Smash Players on this Server!", color=0x008000)
    embed.add_field(name='Player', value=name, inline=True)
    embed.add_field(name='Switch Code', value=switchcode, inline=True)
    embed.add_field(name='Main', value=main, inline=True)
    embed.add_field(name='Secondaries', value=secondaries, inline=True)
    return embed


def fix_switch_code(switchcode):
    block1 = switchcode[0:4]
    block2 = switchcode[4:8]
    block3 = switchcode[8:12]
    switchcode = "SW-"+block1+"-"+block2+"-"+block3
    return switchcode

def check_smash_character(smash_character):
    if smash_character not in Smash_Characters:
        return None
    else:
        return smash_character
def check_secondaries(secondaries):
    secondariesList = []
    for secondary in secondaries:
        if secondary in Smash_Characters:
            secondariesList.append(secondary)
    return secondariesList







class SmashTools:
    __slots__ = ('bot','guild','channel','smashprofiles','smashresources')
    def __init__(self,ctx):
        self.bot = ctx.bot
        self.guild = ctx.guild
        self.channel = ctx.channel

        





class SmashBros(commands.Cog):
    __slots__ = ('bot','tools')
    def __init__(self,bot):
        self.bot = bot
        self.tools = {}

        with open(r"C:\Users\Lefty\Desktop\LuigiBot\cogs\Economy\NewUsers.json",'r') as f:
            self.users = json.load(f)
        with open(r"C:\Users\Lefty\Desktop\LuigiBot\cogs\Economy\NewItems.json",'r') as f:
            self.items = json.load(f)
        with open(r"C:\Users\Lefty\Desktop\LuigiBot\cogs\Economy\NewShop.json",'r') as f:
            self.shop = json.load(f)
        with open(r"C:\Users\Lefty\Desktop\LuigiBot\cogs\Economy\ServerPermissions.json",'r') as f:
            self.servers = json.load(f)

    async def save_users(self,ctx):
        with open(r"C:\Users\Lefty\Desktop\LuigiBot\cogs\Economy\NewUsers.json",'w') as f:
            json.dump(self.users,f,indent=4)
    async def save_items(self,ctx):
        with open(r"C:\Users\Lefty\Desktop\LuigiBot\cogs\Economy\NewItems.json",'w') as f:
            json.dump(self.items,f,indent=4)
    async def save_shop(self,ctx):
        with open(r"C:\Users\Lefty\Desktop\LuigiBot\cogs\Economy\NewShop.json",'w') as f:
            json.dump(self.shop,f,indent=4)
    async def save_servers(self,ctx):
        with open(r"C:\Users\Lefty\Desktop\LuigiBot\cogs\Economy\ServerPermissions.json",'w') as f:
            json.dump(self.servers,f,indent=4)

    
    async def load_users(self,ctx):
        with open(r"C:\Users\Lefty\Desktop\LuigiBot\cogs\Economy\NewUsers.json",'r') as f:
            self.users = json.load(f)
    async def load_items(self,ctx):
        with open(r"C:\Users\Lefty\Desktop\LuigiBot\cogs\Economy\NewItems.json",'r') as f:
            self.items = json.load(f)
    async def load_shop(self,ctx):
        with open(r"C:\Users\Lefty\Desktop\LuigiBot\cogs\Economy\NewShop.json",'r') as f:
            self.shop = json.load(f)
    async def load_servers(self,ctx):
        with open(r"C:\Users\Lefty\Desktop\LuigiBot\cogs\Economy\ServerPermissions.json",'r') as f:
            self.servers = json.load(f)





    def get_tools(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            tool = self.tools[ctx.guild.id]
        except KeyError:
            tool = SmashTools(ctx)
            self.tools[ctx.guild.id] = tool
        return tool






    @commands.command(name='setsmash',pass_context = True)
    async def createsmashprofile(self,ctx,*,arg):
        '''
Create a smash profile on the server. Arguments are semicolon separated, and are case sensitive for smash characters. 
Note: Do not end the command with a semicolon.

Usage:
!setsmash 111122223333;Luigi;Fox
        '''
        await self.load_users(self)

        author = ctx.message.author
        server = ctx.message.guild.id
        #arg = shlex.split(arg)
        arg = arg.split(';')

        if len(arg)<2:
            embed = create_embed('!setsmash Error: Not enough arguments ','You must provide at least 2 arguments for this command.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return


        switchcode = arg[0]
        if len(switchcode)!=12:
            embed = create_embed('!setsmash error: Bad Switch Code ','The length of a switch code is 12 digits.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return
        else:
            switchcode = fix_switch_code(switchcode)

        main = arg[1]
        main = check_smash_character(main)
        if not main:
            embed = create_embed('!setsmash error: Incorrect format for main. ','You did not input a smash character. Try the sschar command to see correct format.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return
        if len(arg)==2:
            secondaries = '--'
        else:
            secondaries = arg[2:]
            secondaries = check_secondaries(secondaries)
            if not secondaries:
                secondaries = '--'
        name = author.name + "@" + author.discriminator
        user = self.users[str(ctx.author.id)]
        user['SmashProfile']['Name'] = name
        user['SmashProfile']['SwitchCode'] = switchcode
        user['SmashProfile']['Main'] = main
        user['SmashProfile']['Secondaries'] = secondaries
        await self.save_users(self)
        await ctx.send('Profile created!')

    @commands.command(name='smashprofiles',pass_context = True)
    async def viewprofiles(self,ctx):
        '''
Shows all of the smash profiles currently on the server.
Usage: 
!smashprofiles
        '''
        await self.load_users(self)
        server = ctx.message.guild
        members = ctx.guild.members


        name = ""
        switchcode = ""
        main = ""

        for member in members:
            try:
                memberid = str(member.id)
                if self.users[memberid]['SmashProfile']['Name'] is None:
                    continue
                name = name + self.users[memberid]['SmashProfile']['Name'] + "\n"
                switchcode = switchcode + self.users[memberid]['SmashProfile']['SwitchCode'] + "\n"
                main = main + self.users[memberid]['SmashProfile']['Main'] + "\n"
            except KeyError:
                continue
  

        embed = csmash_embed(name,switchcode,main,server.name)
        await ctx.send(embed=embed)



    @commands.command(name='smash',pass_context = True)
    async def smashprofile(self,ctx, user:discord.Member = None):
        """
Shows the smash profile of a user. If no user is specified, it will attempt to show the profile of the author.
Usage:
!smash 
!smash @Lefty#6430
        """
        await self.load_users(self)
        if user is None:
            username = ctx.author
            userid = str(ctx.author.id)
        else:
            username = user
            userid = str(user.id)
        name = self.users[userid]['SmashProfile']['Name']
        if not name:
            return await ctx.send("**{}** does not have a profile!".format(username))
        switchcode = self.users[userid]['SmashProfile']['SwitchCode']
        main = self.users[userid]['SmashProfile']['Main']
        secondarylist = self.users[userid]['SmashProfile']['Secondaries']
        secondaries = ''
        for secondary in secondarylist:
            secondaries =secondaries + secondary + ', '
        embed = profile_embed(name,switchcode,main,secondaries)
        await ctx.send(embed=embed)




    @commands.command(name='smashcode',pass_context = True)
    async def switchcode(self,ctx,*,arg):
        '''
        Modifies the switchcode of the author. Requires a 12 digit switchcode.

        Usage:
        !switchcode 123412341234
        '''
        await self.load_users(self)
        arg = shlex.split(arg)
        switchcode = arg[0]
        if len(switchcode)!=12:
            embed = create_embed('smashcode error: Bad Switch Code ','The length of a switch code is 12 digits.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return
        else:
            switchcode = fix_switch_code(switchcode)
        
        userid = str(ctx.author.id)
        name = self.users[userid]['SmashProfile']['Name']
        if not name:
            return await ctx.send("**{}**, you do not have a profile!".format(ctx.author))
        self.users[userid]['SmashProfile']['SwitchCode'] = switchcode
        await self.save_users(self)
        await ctx.send('**{}** has modified their switchcode!'.format(ctx.author))
        


    @commands.command(name='smashmain',pass_context = True)
    async def smashmain(self,ctx,*,arg):
        '''
        Modifies the smash main of the author. Case sensitive. Use !smash characters to see the character format.

        Usage:
        !smashmain Luigi
        '''
        await self.load_users(self)
        author = ctx.message.author
        name = author.name + "@" + author.discriminator
        arg = shlex.split(arg)
        main = arg[0]

        main = check_smash_character(main)
        if not main:
            embed = create_embed('smashmain error: Incorrect format for main. ','You did not input a smash character. Try the sschar command to see correct format.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return


        userid = str(ctx.author.id)
        name = self.users[userid]['SmashProfile']['Name']
        if not name:
            return await ctx.send("**{}**, you do not have a profile!".format(ctx.author))
        self.users[userid]['SmashProfile']['Main'] = main
        await self.save_users(self)
        await ctx.send('**{}** has modified their main!'.format(ctx.author))


    @commands.command(name='smashsecond',pass_context = True)
    async def secondaries(self,ctx,*,arg=''):
        '''
        Modifies the smash secondaries of the author. Case sensitive. Use !smashcharacters to see the character format.

        Usage:
        !smashsecond Luigi;Mario;Fox
        !smashsecond
        '''
        await self.load_users(self)
        arg = arg.split(';')
        secondarylist = check_secondaries(arg)
        if not secondarylist:
            secondarylist = ['--']
        userid = str(ctx.author.id)
        name = self.users[userid]['SmashProfile']['Name']
        if not name:
            return await ctx.send("**{}**, you do not have a profile!".format(ctx.author))
        self.users[userid]['SmashProfile']['Secondaries'] = secondarylist
        await self.save_users(self)
        await ctx.send('**{}** has modified their secondaries!'.format(ctx.author))

    @commands.command(name='deletesmash',pass_context = True)
    async def smash_delete(self,ctx,user: discord.Member = None):
        '''
        Deletes the smash profile of the author. If a user is specified, then the author requires admin privileges. 

        Usage:
        !deletesmash
        !deletesmash @Lefty#6430
        '''
        await self.load_users(self)
        if not ctx.author.guild_permissions.administrator:
                embed = create_embed('!deletesmash error: No permission.', 'You must have admin privileges to do this command',GREEN)
                await ctx.send(embed=embed,delete_after=20)
                return
        
        if user is None:
            userid = ctx.author.id
        else:
            userid = user.id
        self.users[userid]['SmashProfile'] = { 'Name':'' ,
                                    'SwitchCode': '',
                                    'Main': '',
                                    'Secondaries': []
        }
        await self.save_users
        await ctx.send("**{}**'s Smash Profile has been wiped.")
            

            

    @commands.cooldown(1,20,commands.BucketType.guild)
    @commands.command(name='smashcharacters',pass_context = True)
    async def smash_characters(self,ctx):
        '''
        List all the smash characters you can enter when creating and modifying a smash profile.

        Usage:
        !smashcharacters
        '''
        label = 1
        List = ""
        for item in Smash_Characters:
            Labelstr = str(label)
            List = List + Labelstr + ". " + item + "\n"
            label = label +1

        embed = create_embed("Smash Characters Format",List,GREEN)
        await ctx.send(embed=embed, delete_after=15)


    
