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



def permission(self,ctx):
    try:
        for channelid in self.servers[str(ctx.guild.id)]['Channel_Permissions']:
            if channelid == str(self.channel.id):
                return True 
        return False
    except KeyError:
        return False

NOPERMISSION = "Bot has not been given permission to use commands in this channel."