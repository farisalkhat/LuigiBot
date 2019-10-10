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
import json




async def open_users(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\db\Users.json",'r') as f:
        self.users = json.load(f)
async def open_items(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\db\Items.json",'r') as f:
        self.items = json.load(f)
async def open_shop(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\db\Shop.json",'r') as f:
        self.shop = json.load(f)
async def open_servers(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\db\Servers.json",'r') as f:
        self.servers = json.load(f)



async def save_users(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\db\Users.json",'w') as f:
        json.dump(self.users,f,indent=4)
async def save_items(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\db\Items.json",'w') as f:
        json.dump(self.items,f,indent=4)
async def save_shop(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\db\Shop.json",'w') as f:
        json.dump(self.shop,f,indent=4)
async def save_servers(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\db\Servers.json",'w') as f:
        json.dump(self.servers,f,indent=4)

    

async def load_users(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\db\Economy\Users.json",'r') as f:
        self.users= json.load(f)



async def load_items(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\db\Items.json",'r') as f:
        self.items = json.load(f)
async def load_shop(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\db\Economy\Shop.json",'r') as f:
        self.shop = json.load(f)
async def load_servers(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\db\Servers.json",'r') as f:
        self.servers = json.load(f)

async def load_event_server(serverid):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\db\Servers.json",'r') as f:
        servers = json.load(f)
    try:
        server = servers[serverid]
        return server
    except KeyError:
        return None


def permission(self,ctx):
    try:
        for channelid in self.servers[str(ctx.guild.id)]['Channel_Permissions']:
            if channelid == str(ctx.message.channel.id):
                return True
        return 0
    except KeyError:
        print("KeyError")
        return False
    

def log_warning(self,ctx,userid,date,reason):
    server = self.servers[str(ctx.guild.id)]
    enforcer = str(ctx.author.id)
    try:
        server["Warnings"][userid].append([date,enforcer,reason])
    except KeyError:
        server["Warnings"][userid] = []
        server["Warnings"][userid].append([date,enforcer,reason])
def log_kick(self,ctx,userid,date,reason):
    server = self.servers[str(ctx.guild.id)]
    enforcer = str(ctx.author.id)
    try:
        server["Kicks"][userid].append([date,enforcer,reason])
    except KeyError:
        server["Kicks"][userid] = []
        server["Kicks"][userid].append([date,enforcer,reason])
def log_ban(self,ctx,userid,date,reason):
    server = self.servers[str(ctx.guild.id)]
    enforcer = str(ctx.author.id)
    try:
        server["Bans"][userid].append([date,enforcer,reason])
    except KeyError:
        server["Bans"][userid] = []
        server["Bans"][userid].append([date,enforcer,reason])


def return_warning_logs(self,ctx,userid):
    date =  ''
    enforcer = ''
    reason = ''

    try:
        user_logs = self.servers[str(ctx.guild.id)]['Warnings'][userid]
        for log in user_logs:
            date = date + log[0] + '\n'
            enforcer = enforcer + ctx.guild.get_member(int(log[1])).name + '\n'
            if len(log[2]) > 15:
                short_reason = log[2][:13] + '..'
                reason = reason + short_reason + '\n'
            else:
                reason = reason + log[2] + '\n'
        return date, enforcer, reason 
    except KeyError:
        return None, None, None


def return_ban_logs(self,ctx,userid):
    date =  ''
    enforcer = ''
    reason = ''

    try:
        user_logs = self.servers[str(ctx.guild.id)]['Bans'][userid]
        for log in user_logs:
            date = date + log[0] + '\n'
            enforcer = enforcer + ctx.guild.get_member(int(log[1])).name + '\n'
            if len(log[2]) > 15:
                short_reason = log[2][:13] + '..'
                reason = reason + short_reason + '\n'
            else:
                reason = reason + log[2] + '\n'
        return date, enforcer, reason 
    except KeyError:
        return None, None, None

def return_kick_logs(self,ctx,userid):
    date =  ''
    enforcer = ''
    reason = ''

    try:
        user_logs = self.servers[str(ctx.guild.id)]['Kicks'][userid]
        for log in user_logs:
            date = date + log[0] + '\n'
            enforcer = enforcer + ctx.guild.get_member(int(log[1])).name + '\n'
            if len(log[2]) > 15:
                short_reason = log[2][:13] + '..'
                reason = reason + short_reason + '\n'
            else:
                reason = reason + log[2] + '\n'
        return date, enforcer, reason 
    except KeyError:
        return None, None, None
    
def return_allwarn_logs(self,ctx):
    member = ''
    warnings = ''

    server_logs = self.servers[str(ctx.guild.id)]['Warnings']
    for member_warning in server_logs:
        member = member + ctx.guild.get_member(int(member_warning)).name + '\n'
        warnings = warnings + str(len(server_logs[member_warning])) + '\n'
        print(member_warning)
    return member, warnings 
        



NOPERMISSION = "Bot has not been given permission to use commands in this channel."