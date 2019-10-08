


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
from random import randint
import requests
import tokens
from requests.exceptions import HTTPError
import operator
import json
from PIL import Image
dota_api_key = tokens.dota_api
GREEN = 0x16820d
from core import jsondb

class Dota(commands.Cog):

    __slots__ = ('users','items','shop','servers')
    def __init__(self,bot):
        self.bot = bot
        self.users = {}
        self.items = {}
        self.shop = {}
        self.servers = {}



    @commands.command(name='setsteam')
    async def create_id(self,ctx,*,arg):
        """
        Link a STEAM32ID to a discord profile. 

        Usage:
        !setsteam 97985854
        """
        await jsondb.load_users(self)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION,delete_after=10)


        userid = str(ctx.author.id)
        try:
            response = requests.get('https://api.opendota.com/api/players/{}?api_key={}'.format(arg,dota_api_key))
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  
            return await ctx.send("The STEAMID you provided does not exist.")
        except Exception as err:
            print(f'Other error occurred: {err}') 
            return await ctx.send("The STEAMID you provided does not exist.") 
        STEAMID = self.users[userid]['DotaProfile']['Steam32id']
        if STEAMID:
            return await ctx.send("**{}**, you already have STEAMID linked: **{}**".format(ctx.message.author,STEAMID),delete_after=10)
        self.users[userid]['DotaProfile']['Steam32id'] = arg
        print(self.users[userid]['DotaProfile']['Steam32id'])
        await jsondb.save_users(self)
        await ctx.send("**{}** has created his profile with the STEAMID: **{}**".format(ctx.message.author,arg),delete_after=10)

    @commands.command(name='steamdelete')
    async def delete_id(self,ctx):
        """
        Delete the STEAMID associated with the author.

        Usage:
        !steamdelete
        """
        await jsondb.load_users(self)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        userid = str(ctx.author.id)
        self.users[userid]['DotaProfile'] = {'Name':'', 'Steam32id': ''}
        await jsondb.save_users(self)
        await ctx.send("**{}** has wiped their STEAMID.".format(ctx.message.author),delete_after=10)
    
    @commands.command(name='mysteam')
    async def mysteam(self,ctx):
        """
        Shows basic information about the author, if they have a STEAMID linked to them.

        Usage:
        !mysteam
        """
        await jsondb.load_users(self)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        userid = str(ctx.author.id)
        STEAMID = self.users[userid]['DotaProfile']['Steam32id']
        if not STEAMID:
            return await ctx.send("You do not have a STEAMID linked to you!",delete_after=10)
        await ctx.send("**{}**, this is the STEAMID linked to you: **{}**".format(ctx.author,STEAMID))
        



    @commands.command(name='wordcloud',aliases=['wc'])
    async def dota_wordcloud(self, ctx, member:discord.Member = None):
        await jsondb.load_users(self)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        if member is None:
            userid = str(ctx.message.author.id)
        else:
            userid = str(member.id)
        STEAMID = self.users[userid]['DotaProfile']['Steam32id']
        if not STEAMID:
            return await ctx.send("You do not have a STEAMID linked to you!",delete_after=10)

        request = requests.get('https://api.opendota.com/api/players/{}/wordcloud?api_key={}'.format(STEAMID,dota_api_key))
        js = request.json()
        wordcounts = js['my_word_counts']
        wordcounts = sorted(wordcounts.items(), key=operator.itemgetter(1),reverse=True)
        print(wordcounts)
        msg = ''
        i = 0
        while i!=10:
            msg = msg + wordcounts[i][0] + ': ' + str(wordcounts[i][1]) + ' \n'
            i = i+1
        await ctx.send('Here are the top 10 words for **{}** \n'.format(ctx.author) + msg,delete_after=10)



    @commands.command(name='friendstats',aliases=['fs'])
    async def dota_friendstats(self, ctx, member:discord.Member = None):
        '''
        Show the top 5 friends you play with it.
        '''
        await jsondb.load_users(self)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        if member is None:
            userid = str(ctx.message.author.id)
        else:
            userid = str(member.id)
        STEAMID = self.users[userid]['DotaProfile']['Steam32id']
        if not STEAMID:
            return await ctx.send("You do not have a STEAMID linked to you!",delete_after=10)
        request = requests.get('https://api.opendota.com/api/players/{}/peers?api_key={}'.format(STEAMID,dota_api_key))
        js = request.json()
        print(js)


        personanames = [js[0]['personaname'], js[1]['personaname'], js[2]['personaname'], js[3]['personaname'], js[4]['personaname']]
        lastplayed = [js[0]['last_played'], js[1]['last_played'], js[2]['last_played'], js[3]['last_played'], js[4]['last_played']]
        wins = [js[0]['win'], js[1]['win'], js[2]['win'], js[3]['win'], js[4]['win']]
        losses =[js[0]['games'] - js[0]['win']  ,js[1]['games'] - js[1]['win'], js[2]['games'] - js[2]['win'],js[3]['games'] - js[3]['win'],js[4]['games'] - js[4]['win']]

        lastplayedlinks = []

        for last in lastplayed:
            lastplayedlinks.append( 'https://www.opendota.com/matches/' + str(last))




        personalist = ''
        lastplayedlinkslist= ''
        WLlist = []



        i = 0
        while i!=5:
            WL = '('+str(wins[i]) + '-' + str(losses[i])+')'
            WLlist.append(WL)
            i = i+1
        i = 0
        while i!=5:
            personalist = personalist + personanames[i] + ' {}'.format(WLlist[i]) + '\n'
            i = i+1



        for last in lastplayedlinks:
            lastplayedlinkslist= lastplayedlinkslist + last + '\n'
        



        print(personalist)
        print(lastplayedlinkslist)
        print(WLlist)

        author = ctx.author.name

        embed=discord.Embed(title=author, description="Dota Friend Stats", color=0x800000)
        embed.add_field(name='Friends', value=personalist, inline=True)
        embed.add_field(name='Last Played', value=lastplayedlinkslist, inline=True)
        await ctx.send(embed=embed)



















    '''
    @commands.command(name='dotarecent')
    async def dotarecent(self, ctx, member:discord.Member = None):
        self.load_users(self)
        if member is None:
            userid = ctx.message.author.id
        else:
            userid = member.id
        STEAMID = self.users[userid]['DotaProfile']['Steam32id']
        if not STEAMID:
            return await ctx.send("You do not have a STEAMID linked to you!",delete_after=10)

        print(STEAMID)
        request = requests.get('https://api.opendota.com/api/players/{}/recentMatches?api_key={}'.format(STEAMID,dota_api_key))
        js = request.json()
        print(js)

        matchid = [js[0]['match_id'], js[1]['match_id'], js[2]['match_id'], js[3]['match_id'], js[4]['match_id'],
        js[5]['match_id'],js[6]['match_id'],js[7]['match_id'],js[8]['match_id'],js[9]['match_id']]

        playerslot = [js[0]['player_slot'], js[1]['player_slot'], js[2]['player_slot'], js[3]['player_slot'], js[4]['player_slot'],
        js[5]['player_slot'],js[6]['player_slot'],js[7]['player_slot'],js[8]['player_slot'],js[9]['player_slot']]

        result = [js[0]['radiant_win'], js[1]['radiant_win'], js[2]['radiant_win'], js[3]['radiant_win'], js[4]['radiant_win'],
        js[5]['radiant_win'],js[6]['radiant_win'],js[7]['radiant_win'],js[8]['radiant_win'],js[9]['radiant_win']]

        heroes = [js[0]['hero_id'], js[1]['hero_id'], js[2]['hero_id'], js[3]['hero_id'], js[4]['hero_id'],
        js[5]['hero_id'],js[6]['hero_id'],js[7]['hero_id'],js[8]['hero_id'],js[9]['hero_id']]

        kda = []
    '''

    @commands.command(name='whoishere')
    async def whoishere(self, ctx):
        await jsondb.load_users(self)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        members = ctx.guild.members
        names = ''
        steams = ''

        for member in members:
            memberid = str(member.id)
            if self.users[memberid]['DotaProfile']['Steam32id'] is not None:
                names = names + self.users[memberid]['Name'] + '\n'
                steams = steams + self.users[memberid]['DotaProfile']['Steam32id'] +'\n'


        embed=discord.Embed(title='Steam Users')
        embed.add_field(name='Discord Name', value=names, inline=True)
        embed.add_field(name='Steam32ID', value=steams, inline=True)
        await ctx.send(embed=embed,delete_after=20)
        
    @commands.command(name='dotahelp')
    async def dotahelp(self, ctx):
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        author = ctx.author
        msg = """To setup a dota profile, you first need to link up your Steam32id. To get that, I reccommend you use https://steamid.xyz/ to get it.
Then, you simply use the !setsteam command.
!setsteam 97985854

Then you can see your profile as well as others with !dota. Use !help Dota to see all of the dota commands.

"""
        author.send(msg)

    @commands.command(name='dota')
    async def dotaprofile(self, ctx, member:discord.Member = None):
        """
        Retrieves the dota profile of a user who has a STEAM32ID linked to their discord. 
        By default it provides the profile of the author.

        Author can optionally tag a user and get their profile. 

        Usage:
        !dota 
        !dota @Lefty#6430


        """

        await jsondb.load_users(self)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        if member is None:
            userid = str(ctx.message.author.id)
        else:
            userid = str(member.id)
        STEAMID = self.users[userid]['DotaProfile']['Steam32id']
        if not STEAMID:
            return await ctx.send("You do not have a STEAMID linked to you!",delete_after=10)

        request = requests.get('https://api.opendota.com/api/players/{}/wl?api_key={}'.format(STEAMID,dota_api_key))
        js = request.json()
        print(js)
        winlossper = js['win'] / (js['win'] + js['lose'])
        winlosscorr = "%.1f" % round(winlossper * 100,1)
        winloss = str(js['win']) + '/' + str(js['lose']) + " ({}%)".format(winlosscorr)

        #Get most recent match
        request = requests.get('https://api.opendota.com/api/players/{}/recentMatches?api_key={}'.format(STEAMID,dota_api_key))
        js = request.json()
        recent = 'https://www.opendota.com/matches/' + str(js[0]['match_id'])

        #Get Dota username
        request =requests.get('https://api.opendota.com/api/players/{}?api_key={}'.format(STEAMID,dota_api_key))
        js = request.json()
        comprank = get_emblem(str(js["rank_tier"]))
        comprank_str = comprank[0]
        comprank_url = comprank[1]
        username = js["profile"]["personaname"]
        
        #Gets Top 5 Heroes for User
        
        request =requests.get('https://api.opendota.com/api/players/{}/heroes?api_key={}'.format(STEAMID,dota_api_key))
        js = request.json()
        sortedWins = sorted(js,key = lambda i: i['win'],reverse=True)
        Heroes = []
        i = 0
        while i!=5:
            print(sortedWins[i])
            Heroes.append(sortedWins[i])
            i = i+1
        request =requests.get('https://api.opendota.com/api/heroes?api_key={}'.format(dota_api_key))
        r = request.json()
        HeroDicts = []
        for hero in Heroes:
            match = next((l for l in r if l['id'] == int(hero['hero_id'])), None)
            HeroDicts.append(match)
        HeroNames = []
        for hero in HeroDicts:
            HeroNames.append(hero['localized_name'])
        HeroWL = []
        for hero in Heroes:
            WLpercent = "%.1f" %round((hero['win'] / hero['games'])*100,1)
            HeroWL.append(WLpercent)
        HeroList = ''
        i = 0
        while i!=5:
            HeroList = HeroList + HeroNames[i] + ' ({}%)'.format(HeroWL[i]) + '\n'
            i = i+1
    
        opendota = 'https://www.opendota.com/players/' + STEAMID
        dotabuff = 'https://www.dotabuff.com/players/' + STEAMID

        embed = dota_profile(username,comprank_url,comprank_str,winloss,recent,HeroList,opendota,dotabuff)
        await ctx.send(embed=embed)

    

    
    

