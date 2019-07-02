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
from db import gachadatabase
from db import database
from core.helper import gacha_allowed


class Gacha(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
    @commands.command(name='gacharemove')
    async def rhero(self,ctx,*,arg):
        """
        Removes the hero from being obtainable through summoning. Must have admin privileges to execute it. 
        This command does NOT remove the hero from any users barracks. Use gachamassacre for that.

        Usage:
        !gacharemove Dio Brando

        """
        

        author = ctx.message.author
        SERVERID = str(ctx.message.guild.id)
        channelid = ctx.message.channel.id
        if not gachadatabase.get_gacha_channel([SERVERID,channelid]):
            return await ctx.send("This channel was not set for Gacha Commands to be used.")

        if not author.guild_permissions.administrator:
            await ctx.send('Sorry good sir, you do not have permission to modify the database!',delete_after=20)
            return
        lmao = gachadatabase.get_hero([arg,ctx.message.guild.id])
        if not lmao:
            await ctx.send("Hero does not exist!",delete_after = 20)
        else:
            HERONAME = lmao[1]
            gachadatabase.remove_hero([SERVERID,HERONAME])
            await ctx.send("Hero has been deleted!",delete_after=20)


    @commands.command(name='gachamassacre')
    async def pdhero(self,ctx,*,arg):
        """
        Removes the hero from everyones barracks. You must have admin privileges to execute this command.
        This command does NOT remove the hero from the summoning pool. Use gacharemove for that.

        Usage:
        !gachamassacre Dio Brando
        """
        author = ctx.message.author
        SERVERID = str(ctx.message.guild.id)
        channelid = ctx.message.channel.id
        if not gachadatabase.get_gacha_channel([SERVERID,channelid]):
            return await ctx.send("This channel was not set for Gacha Commands to be used.")
        if not author.guild_permissions.administrator:
            await ctx.send('Sorry good sir, you do not have permission to create an economy!',delete_after=20)
            return
        lmao = gachadatabase.get_barracks_hero2([ctx.message.guild.id,arg])
        if not lmao:
            await ctx.send("Hero does not exist!")
        else:
            gachadatabase.remove_barracks_hero([SERVERID,arg])
            await ctx.send("Hero has been removed from everyones barracks!")




    @commands.command(name='gachacreate', aliases=['gcreate'])
    async def gcreate(self,ctx,*,arg):
        """
        Add a new hero for the server you're in. Requires admin privileges to execute this command.
        At the moment, this command is flawed. It is comma separated and requries 11 arguments. 
        This means that you CANNOT use commas anywhere in your hero creation, which includes the description.
        This will be updated in the future.

        Usage:
        !gachacreate  Swindlemelonz, http://a.espncdn.com/photo/2016/0811/r112443_1855x2651cc.jpg,One of NA Dota's greatest heroes and greatest adversaries. ,Faris,Antagonist,5,46,36,26,27,30
        """
        SERVERID = str(ctx.message.guild.id)
        gacha = arg.split(',')
        author = ctx.message.author
        channelid = ctx.message.channel.id
        if not gachadatabase.get_gacha_channel([SERVERID,channelid]):
            return await ctx.send("This channel was not set for Gacha Commands to be used.")
        if not author.guild_permissions.administrator:
            await ctx.send('Sorry good sir, you do not have permission to create an economy!',delete_after=20)
            return

        if len(arg)<11:
            await ctx.send('Sorry, you need to provide at least 11 arguments to create a new gacha hero.')
            return

        gachas = gacha[:5]
        gachaints = gacha[5:11]
        gachas.insert(0,SERVERID)

        T2 = [int(x) for x in gachaints]
        for intboy in T2:
            gachas.append(intboy)
        gachadatabase.create_hero(gachas)
        await ctx.send("**{}** has created the hero: **{}**".format(ctx.message.author,gachas[1]))

    @commands.command(name="gachahero",aliases=['gh'])
    async def get_hero_data(self,ctx,*,arg):
        """
        Get some basic info for a gacha hero on this server.

        Usage:
        !gachahero Dio Brando
        !gh Oliver
        """
        SERVERID = ctx.message.guild.id
        channelid = ctx.message.channel.id
        if not gachadatabase.get_gacha_channel([SERVERID,channelid]):
            return await ctx.send("This channel was not set for Gacha Commands to be used.")
        lmao = gachadatabase.get_hero([arg,ctx.message.guild.id])
        if not lmao:
            await ctx.send("Hero does not exist!")
        else:
            print(lmao)
            stats = "HP: " + str(lmao[7]) + " \n" + "ATK: " + str(lmao[8]) + " \n" + "DEF: " + str(lmao[9]) + " \n" + "SPDEF:"+ str(lmao[10])+ " \n" + "SPD: " + str(lmao[11]) + " \n"
            embed=discord.Embed(title=lmao[1], description=lmao[3])
            embed.set_image(url = lmao[2])
            embed.add_field(name='Creator', value=lmao[4], inline=True)
            embed.add_field(name='Rating', value=lmao[6], inline=True)
            embed.add_field(name='Type', value=lmao[5], inline=True)
            embed.add_field(name='Moves', value='TODO', inline=True)
            embed.add_field(name='Stats', value=stats, inline=True)
            await ctx.send(embed=embed)


    @commands.command(name='gachagivecoins',aliases=['ggc'])
    async def givecoins(self,ctx,member: discord.Member = None,coins: int = 0):
        """
        Gives coins to a user. Requires admin privileges to execute this command. 
        Use gachasetcoins to set the coins of a user to a specific amount.

        Usage:
        !gachagivecoins @Lefty#6430 50
        !gg @Lefty#6430 50
        """

        author = ctx.message.author
        SERVERID = str(ctx.message.guild.id)
        MEMBERID = str(member.id)
        channelid = ctx.message.channel.id
        if not gachadatabase.get_gacha_channel([SERVERID,channelid]):
            return await ctx.send("This channel was not set for Gacha Commands to be used.")

        if not author.guild_permissions.administrator:
            await ctx.send('Sorry good sir, you do not have permission to modify the database.',delete_after=20)
            return
        
        balance = database.get_balance([SERVERID,MEMBERID])
        newbal = balance[2] + coins
        database.set_balance([SERVERID,MEMBERID,newbal])
        await ctx.send("**{}**, you now have a balance of **{}** LuigiCoins!".format(author,newbal))

    @commands.command(name='gachasetcoins',aliases=['gsc'])
    async def setcoins(self,ctx,member: discord.Member = None,coins: int = 0):
        """
        Sets coins to a user. Requires admin privileges to execute this command. 
        Use gachagivecoins to give coins of a specific amount to a user.

        Usage:
        !gs @Lefty#6430 50
        !gachasetcoins @Lefty#6430 50
        """

        author = ctx.message.author
        SERVERID = str(ctx.message.guild.id)
        MEMBERID = str(member.id)
        channelid = ctx.message.channel.id
        if not gachadatabase.get_gacha_channel([SERVERID,channelid]):
            return await ctx.send("This channel was not set for Gacha Commands to be used.")
        if not author.guild_permissions.administrator:
            await ctx.send('Sorry good sir, you do not have permission to create an economy!',delete_after=20)
            return
        
        database.set_balance([SERVERID,MEMBERID,coins])
        await ctx.send("**{}**, you now have a balance of **{}** LuigiCoins!".format(author,coins))


    @commands.command(name='gachasummon',aliases=['summon','gs'])
    async def summon(self,ctx):
        '''
        Summons a hero from the pool of heroes set for the server.
        Requires 5 LuigiCoins from the author.
        Current summoning rates: 50% for 3 Star, 40% for 4 star, 10% for 5 star.

        Usage:
        !gachasummon
        !summon
        !gs
        '''
        SERVERID = str(ctx.message.guild.id)
        MEMBERID = str(ctx.message.author.id)
        balance = database.get_balance([SERVERID,MEMBERID])
        ID = randint(0,80000)
        channelid = ctx.message.channel.id
        if not gachadatabase.get_gacha_channel([SERVERID,channelid]):
            return await ctx.send("This channel was not set for Gacha Commands to be used.")
        if not balance:
            await ctx.send("You don't have an account set up on this server!")
            return
        tokens = balance[2]
        if tokens >=5:
            tokens = tokens - 5
            database.set_balance([SERVERID,MEMBERID,tokens])
            value = randint(1,100)
            
            
            
            if value >= 1 and value <=50:
                threestars = gachadatabase.get_threestars(SERVERID)
                gachaplace = randint(0,len(threestars)-1)
                gacha = threestars[gachaplace]
                gachadatabase.add_hero([SERVERID,MEMBERID,gacha[0],gacha[1],gacha[2],gacha[3],gacha[4],gacha[5],3,ID,gacha[7]])
                await ctx.send("You got the 3 star hero: **{}**!! ID: {} Description: {}".format(gacha[0],ID,gacha[6]))
            
            if value >=51 and value <=90:
                fourstars = gachadatabase.get_fourstars(SERVERID)
                gachaplace = randint(0,len(fourstars)-1)
                gacha = fourstars[gachaplace]
                gachadatabase.add_hero([SERVERID,MEMBERID,gacha[0],gacha[1],gacha[2],gacha[3],gacha[4],gacha[5],4,ID,gacha[7]])
                await ctx.send("You got the 4 star hero: **{}**!! Description: {}".format(gacha[0],gacha[6]))

            if value >=91 and value <=100:
                fivestars = gachadatabase.get_fivestars(SERVERID)
                gachaplace = randint(0,len(fivestars)-1)
                gacha = fivestars[gachaplace]
                gachadatabase.add_hero([SERVERID,MEMBERID,gacha[0],gacha[1],gacha[2],gacha[3],gacha[4],gacha[5],5,ID,gacha[7]])
                await ctx.send("You got the 5 star hero: **{}**!! Description: {}".format(gacha[0],gacha[6]))
        else:
            await ctx.send("Sorry, you don't have enough coins sir!")
            

    @commands.command('gacha3', aliases = ['g3'])
    async def list3stars(self,ctx):
        """
        List all 3 star heroes on the server.
        !gacha3
        !g3
        """
        SERVERID = str(ctx.message.guild.id)
        channelid = ctx.message.channel.id
        if not gachadatabase.get_gacha_channel([SERVERID,channelid]):
            return await ctx.send("This channel was not set for Gacha Commands to be used.")
        threestars = gachadatabase.get_threestars(SERVERID)
        await ctx.send("There are currently **{}** Three Rarity Heroes on this server.".format(len(threestars)))
        newlist = create_filter_list(threestars)
        await ctx.send(newlist)
    
    @commands.command('gacha4',aliases = ['g4'])
    async def list4stars(self,ctx):
        """
        List all 4 star heroes on the server.
        !gacha4
        !g4
        """
        SERVERID = str(ctx.message.guild.id)
        
        channelid = ctx.message.channel.id
        if not gachadatabase.get_gacha_channel([SERVERID,channelid]):
            return await ctx.send("This channel was not set for Gacha Commands to be used.")
        fourstars = gachadatabase.get_fourstars(SERVERID)
        await ctx.send("There are currently **{}** Four Rarity Heroes on this server.".format(len(fourstars)))
        newlist = create_filter_list(fourstars)
        await ctx.send(newlist)
    
    @commands.command('gacha5',aliases = ['g5'])
    async def list5stars(self,ctx):
        """
        List all 5 star heroes on the server.
        !gacha5
        !g5
        """
        SERVERID = str(ctx.message.guild.id)
        channelid = ctx.message.channel.id
        if not gachadatabase.get_gacha_channel([SERVERID,channelid]):
            return await ctx.send("This channel was not set for Gacha Commands to be used.")
        fivestars = gachadatabase.get_fivestars(SERVERID)
        await ctx.send("There are currently **{}** Five Rarity Heroes on this server.".format(len(fivestars)))
        newlist = create_filter_list(fivestars)
        await ctx.send(newlist)






    @commands.command(name='gachapc',aliases=['gpc','pc'])
    async def checkbox(self,ctx):
        """
        Lists all of the author's heroes.
        Usage:
        !gachapc
        !gpc
        !pc
        """
        SERVERID = str(ctx.message.guild.id)
        MEMBERID = str(ctx.message.author.id)
        channelid = ctx.message.channel.id

        if not gachadatabase.get_gacha_channel([SERVERID,channelid]):
            return await ctx.send("This channel was not set for Gacha Commands to be used.")

        barracks = gachadatabase.get_heroes([SERVERID,MEMBERID])
        if not barracks:
            await ctx.send("You got no boys, bro!")
        barrackslist = create_list(barracks)
        await ctx.send(barrackslist,delete_after=30)
        
    
    @commands.command(name='gachareturn',aliases =['gr','gk'])
    async def killhero(self,ctx,*,arg):
        """
        Release a hero the author owns. Gives back LuigiCoins for the following rarities:
        3 star = 2 LuigiCoins
        4 star = 4 LuigiCoins
        5 star = 10 LuigiCoins

        Requires the user to input their hero ID. Use the gachapc command to see it.
        Usage:
        !gr 11435
        """
        SERVERID = ctx.message.guild.id
        MEMBERID = ctx.author.id
        heroids = arg.split(';')
        heroid_ints = []
        for hero in heroids:
            heroid_ints.append(int(hero))
        print(heroid_ints)
        msg = ""

        channelid = ctx.message.channel.id
        if not gachadatabase.get_gacha_channel([SERVERID,channelid]):
            return await ctx.send("This channel was not set for Gacha Commands to be used.")


        for ID in heroid_ints:

            hero = gachadatabase.get_barracks_hero([SERVERID,MEMBERID,ID])
            if not hero:
                await ctx.send("You do not own a hero with this ID: **{}**".format(ID),delete_after=10)
                continue

            if hero[9] == 3:
                coins = 2
            if hero[9] == 4:
                coins = 4
            if hero[9] == 5:
                coins = 10

            balance = database.get_balance([SERVERID,MEMBERID])
            newbal = balance[2] + coins
            database.set_balance([SERVERID,MEMBERID,newbal])
            gachadatabase.delete_barracks_hero(ID)  
            msg = msg + "**{}** has been deleted. Returning **{} LuigiCoins.** \n".format(hero[2],coins)
        if msg != "":
            await ctx.send(msg,delete_after=20)
        

    


    @commands.command(name='gachaprimary',aliases=['gp','gsp'])
    async def setp(self,ctx,*,arg):
        """
        Sets the primary hero for the user on the current server. Requires the hero to have 4 moves already, as well as the Hero ID.

        Usage:
        !gachaprimary 11123;12345;12333;14141
        """
        authorid = str(ctx.message.author.id)
        serverid= str(ctx.message.guild.id)
        HEROIDS =  arg.split(' ')
        OWN_HEROID = []
        msg = "Your primary team is now: "

        channelid = ctx.message.channel.id

        if not gachadatabase.get_gacha_channel([serverid,channelid]):
            return await ctx.send("This channel was not set for Gacha Commands to be used.")

        if len(HEROIDS)>4:
            return await ctx.send("Sorry, you can only set up to 4 primary heroes max!")

        for HEROID in HEROIDS:
            hero = gachadatabase.get_barracks_hero([serverid,authorid,HEROID])
            if not hero:
                await ctx.send("Sorry, you do not have a hero with the following ID: **{}**".format(HEROID))
            else:
                OWN_HEROID.append(HEROID)
                msg = msg + "**"+hero[2]+"**, "

        if not OWN_HEROID:
            return await ctx.send("Sorry, you don't own any heroes with the IDS you gave.")
        gachadatabase.remove_primary_hero([serverid,authorid])
        if len(OWN_HEROID) == 1:
            gachadatabase.place_primary_hero1([serverid,authorid,OWN_HEROID[0]])
        if len(OWN_HEROID) == 2:
            gachadatabase.place_primary_hero2([serverid,authorid,OWN_HEROID[0],OWN_HEROID[1]])
        if len(OWN_HEROID) == 3:
            gachadatabase.place_primary_hero3([serverid,authorid,OWN_HEROID[0],OWN_HEROID[1],OWN_HEROID[2]])
        if len(OWN_HEROID) == 4:
            gachadatabase.place_primary_hero4([serverid,authorid,OWN_HEROID[0],OWN_HEROID[1],OWN_HEROID[2],OWN_HEROID[3]])


        
        await ctx.send(msg)

    @commands.command(name='setgacha')
    async def setgacha(self,ctx):
        """
        Sets the channel for gacha commands to occur.
        """
        author = ctx.message.author
        SERVERID = str(ctx.message.guild.id)
        CHANNELID = str(ctx.message.channel.id)


        if not author.guild_permissions.administrator:
            await ctx.send('Sorry good sir, you do not have permission to modify the database!',delete_after=10)
            return
        gachadatabase.set_gacha_channel([SERVERID,CHANNELID])
        await ctx.send("Battles have been set to the **{}** channel.".format(ctx.message.channel),delete_after = 10)

    @commands.command(name='createmove')
    async def addgachamove(self,ctx,*,arg):
        arg = arg.split(';')
        author = ctx.message.author
        SERVERID = str(ctx.message.guild.id)
        CHANNELID = str(ctx.message.channel.id)
        if not gachadatabase.get_gacha_channel([SERVERID,CHANNELID]):
            return await ctx.send("This channel was not set for Gacha Commands to be used.")
        if not author.guild_permissions.administrator:
            await ctx.send('Sorry good sir, you do not have permission to modify the database!',delete_after=10)
            return
        arg.insert(0,SERVERID)
        gachadatabase.add_gacha_move(arg)
        await ctx.send("You have created the move **{}** for the Hero: **{}**.".format(arg[2],arg[1]))



def create_list(barracks):
    label = 1
    List = ""
    for item in barracks:
        Labelstr = str(label)
        List = List + "__**" + item[2] + "**__  ID: " + str(item[10]) +    "  Rarity: **" +str(item[9])+"**  HP: " + str(item[3]) + '  ATK: ' + str(item[4]) +'  DEF: ' + str(item[5]) +'  SDEF: ' + str(item[6]) +'  SPD: ' + str(item[7]) + '  UPGRADES: ' + str(item[8])+ "\n"
        label = label +1

    return List


def create_filter_list(thelist):
    label = 1
    List = ""
    for item in thelist:
        Labelstr = str(label)
        List = List + Labelstr + ". **" + item[0] + "**  Description: " + item[6] + " \n" 
        label = label + 1    
    return List



    