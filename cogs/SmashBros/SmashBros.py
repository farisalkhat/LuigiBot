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
import json
from core import jsondb

RED = 0xc9330a
GREEN = 0x16820d

Smash_Characters = {'Mario','Luigi','Peach','Bowser','Dr.Mario','RosaLuma','Bowser Jr','Yoshi','ZSS',
                            'Donkey Kong','Diddy Kong','Link','Zelda','Sheik','Young Link','Ganondorf','Toon Link',
                            'Samus','ZSS','Kirby','Meta Knight','King Dedede','Fox','Falco','Wolf',
                            'Pikachu','Jigglypuff','Pichu','Mewtwo','Pokemon Trainer',
                            'Lucario','Greninja','Falcon','Ness','Lucas','Ice Climbers','Marth','Roy',
                            'Ike','Lucina','Robin','Corrin','G&W','Pit','Palutena','Dark Pit',
                            'Wario','Olimar','ROB','Villager','Wii Fit Trainer','Little Mac','Shulk','Duck Hunt',
                            'Snake','Sonic','Megaman','Pacman','Ryu','Cloud','Bayonetta',
                            'Mii Brawler','Mii Swordfighter','Mii Gunner','Daisy','Piranha Plant','King K Rool',
                            'Ridley','Dark Samus','Incineroar','Chrom','Isabelle','Inkling','Ken','Simon','Richter',
                            'Joker','Hero','Banjo','Megaman'}




