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
from db import database
from core.helper import permission
import json
from db import dota
from datetime import datetime,timedelta,date


from core import jsondb





class NewEconomy(commands.Cog):
    __slots__ = ('users','items','shop','servers')
    def __init__(self,bot):
        self.bot = bot
        self.users = {}
        self.items = {}
        self.shop = {}
        self.servers = {}


    @commands.command(name="createeconomy")
    async def neweconomy(self,ctx):
        memberslist = ctx.message.guild.members
        for member in memberslist:
            memberid = member.id
            if not str(memberid) in self.users:
                self.users[str(memberid)] = {
                    'Name': member.name,
                    'Level': 1,
                    'Experience': 0,

                    'Daily': {'Year':1990,
                        'Month':5,
                        'Day': 15,
                        'Hour':1,
                        },
                    'Weekly': {'Year':1990,
                        'Month':5,
                        'Day': 15,
                        'Hour':1,
                        },

                    'Inventory': ['1','1','2','2','2','2'],
                    'Coins': 25,
                    'Rigged':0,

                    'SmashProfile': { 'Tag':'' ,
                                    'SwitchCode': '',
                                    'Main': [],
                                    'Secondaries': [],
                                    'Pockets':[],
                                    'Games':[],
                                    'Region':'',
                                    'Note':'',
                                    'Colour':'',
                                    'Image':''
                    },
                    'OsuProfile' : {'Name':'', 'OsuTag':''},
                    'DotaProfile': {'Name':'', 'Steam32id': ''}

                }

        await jsondb.save_users(self)
    
    @commands.command(name="daily")
    async def daily(self,ctx):
        await jsondb.load_users(self)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)

        userid = str(ctx.author.id)
        time = self.users[userid]['Daily']
        date = datetime(time['Year'], time['Month'], time['Day'], 0, 0)
        if date.day == datetime.today().day:
            return await ctx.send("You cannot collect any daily rewards for today!")
        time['Year'] = datetime.today().year
        time['Day'] = datetime.today().day
        time['Month'] = datetime.today().month
        self.users[userid]['Coins'] = self.users[userid]['Coins'] + 20
        await jsondb.save_users(self)
        await ctx.send('**{}** has claimed his daily reward of **20 coins!**'.format(ctx.author))
    
    @commands.command(name="weekly")
    async def weekly(self,ctx):
        await jsondb.load_users(self)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)

        userid = str(ctx.author.id)
        time = self.users[userid]['Weekly']
        date = datetime(time['Year'], time['Month'], time['Day'], 0, 0)
        today = datetime.today()
        if (today - date).days < 7:
            return await ctx.send("You cannot collect any weekly rewards today!")
        time['Year'] = datetime.today().year
        time['Day'] = datetime.today().day
        time['Month'] = datetime.today().month
        self.users[userid]['Coins'] = self.users[userid]['Coins'] + 100
        await jsondb.save_users(self)
        await ctx.send('**{}** has claimed his weekly reward of **100 coins!**'.format(ctx.author))

    @commands.command(name="balance")
    async def newbalance(self,ctx,member:discord.Member = None): 
        await jsondb.load_users(self)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        if member is None:
            userid = str(ctx.message.author.id)
            user = ctx.author
        else:
            userid = str(member.id)  
            user = member

        if not userid in self.users:
            await ctx.send('**{}**, you do not have a profile currently!')
        coins = self.users[userid]['Coins']
        await ctx.send('**{}** currently has **{} Coins**.'.format(user,coins),delete_after=10)   

    @commands.command(name="inventory")
    async def inventory(self,ctx): 
        await jsondb.load_users(self)
        await jsondb.load_items(self)

        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)

            
        userid = str(ctx.message.author.id)
        
        if userid not in self.users:
            await ctx.send('**{}**, you do not have a profile currently!')
        inventory = self.users[userid]['Inventory']
        itemnames = ''
        itemtypes = ''
        itemids = ''

        for item in inventory:
            if item in self.items:
                itemids   = itemids + self.items[item]['ItemID'] + '\n'
                itemnames = itemnames + self.items[item]['ItemName'] + '\n'
                itemtypes = itemtypes + self.items[item]['ItemType'] + '\n'
            
        if itemids is None:
            return await ctx.send("Your inventory is empty.")
        embed=discord.Embed(title="{}'s Inventory".format(ctx.message.author.name))
        embed.add_field(name='Item ID', value=itemids, inline=True)
        embed.add_field(name='Item Name', value=itemnames, inline=True)
        embed.add_field(name='Item Type', value=itemtypes, inline=True)
        await ctx.send(embed=embed,delete_after=20)

    @commands.command(name="shop")
    async def open_shop(self,ctx): 
        guild = ctx.guild
        await jsondb.load_shop(self)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)

        serverid = str(ctx.guild.id)
        if serverid not in self.shop:
            self.shop[serverid] = {
                    'Name': guild.name,
                    'Inventory': ['1']
                }
            await ctx.send("**{}** does not have a shop. I've just created one though!".format(guild.name))
            await jsondb.save_shop(self)
        shop = self.shop[serverid]
        items = []

        for itemID in shop['Inventory']:
            item = self.items[itemID]
            price = item['Price']

            itemname = '**'+item['ItemName']+'**' + ' -- ' + '__{} coins__'.format(price) + '\t **ID: '+item['ItemID']+'** '+ '\n'
            itemdesc = itemname + item['Description'] + '\n'
            items.append(itemdesc)
        
        itemstr = ''
        for item in items:
            itemstr = itemstr + item

        embed=discord.Embed(title="**{}'s Shop**".format(ctx.guild.name))
        embed.add_field(name='Current items in the shop', value=itemstr, inline=True)    

        await ctx.send(embed=embed)
            
    @commands.command(name="shopadd")
    async def shopadd(self,ctx,index:str): 
        await jsondb.load_shop(self)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)

        author =ctx.author
        serverid = str(ctx.guild.id)
        guild = ctx.guild
        if not author.guild_permissions.administrator:
            await ctx.send('Sorry good sir, you do not have permission to modify the database!',delete_after=10)
            return
        if serverid not in self.shop:
            return await ctx.send("Sorry, there is no shop set up on this server!",delete_after=15)
        if index not in self.items:
            return await ctx.send("Sorry, that item does not exist!")
        if index in self.shop[serverid]['Inventory']:
            return await ctx.send("This item is already in the shop!")
        self.shop[serverid]['Inventory'].append(index)
        await jsondb.save_shop(self)
        await ctx.send("The item: **{}**, has been added to the **{}** shop!".format(self.items[index]['ItemName'],guild.name))

    @commands.command(name="shoprem")
    async def shoprem(self,ctx,index:str): 
        await jsondb.load_shop(self)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)

        author =ctx.author
        serverid = str(ctx.guild.id)
        guild = ctx.guild
        if not author.guild_permissions.administrator:
            await ctx.send('Sorry good sir, you do not have permission to modify the database!',delete_after=10)
            return
        if serverid not in self.shop:
            return await ctx.send("Sorry, there is no shop set up on this server!",delete_after=15)
        if index not in self.items:
            return await ctx.send("Sorry, that item does not exist!")
        if index not in self.shop[serverid]['Inventory']:
            return await ctx.send("This shop does not sell this item!")
        self.shop[serverid]['Inventory'].remove(index)
        await jsondb.save_shop(self)
        await ctx.send("The item: **{}**, has been added to the **{}** shop!".format(self.items[index]['ItemName'],guild.name))
        
    @commands.command(name="shopbuy")
    async def shopbuy(self,ctx,index:str): 
        await jsondb.load_shop(self)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        author =ctx.author

        serverid = str(ctx.guild.id)
        authorid = str(ctx.author.id)
        if serverid not in self.shop:
            return await ctx.send("Sorry, there is no shop set up on this server!",delete_after=15)
        if index not in self.items:
            return await ctx.send("Sorry, that item does not exist!")
        if index not in self.shop[serverid]['Inventory']:
            return await ctx.send("This shop does not sell this item!")
        if self.users[authorid]['Coins'] - int(self.items[index]['Price']) < 0 :
            return await ctx.send("Sorry, you do not have enough to purchase that!")
        self.users[authorid]['Coins'] =  self.users[authorid]['Coins'] - int(self.items[index]['Price'])
        self.users[authorid]['Inventory'].append(index)
        await jsondb.save_users(self)
        await ctx.send("**{}** has purchased **{}** for **{}** coins.".format(author.name,self.items[index]['ItemName'],self.items[index]['Price']))

    @commands.command(name="itemdb")
    async def all_items(self,ctx): 
        await jsondb.load_shop(self)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        if permission(ctx.guild.id,ctx.channel.id) is False:
            return await ctx.send("This channel has not been set to use **New Economy Commands**.")
        userid = str(ctx.message.author.id)

        if not userid in self.users:
            await ctx.send('**{}**, you do not have a profile currently!')
        

        itemnames = ''
        itemtypes = ''
        itemids = ''

        for item in self.items:
            itemids   = itemids + self.items[item]['ItemID'] + '\n'
            itemnames = itemnames + self.items[item]['ItemName'] + '\n'
            itemtypes = itemtypes + self.items[item]['ItemType'] + '\n'

        embed=discord.Embed(title="{}'s Inventory".format(ctx.message.author.name))
        embed.add_field(name='Item ID', value=itemids, inline=True)
        embed.add_field(name='Item Name', value=itemnames, inline=True)
        embed.add_field(name='Item Type', value=itemtypes, inline=True)
        await ctx.send(embed=embed,delete_after=20)
    
    @commands.command(name="item")
    async def item_find(self,ctx,index:str,member:discord.Member=None):
        await jsondb.load_shop(self)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)

        if index not in self.items:
            return await ctx.send("Sorry, that item does not exist!")
        item = self.items[index]

        price = item['Price']
        itemname = '**'+item['ItemName']+'**' + ' -- ' + '__{} coins__'.format(price) + '\n**__ID:__** '+item['ItemID']+ ' \t**__Item Type:__** ' + item['ItemType'] + '\t**__Use:__** ' + item['Use'] + '\t**__Purchasable:__** ' + item['Sell'] + '\n'
        itemdesc = itemname + item['Description'] + '\n'

        await ctx.send(itemdesc)
        
    @commands.command(name='setcoins',aliases=['sc'])
    async def setcoins(self,ctx,member: discord.Member = None,coins: int = 0):
        """
        Sets coins to a user. Requires admin privileges to execute this command. 
        Use !givecoins to give coins of a specific amount to a user.

        Usage:
        !setcoins @Lefty#6430 50
        !sc @Lefty#6430 50
        """
        jsondb.load_users(self)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        author = ctx.message.author

    
        
        if not author.guild_permissions.administrator:
            await ctx.send('Sorry **{}**, you do not have permission to use this command.'.format(author.name),delete_after=20)
            return
        if member is None:
            return await ctx.send('**{]**, you must target a user first before using this command.',delete_after=20)
        
        userid = str(member.id)
        self.users[userid]['Coins'] = coins
        await jsondb.save_users(self)
        await ctx.send("**{}**, you now have a balance of **{}** Coins!".format(member,coins))

    @commands.command(name="use")
    async def use(self,ctx,index:str,member:discord.Member=None):
        jsondb.load_users(self)
        await jsondb.load_servers(self)
        if jsondb.permission(self,ctx) is False:
            return await ctx.send(jsondb.NOPERMISSION)
        author = ctx.author
        userid = str(ctx.author.id)
        if index not in self.items:
            return await ctx.send("Sorry, that item does not exist!")
        if index not in self.users[userid]['Inventory']:
            return await ctx.send("Sorry, you do not own that item!")
        item = self.items[index]
        if item['Use']=='No':
            return await ctx.send("You cannot use this item!")
        await ctx.send('This is the item you are trying to use: **{}**'.format(item['ItemName']))

        if index == '1':
            self.users[userid]['Level'] = self.users[userid]['Level'] + 1
            self.users[userid]['Inventory'].remove(index)
            await jsondb.save_users(self)
            return await ctx.send("**{}** has used **{}** and gained a level! Your level is now **{}**.".format(author,item['ItemName'],str(self.users[userid]['Level'])))
        if index =='2':
            if member is None:
                return await ctx.send("**{}**, you must target a user to bless their Smash Profile.".format(author))
            memberid = str(member.id)
            self.users[memberid]['SmashProfile']['Main'] = 'Goku'
            return await jsondb.save_users(self)
        if index == '3':
            if  self.users[userid]['Rigged'] == 1:
                return await ctx.send("You're already rigging the system, bro!")
            else:
                self.users[userid]['Rigged'] = 1
                self.users[userid]['Inventory'].remove(index)
                await jsondb.save_users(self)
            return await ctx.send("**{}** has used **{}** and is now insanely lucky!".format(author,item['ItemName']))
        if index =='4':
            if member is None:
                return await ctx.send("**{}**, you must target a user to bless their Smash Profile.".format(author))
            roles = ctx.guild.roles
            for role in roles:
                if role.name =='BANNED':
                    await member.add_roles(role)
                    self.users[userid]['Inventory'].remove(index)
                    await jsondb.save_users(self)
                    return await ctx.send('**{}** has banned **{}**! Hilarious!'.format(ctx.author,member))
            
            await ctx.guild.create_role(name='BANNED',colour=discord.Colour.dark_grey())
            await member.add_roles(role)
            self.users[userid]['Inventory'].remove(index)
            await jsondb.save_users(self)
            return await ctx.send('**{}** has banned **{}**! Hilarious!'.format(ctx.author,member))

            





days = 9465
start = date(1990,1,1)
delta = timedelta(days)   
offset = start + delta


    

            



