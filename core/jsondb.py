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
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\cogs\Economy\NewUsers.json",'r') as f:
        self.users = json.load(f)
async def open_items(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\cogs\Economy\NewItems.json",'r') as f:
        self.items = json.load(f)
async def open_shop(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\cogs\Economy\NewShop.json",'r') as f:
        self.shop = json.load(f)
async def open_servers(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\cogs\Economy\ServerPermissions.json",'r') as f:
        self.servers = json.load(f)



async def save_users(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\cogs\Economy\NewUsers.json",'w') as f:
        json.dump(self.users,f,indent=4)
async def save_items(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\cogs\Economy\NewItems.json",'w') as f:
        json.dump(self.items,f,indent=4)
async def save_shop(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\cogs\Economy\NewShop.json",'w') as f:
        json.dump(self.shop,f,indent=4)
async def save_servers(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\cogs\Economy\ServerPermissions.json",'w') as f:
        json.dump(self.servers,f,indent=4)

    

async def load_users(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\cogs\Economy\NewUsers.json",'r') as f:
        self.users= json.load(f)



async def load_items(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\cogs\Economy\NewItems.json",'r') as f:
        self.items = json.load(f)
async def load_shop(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\cogs\Economy\NewShop.json",'r') as f:
        self.shop = json.load(f)
async def load_servers(self):
    with open(r"C:\Users\Lefty\Desktop\Portfolio\Github-Repositories\LuigiBot\cogs\Economy\ServerPermissions.json",'r') as f:
        self.servers = json.load(f)



def permission(self,ctx):
    try:
        if self.servers[str(ctx.guild.id)] and self.servers[str(ctx.guild.id)]["Channelid"]== str(ctx.channel.id):
                return True
    except KeyError:
        return False

NOPERMISSION = "Bot has not been given permission to use commands in this channel."