def dota_profile(username,comprank_url,comprank_str,winloss,recent,HeroList,opendota,dotabuff):
    links = opendota + '\n' + dotabuff
    embed=discord.Embed(title=username)
    embed.set_thumbnail(url=comprank_url)
    embed.add_field(name='Medal', value=comprank_str, inline=True)
    embed.add_field(name='Win/Loss', value=winloss, inline=True)
    embed.add_field(name='Last Match Played', value=recent, inline=True)
    embed.add_field(name='Most Successful Heroes',value=HeroList,inline=True)
    embed.add_field(name='Detailed stats',value=links,inline=True)
    return embed

def get_emblem(rank):
    tier = rank[0]
    stars = rank[1]
    
    if tier == '1':
        if stars=='1':
            return ['Herald 1','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/8/85/SeasonalRank1-1.png/140px-SeasonalRank1-1.png?version=ce7c6eea36971495cdad1f06e7ef3709']
        if stars=='2':
            return ['Herald 2','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/e/ee/SeasonalRank1-2.png/140px-SeasonalRank1-2.png?version=094dc352040053ea02f1bbb82a4591f1']
        if stars=='3':
            return ['Herald 3','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/0/05/SeasonalRank1-3.png/140px-SeasonalRank1-3.png?version=529b1f8ac23899b14bb30b03036d277e']
        if stars=='4':
            return ['Herald 4','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/6/6d/SeasonalRank1-4.png/140px-SeasonalRank1-4.png?version=e5fa236efcfc108987fac807d890771d']
        if stars=='5':
            return ['Herald 5','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/2/2b/SeasonalRank1-5.png/140px-SeasonalRank1-5.png?version=c33004c635c667fa661fad0e2593869e']
        if stars=='6':
            return ['Herald 6','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/9/94/SeasonalRank1-6.png/140px-SeasonalRank1-6.png?version=bb9f79190f5d22036e159cc11f6e4552']
        if stars=='7':
            return ['Herald 7','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/1/12/SeasonalRank1-7.png/140px-SeasonalRank1-7.png?version=06c12864a8818c15a257e56b1dff33e6']

    if tier == '2':
        if stars=='1':
            return['Guardian 1','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/c/c7/SeasonalRank2-1.png/140px-SeasonalRank2-1.png?version=832ba8a7042450ebf2cee3209e2cfac8']
        if stars=='2':
            return['Guardian 2','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/2/2c/SeasonalRank2-2.png/140px-SeasonalRank2-2.png?version=be558245d8ddcb6479277d684956aea9']
        if stars=='3':
            return['Guardian 3','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/f/f5/SeasonalRank2-3.png/140px-SeasonalRank2-3.png?version=38233a7123c0b90df8872a6b9a04a87c']
        if stars=='4':
            return['Guardian 4','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/b/b4/SeasonalRank2-4.png/140px-SeasonalRank2-4.png?version=879bc97952e7acbbb4cb76df1618757a']
        if stars=='5':
            return['Guardian 5','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/3/32/SeasonalRank2-5.png/140px-SeasonalRank2-5.png?version=5b99be61ba7db96bfdc03a9fef6f1fb4']
        if stars=='6':
            return['Guardian 6','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/7/72/SeasonalRank2-6.png/140px-SeasonalRank2-6.png?version=bce1599901754fd7efba4a436ed73c2c']
        if stars=='7':
            return['Guardian 7','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/c/c6/SeasonalRank2-7.png/140px-SeasonalRank2-7.png?version=4edfbd10d740bfde6b55d157684f91f8']
    
    if tier == '3':
        if stars=='1':
            return ['Crusader 1','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/8/82/SeasonalRank3-1.png/140px-SeasonalRank3-1.png?version=b9a19f0189fe0236ee00fb94cc97a693']
        if stars=='2':
            return ['Crusader 2','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/6/6e/SeasonalRank3-2.png/140px-SeasonalRank3-2.png?version=8e03bbb7be665bcadcb0913eaecee2c0']
        if stars=='3':
            return ['Crusader 3','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/6/67/SeasonalRank3-3.png/140px-SeasonalRank3-3.png?version=59df65f46dbfc05c7dcb5d877aa2f37c']
        if stars=='4':
            return ['Crusader 4','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/8/87/SeasonalRank3-4.png/140px-SeasonalRank3-4.png?version=8582a808c060a4df95385c98844e666b']
        if stars=='5':
            return ['Crusader 5','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/b/b1/SeasonalRank3-5.png/140px-SeasonalRank3-5.png?version=4f0db8503ae24ddd488374b6e5968daf']
        if stars=='6':
            return ['Crusader 6','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/3/33/SeasonalRank3-6.png/140px-SeasonalRank3-6.png?version=49a476e554c32209127a75251927f9eb']
        if stars=='7':
            return ['Crusader 7','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/6/66/SeasonalRank3-7.png/140px-SeasonalRank3-7.png?version=af7845383494861912c4455b96fe2ee1']
    
    if tier == '4':
        if stars=='1':
            return ['Archon 1','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/7/76/SeasonalRank4-1.png/140px-SeasonalRank4-1.png?version=7a9db7f22e02de4a58923f40da38b9db']
        if stars=='2':
            return ['Archon 2','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/8/87/SeasonalRank4-2.png/140px-SeasonalRank4-2.png?version=358a9043ef264bcb2ea3424339ac671a']
        if stars=='3':
            return ['Archon 3','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/6/60/SeasonalRank4-3.png/140px-SeasonalRank4-3.png?version=3e5c81e69f244b6028ef27beb0fc3ec6']
        if stars=='4':
            return ['Archon 4','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/4/4a/SeasonalRank4-4.png/140px-SeasonalRank4-4.png?version=aacf3fb098fb8de1c514d73b7a0f63c7']
        if stars=='5':
            return ['Archon 5','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/a/a3/SeasonalRank4-5.png/140px-SeasonalRank4-5.png?version=7b207bd7de3fe423117f6ea7331dfc88']
        if stars=='6':
            return ['Archon 6','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/7/7e/SeasonalRank4-6.png/140px-SeasonalRank4-6.png?version=66471a1deead6b4ca9afcb1749300144']
        if stars=='7':
            return ['Archon 7','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/9/95/SeasonalRank4-7.png/140px-SeasonalRank4-7.png?version=13cf98fe65e3be143a20f4db86f73dbe']
    
    if tier == '5':
        if stars=='1':
            return['Legend 1','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/7/79/SeasonalRank5-1.png/140px-SeasonalRank5-1.png?version=7742371d2571ee59b59c6ac14e5688fa']
        if stars=='2':
            return['Legend 2','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/5/52/SeasonalRank5-2.png/140px-SeasonalRank5-2.png?version=204da548015c1947ce514c8ac81c99ea']
        if stars=='3':
            return['Legend 3','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/8/88/SeasonalRank5-3.png/140px-SeasonalRank5-3.png?version=990f1323b00256eb84002ab050b9188b']
        if stars=='4':
            return['Legend 4','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/2/25/SeasonalRank5-4.png/140px-SeasonalRank5-4.png?version=0248fc56651cc810ddceca901386322a']
        if stars=='5':
            return['Legend 5','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/8/8e/SeasonalRank5-5.png/140px-SeasonalRank5-5.png?version=14dc5ce669daf93b178350a0b3ee27e1']
        if stars=='6':
            return['Legend 6','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/2/2f/SeasonalRank5-6.png/140px-SeasonalRank5-6.png?version=5646cbec393b398e93ad943dff59450d']
        if stars=='7':
            return['Legend 7','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/c/c7/SeasonalRank5-7.png/140px-SeasonalRank5-7.png?version=fba307eea0262c8c1fb9d2df6719ab80']
    
    if tier == '6':
        if stars=='1':
            return['Ancient 1',
            'https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/e/e0/SeasonalRank6-1.png/140px-SeasonalRank6-1.png?version=56f4415e7d8fc83168c03f374e7babbc']
        if stars=='2':
            return['Ancient 2',
            'https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/1/1c/SeasonalRank6-2.png/140px-SeasonalRank6-2.png?version=87515796db90be81886c62cad9faf87f']
        if stars=='3':
            return['Ancient 3',
            'https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/d/da/SeasonalRank6-3.png/140px-SeasonalRank6-3.png?version=190512e1572f037b0936f8b1a4bb55b6']
        if stars=='4':
            return['Ancient 4',
            'https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/d/db/SeasonalRank6-4.png/140px-SeasonalRank6-4.png?version=aba16fcff849cb2495f1ddc25bfefd74']
        if stars=='5':
            return['Ancient 5',
            'https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/4/47/SeasonalRank6-5.png/140px-SeasonalRank6-5.png?version=1ae82223757486aa55461a82fa09ac6a']
        if stars=='6':
            return['Ancient 6',
            'https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/b/bd/SeasonalRank6-6.png/140px-SeasonalRank6-6.png?version=2dcf5133eb4f5661b7b37d962c4b0b8a']
        if stars=='7':
            return['Ancient 7',
            'https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/b/b8/SeasonalRank6-7.png/140px-SeasonalRank6-7.png?version=468afa717e6f36af09d4b6c5b71a0ddb']
    
    
    
    if tier == '7':
        if stars=='1':
            return ['Divine 1','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/b/b7/SeasonalRank7-1.png/140px-SeasonalRank7-1.png?version=8cd74e57b63ceb730d7b36a8f6589b9f']
        if stars=='2':
            return ['Divine 2','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/8/8f/SeasonalRank7-2.png/140px-SeasonalRank7-2.png?version=59d74d77a554732a99debd54d1b1b641']
        if stars=='3':
            return ['Divine 3', 'https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/f/fd/SeasonalRank7-3.png/140px-SeasonalRank7-3.png?version=12f7e65e8c858b1d39e2a4a17bc85522']
        if stars=='4':
            return ['Divine 4','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/1/13/SeasonalRank7-4.png/140px-SeasonalRank7-4.png?version=247aba452307e17cd6f647321450b8a5']
        if stars=='5':
            return ['Divine 5','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/3/33/SeasonalRank7-5.png/140px-SeasonalRank7-5.png?version=0db40597d94b70e3619c2a3e80317e94']
        if stars=='6':
            return ['Divine 6','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/a/a1/SeasonalRank7-6.png/140px-SeasonalRank7-6.png?version=85d8919b41a8db103eef75445457b58f']
        if stars=='7':
            return ['Divine 7','https://gamepedia.cursecdn.com/dota2_gamepedia/thumb/c/c1/SeasonalRank7-7.png/140px-SeasonalRank7-7.png?version=7a669fe5a5f721dce6643cb64eb65fc8']
        