def check_embed_limits(embed):
    '''
    Embeds have limits to how many characters can be returned. 

    Title = 256 characters
    Description = 2048 characters
    Fields = Max 25 fields
    Field name = 256 characters
    Field value = 1024 characters
    Footer text = 2048 characters
    Author name = 256 characters

    Sum of all characters cannot exceed 6000 characters. 

    This will check if the limit is broken. 
    It will return true if the limit is broken.
    Otherwise, it will return false.
    '''
    totalChar = 0


    
    if len(embed.title)>256:
        return True
    totalChar = totalChar + len(embed.title)
    fields = embed.fields

    if len(fields)> 25:
        return True

    for field in fields:
        if len(field.name)>256:
            return True
        if len(field.value)>1024:
            return True
        totalChar = totalChar + len(field.name) + len(field.value)

    print(totalChar)
    if totalChar > 6000:
        return True
    
    return False

        
            



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
    __slots__ = ('users','items','shop','servers','tools')
    def __init__(self,bot):
        self.bot = bot
        self.users = {}
        self.items = {}
        self.shop = {}
        self.servers = {}
        self.tools={}





    def get_tools(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            tool = self.tools[ctx.guild.id]
        except KeyError:
            tool = SmashTools(ctx)
            self.tools[ctx.guild.id] = tool
        return tool



    

    






    @commands.command(name='smashprofiles',pass_context = True)
    async def viewprofiles(self,ctx):
        '''
        Shows all of the smash profiles currently on the server.
        Usage: 
        !smashprofiles
        '''
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)


        await jsondb.load_users(self)
        server = ctx.message.guild
        members = ctx.guild.members


        name = ""
        switchcode = ""
        main = ""

        for member in members:
            try:
                memberid = str(member.id)
                if self.users[memberid]['SmashProfile']['Tag'] is None:
                    continue
                name = name + self.users[memberid]['SmashProfile']['Tag'] + "\n"
                switchcode = switchcode + self.users[memberid]['SmashProfile']['SwitchCode'] + "\n"
                mains = self.users[memberid]['SmashProfile']['Main']
                #TODO Make their mains into their icons instead of just the name.
                try:
                    main = main + mains[0] + "\n"
                except IndexError:
                    continue

            except KeyError:
                continue
   
        if name is None:
            embed = create_embed('No users!','There are no users! Interesting..',RED)
            await ctx.send(embed=embed,delete_after=20)
            return


        embed = csmash_embed(name,switchcode,main,server.name)
        
        if check_embed_limits(embed):
            #TODO Create multiple embeds when embed limit is exceeded
            embed = create_embed('Embed limit exceeded!','There are no users! Interesting..',RED)
            await ctx.send(embed=embed)
            return
        else:
            await ctx.send(embed=embed)
        


    
        




    @commands.command(name='smashcode',pass_context = True)
    async def switchcode(self,ctx,*,arg):
        '''
        Modifies the switchcode of the author. Requires a 12 digit switchcode.

        Usage:
        !switchcode 123412341234
        '''

        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        await jsondb.load_users(self)
        arg = shlex.split(arg)
        switchcode = arg[0]
        if len(switchcode)!=12:
            embed = create_embed('smashcode error: Bad Switch Code ','The length of a switch code is 12 digits.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return
        else:
            switchcode = fix_switch_code(switchcode)
        
        userid = str(ctx.author.id)
        self.users[userid]['SmashProfile']['SwitchCode'] = switchcode
        await jsondb.save_users(self)
        await ctx.send('**{}** has modified their switchcode!'.format(ctx.author))
        


    @commands.command(name='smashmain',pass_context = True)
    async def smashmain(self,ctx,*,arg):
        '''
        Modifies the smash main of the author. Case sensitive. Use !smash characters to see the character format.

        Usage:
        !smashmain Luigi
        '''

        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        await jsondb.load_users(self)
        arg = arg.split(';')
        main = check_secondaries(arg)
        if not main:
            embed = create_embed('smashmain error: Incorrect format for main. ','You did not input a smash character. Try the sschar command to see correct format.',RED)
            await ctx.send(embed=embed,delete_after=20)
            return
        userid = str(ctx.author.id)
        self.users[userid]['SmashProfile']['Main'] = main
        await jsondb.save_users(self)
        await ctx.send('**{}** has modified their mains!'.format(ctx.author))



    @commands.command(name='smashgames',pass_context = True)
    async def smashgames(self,ctx,*,arg):

        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        await jsondb.load_users(self)
        userid = str(ctx.author.id)
        arg = arg.split(';')
        for game in arg:
            if game is not 'Ultimate' or game is not 'Melee':
                return await ctx.send('**{}**, the only smash games are Ultimate or Melee. xd')
        self.users[userid]['SmashProfile']['Tag'] = arg
        await jsondb.save_users(self)
        await ctx.send('**{}** has modified their tag.'.format(ctx.author))


    @commands.command(name='smashtag',pass_context = True)
    async def smashtag(self,ctx,*,arg):
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        await jsondb.load_users(self)
        userid = str(ctx.author.id)
        self.users[userid]['SmashProfile']['Tag'] = arg
        await jsondb.save_users(self)
        await ctx.send('**{}** has modified their tag.'.format(ctx.author))


    @commands.command(name='smashnote',pass_context = True)
    async def smashnote(self,ctx,*,arg):
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        await jsondb.load_users(self)
        userid = str(ctx.author.id)
        self.users[userid]['SmashProfile']['Note'] = arg
        await jsondb.save_users(self)
        await ctx.send('**{}** has modified their note.'.format(ctx.author))

    @commands.command(name='smashimage',pass_context = True)
    async def smashimage(self,ctx,*,arg):
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        await jsondb.load_users(self)
        userid = str(ctx.author.id)
        self.users[userid]['SmashProfile']['Image'] = arg
        await jsondb.save_users(self)
        await ctx.send('**{}** has modified their image.'.format(ctx.author))

    @commands.command(name='smashregion',pass_context = True)
    async def smashregion(self,ctx,*,arg):
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        await jsondb.load_users(self)
        userid = str(ctx.author.id)
        self.users[userid]['SmashProfile']['Region'] = arg
        await jsondb.save_users(self)
        await ctx.send('**{}** has modified their region.'.format(ctx.author))

    @commands.command(name='smashcolor',pass_context = True)
    async def smashcolor(self,ctx,*,Colour):
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        await jsondb.load_users(self)
        colorString = Colour
        Colour = re.search(r'^0x(?:[0-9a-fA-F]{3}){1,2}$', Colour)
        if not Colour:
            return await ctx.send("**{}**, you did not provide a color in hex format.".format(ctx.author))
        userid = str(ctx.author.id)
        self.users[userid]['SmashProfile']['Colour'] = colorString
        await jsondb.save_users(self)
        await ctx.send('**{}** has modified their colour.'.format(ctx.author))


    @commands.command(name='smashpocket',pass_context = True)
    async def smashpocket(self,ctx,*,arg=''):
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        await jsondb.load_users(self)
        arg = arg.split(';')
        secondarylist = check_secondaries(arg)
        if not secondarylist:
            secondarylist = ['']
        userid = str(ctx.author.id)
        self.users[userid]['SmashProfile']['Pockets'] = secondarylist
        await jsondb.save_users(self)
        await ctx.send('**{}** has modified their pockets!'.format(ctx.author))
    
    @commands.command(name='smashsecond',pass_context = True)
    async def secondaries(self,ctx,*,arg=''):
        '''
        Modifies the smash secondaries of the author. Case sensitive. Use !smashcharacters to see the character format.

        Usage:
        !smashsecond Luigi;Mario;Fox
        !smashsecond
        '''
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        await jsondb.load_users(self)
        arg = arg.split(';')
        secondarylist = check_secondaries(arg)
        if not secondarylist:
            secondarylist = ['']
        userid = str(ctx.author.id)
        self.users[userid]['SmashProfile']['Secondaries'] = secondarylist
        await jsondb.save_users(self)
        await ctx.send('**{}** has modified their secondaries!'.format(ctx.author))

    @commands.command(name='smashdelete',pass_context = True)
    async def smash_delete(self,ctx,user: discord.Member = None):
        '''
        Deletes the smash profile of the author. If a user is specified, then the author requires admin privileges. 

        Usage:
        !deletesmash
        !deletesmash @Lefty#6430
        '''
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        await jsondb.load_users(self)
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
        await jsondb.save_users
        await ctx.send("**{}**'s Smash Profile has been wiped.")
            

            

    @commands.cooldown(1,20,commands.BucketType.guild)
    @commands.command(name='smashchars',pass_context = True)
    async def smash_characters(self,ctx):
        '''
        List all the smash characters you can enter when creating and modifying a smash profile.

        Usage:
        !smashcharacters
        '''
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        author = ctx.author
        label = 1
        List = ""
        for item in Smash_Characters:
            Labelstr = str(label)
            List = List + Labelstr + ". " + item + "\n"
            label = label +1

        embed = create_embed("Smash Characters Format",List,GREEN)
        await author.send(embed=embed, delete_after=15)





    @commands.command(name='smash',pass_context = True)
    async def smashprofile(self,ctx, user:discord.Member = None):
        """
        """
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        await jsondb.load_users(self)
        if user is None:
            username = ctx.author
            userid = str(ctx.author.id)
        else:
            username = user
            userid = str(user.id)
        SmashProfile = self.users[userid]['SmashProfile']

        Tag = SmashProfile['Tag']
        SwitchCode = SmashProfile['SwitchCode']

        Colour = SmashProfile['Colour']
        if Colour:
            colorString = Colour
            Colour = re.search(r'^0x(?:[0-9a-fA-F]{3}){1,2}$', Colour)
            if Colour:
                colorString = int(colorString,16)
                colorString = discord.Colour(colorString)
                Colour = colorString
            else:
                Colour = 0x585d66
        else:
            Colour = 0x585d66

        embed=discord.Embed(title="{}'s Profile".format(username), color=Colour)
        if Tag:
            embed.add_field(name='Tag', value=Tag, inline=True)
        else:
            return await ctx.send("Error!")
        if SwitchCode:
            embed.add_field(name='Friend Code', value=SwitchCode, inline=True)

        mains = self.users[userid]['SmashProfile']['Main']
        guild = self.bot.get_guild(596938793244819458)
        guildemojis = guild.emojis
        emojis = []
        for name in mains:
            for emoji in guildemojis:
                if emoji.name == name:
                    emojis.append(emoji)
        guild = self.bot.get_guild(596938824983117825)
        guildemojis = guild.emojis
        for name in mains:
            for emoji in guildemojis:
                if emoji.name == name:
                    emojis.append(emoji)
        if len(emojis)==1:
            embed.add_field(name='Mains', value='{}'.format(emojis[0]), inline=True)
        elif len(emojis)==2:
            embed.add_field(name='Mains', value='{}{}'.format(emojis[0],emojis[1]), inline=True)
        elif len(emojis)==3:
            embed.add_field(name='Mains', value='{}{}{}'.format(emojis[0],emojis[1],emojis[2]), inline=True)
        elif len(emojis)==4:
            embed.add_field(name='Mains', value='{}{}{}{}'.format(emojis[0],emojis[1],emojis[2],emojis[3]), inline=True)



        secondaries = self.users[userid]['SmashProfile']['Secondaries']
        guild = self.bot.get_guild(596938793244819458)
        guildemojis = guild.emojis
        emojis = []
        for name in secondaries:
            for emoji in guildemojis:
                if emoji.name == name:
                    emojis.append(emoji)
        guild = self.bot.get_guild(596938824983117825)
        guildemojis = guild.emojis
        for name in secondaries:
            for emoji in guildemojis:
                if emoji.name == name:
                    emojis.append(emoji)
        if len(emojis)==1:
            embed.add_field(name='Secondaries', value='{}'.format(emojis[0]), inline=True)
        elif len(emojis)==2:
            embed.add_field(name='Secondaries', value='{}{}'.format(emojis[0],emojis[1]), inline=True)
        elif len(emojis)==3:
            embed.add_field(name='Secondaries', value='{}{}{}'.format(emojis[0],emojis[1],emojis[2]), inline=True)
        elif len(emojis)==4:
            embed.add_field(name='Secondaries', value='{}{}{}{}'.format(emojis[0],emojis[1],emojis[2],emojis[3]), inline=True)
        

        pockets = self.users[userid]['SmashProfile']['Pockets']
        guild = self.bot.get_guild(596938793244819458)
        guildemojis = guild.emojis
        emojis = []
        for name in pockets:
            for emoji in guildemojis:
                if emoji.name == name:
                    emojis.append(emoji)
        guild = self.bot.get_guild(596938824983117825)
        guildemojis = guild.emojis
        for name in pockets:
            for emoji in guildemojis:
                if emoji.name == name:
                    emojis.append(emoji)
        if len(emojis)==1:
            embed.add_field(name='Pockets', value='{}'.format(emojis[0]), inline=True)
        elif len(emojis)==2:
            embed.add_field(name='Pockets', value='{}{}'.format(emojis[0],emojis[1]), inline=True)
        elif len(emojis)==3:
            embed.add_field(name='Pockets', value='{}{}{}'.format(emojis[0],emojis[1],emojis[2]), inline=True)
        elif len(emojis)==4:
            embed.add_field(name='Pockets', value='{}{}{}{}'.format(emojis[0],emojis[1],emojis[2],emojis[3]), inline=True)
        elif len(emojis)==5:
            embed.add_field(name='Pockets', value='{}{}{}{}{}'.format(emojis[0],emojis[1],emojis[2],emojis[3],emojis[4]), inline=True)
        elif len(emojis)==6:
            embed.add_field(name='Pockets', value='{}{}{}{}{}{}'.format(emojis[0],emojis[1],emojis[2],emojis[3],emojis[4],emojis[5]), inline=True)
        elif len(emojis)==7:
            embed.add_field(name='Pockets', value='{}{}{}{}{}{}{}'.format(emojis[0],emojis[1],emojis[2],emojis[3],emojis[4],emojis[5],emojis[6]), inline=True)
        

        Games = SmashProfile['Games']
        if Games:
            gamelist = ''
            gamelist = Games[0]
            if len(Games) > 1:
                for Game in Games:
                    gamelist = "{},".format(gamelist) + Game
            embed.add_field(name='Games', value=gamelist, inline=True)
        Region = SmashProfile['Region']
        if Region:
            embed.add_field(name='Region', value=Region, inline=True)
        Note = SmashProfile['Note']
        if Note:
            embed.add_field(name='Note', value=Note, inline=True)

        Image = SmashProfile['Image']
        embed.set_thumbnail(url=Image)
        await ctx.send(embed=embed)





    @commands.command(name='smashhelp')
    async def smashhelp(self,ctx):
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)
        author = ctx.author
        msg = """Hello, here is how to setup LuigiBot's Smash profiles:
__**!smashtag:**__ Set your smash tag with this command. **Example: !smashtag Lefty**
__**!smashmain:**__ Set your smash mains with this command. Smash characters are case sensitive AND require correct format for each character. Separated by semicolons. 
Do !smashchars to see how to input the characters correctly. **Example: !smashmain Luigi;Mario**
__**!smashsecond:**__ Similar to smashmain, except with secondaries. **Example: !smashsecond Pacman;Ike**
__**!smashpocket:**__ Similar to smashmain, except with secondaries. **Example: !smashpocket Pichu;Daisy;Simon**
__**!smashimage:**__ Set your profile image to whatever link you provide. **Example: !smashimage https://cdn.discordapp.com/avatars/88047132937822208/3cb38e0dd632deb37a37e9770631023c.png?size=1024**
__**!smashregion:**__ Set your region to whatever you want(for now). **Example: !smashregion The Black Sea**
__**!smashgames:**__ Set the smash games you can play. Only options are Melee and Ultimate. **Example: !smashgames Ultimate;Melee**
__**!smashcode:**__ Set your switch code. Requires 12 digits. **Example: !smashcode 111122223333**
__**!smashcolor:**__ Set the color of your profile. Requires a color in hex format. **Example: !smashcolor 0x167a22**
__**!smashnote:**__ Leave a little note for whoever sees your profile. **Example: !smashnote I love Luigi!**

In addition, you can do **!command** to get understand specific usage of the commands. **Example: !command smashregion**

"""
        await author.send(msg)








        '''
        secondarylist = self.users[userid]['SmashProfile']['Secondaries']
        secondaries = ''
        for secondary in secondarylist:
            secondaries =secondaries + secondary + ', '
        embed = profile_embed(name,switchcode,main,secondaries)
        '''