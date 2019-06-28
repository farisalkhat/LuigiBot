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



class Gacha(commands.Cog):

    def __init__(self,bot):
        self.bot = bot


    @commands.command(name='rhero')
    async def rhero(self,ctx,*,arg):
        author = ctx.message.author
        SERVERID = str(ctx.message.guild.id)

        if not author.guild_permissions.administrator:
            await ctx.send('Sorry good sir, you do not have permission to create an economy!',delete_after=20)
            return
        lmao = gachadatabase.get_hero([arg,ctx.message.guild.id])
        if not lmao:
            await ctx.send("Hero does not exist!")
        else:
            HERONAME = lmao[1]
            gachadatabase.remove_hero([SERVERID,HERONAME])
            await ctx.send("Hero has been deleted!")


    @commands.command(name='pdhero')
    async def pdhero(self,ctx,*,arg):
        author = ctx.message.author
        SERVERID = str(ctx.message.guild.id)

        if not author.guild_permissions.administrator:
            await ctx.send('Sorry good sir, you do not have permission to create an economy!',delete_after=20)
            return
        lmao = gachadatabase.get_barracks_hero2([ctx.message.guild.id,arg])
        if not lmao:
            await ctx.send("Hero does not exist!")
        else:
            gachadatabase.remove_barracks_hero([SERVERID,arg])
            await ctx.send("Hero has been removed from everyones barracks!")




    @commands.command(name='gcreate')
    async def gcreate(self,ctx,*,arg):
        SERVERID = str(ctx.message.guild.id)
        gacha = arg.split(',')
        author = ctx.message.author

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

    @commands.command(name="hero",aliases=['h'])
    async def get_hero_data(self,ctx,*,arg):
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


    @commands.command(name='givecoins',aliases=['gc'])
    async def givecoins(self,ctx,member: discord.Member = None,coins: int = 0):

        author = ctx.message.author
        SERVERID = str(ctx.message.guild.id)
        MEMBERID = str(member.id)

        if not author.guild_permissions.administrator:
            await ctx.send('Sorry good sir, you do not have permission to create an economy!',delete_after=20)
            return
        
        balance = gachadatabase.get_balance([SERVERID,MEMBERID])
        newbal = balance[2] + coins
        gachadatabase.set_balance([SERVERID,MEMBERID,newbal])

    @commands.command(name='setcoins',aliases=['sc'])
    async def setcoins(self,ctx,member: discord.Member = None,coins: int = 0):

        author = ctx.message.author
        SERVERID = str(ctx.message.guild.id)
        MEMBERID = str(member.id)

        if not author.guild_permissions.administrator:
            await ctx.send('Sorry good sir, you do not have permission to create an economy!',delete_after=20)
            return
        
        gachadatabase.set_balance([SERVERID,MEMBERID,coins])


    @commands.command(name='summon',aliases=['s'])
    async def summon(self,ctx):
        SERVERID = str(ctx.message.guild.id)
        MEMBERID = str(ctx.message.author.id)
        balance = gachadatabase.get_balance([SERVERID,MEMBERID])
        ID = randint(0,80000)
        if not balance:
            await ctx.send("You don't have an account set up on this server!")
            return
        tokens = balance[2]
        if tokens >=5:
            tokens = tokens - 5
            gachadatabase.set_balance([SERVERID,MEMBERID,tokens])
            value = randint(1,100)
            
            
            
            if value >= 1 and value <=50:
                threestars = gachadatabase.get_threestars(SERVERID)
                gachaplace = randint(0,len(threestars)-1)
                gacha = threestars[gachaplace]
                gachadatabase.add_hero([SERVERID,MEMBERID,gacha[0],gacha[1],gacha[2],gacha[3],gacha[4],gacha[5],3,ID])
                await ctx.send("You got the 3 star hero: **{}**!! ID: {} Description: {}".format(gacha[0],ID,gacha[6]))
            
            if value >=51 and value <=90:
                fourstars = gachadatabase.get_fourstars(SERVERID)
                gachaplace = randint(0,len(fourstars)-1)
                gacha = fourstars[gachaplace]
                gachadatabase.add_hero([SERVERID,MEMBERID,gacha[0],gacha[1],gacha[2],gacha[3],gacha[4],gacha[5],4,ID])
                await ctx.send("You got the 4 star hero: **{}**!! Description: {}".format(gacha[0],gacha[6]))

            if value >=91 and value <=100:
                fivestars = gachadatabase.get_fivestars(SERVERID)
                gachaplace = randint(0,len(fivestars)-1)
                gacha = fivestars[gachaplace]
                gachadatabase.add_hero([SERVERID,MEMBERID,gacha[0],gacha[1],gacha[2],gacha[3],gacha[4],gacha[5],5,ID])
                await ctx.send("You got the 5 star hero: **{}**!! Description: {}".format(gacha[0],gacha[6]))
        else:
            await ctx.send("Sorry, you don't have enough coins sir!")
            

    @commands.command('list3stars')
    async def list3stars(self,ctx):
        SERVERID = str(ctx.message.guild.id)
        threestars = gachadatabase.get_threestars(SERVERID)
        await ctx.send("There are currently **{}** Three Rarity Heroes on this server.".format(len(threestars)))
        newlist = create_filter_list(threestars)
        await ctx.send(newlist)
    
    @commands.command('list4stars')
    async def list4stars(self,ctx):
        SERVERID = str(ctx.message.guild.id)
        fourstars = gachadatabase.get_fourstars(SERVERID)
        await ctx.send("There are currently **{}** Four Rarity Heroes on this server.".format(len(fourstars)))
        newlist = create_filter_list(fourstars)
        await ctx.send(newlist)
    
    @commands.command('list5stars')
    async def list5stars(self,ctx):
        SERVERID = str(ctx.message.guild.id)
        fivestars = gachadatabase.get_fivestars(SERVERID)
        await ctx.send("There are currently **{}** Five Rarity Heroes on this server.".format(len(fivestars)))
        newlist = create_filter_list(fivestars)
        await ctx.send(newlist)






    @commands.command(name='checkbox',aliases=['cb','pc'])
    async def checkbox(self,ctx):
        SERVERID = str(ctx.message.guild.id)
        MEMBERID = str(ctx.message.author.id)

        barracks = gachadatabase.get_heroes([SERVERID,MEMBERID])
        if not barracks:
            await ctx.send("You got no boys, bro!")
        barrackslist = create_list(barracks)
        await ctx.send(barrackslist)
        print(barracks)
    
    @commands.command(name='killhero',aliases =['kh'])
    async def killhero(self,ctx,ID: int = 0):
        SERVERID = ctx.message.guild.id
        MEMBERID = ctx.author.id

        hero = gachadatabase.get_barracks_hero([SERVERID,MEMBERID,ID])
        if not hero:
            await ctx.send("You do not own a hero with this ID.")
            return

        if hero[9] == 3:
            coins = 2
        if hero[9] == 4:
            coins = 4
        if hero[9] == 5:
            coins = 10

        balance = gachadatabase.get_balance([SERVERID,MEMBERID])
        newbal = balance[2] + coins
        gachadatabase.set_balance([SERVERID,MEMBERID,newbal])
        gachadatabase.delete_barracks_hero(ID)  
        await ctx.send("**{}** has been deleted. Returning **{} LuigiCoins.**".format(hero[2],coins))




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