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
from discord.utils import get


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    '''
    @commands.Cog.listener
    async def on_message(message):
        if message.author == message.guild.me:
            #emoji = get(self.get_all_emojis(),name='wastebasket')
            await message.add_reaction("wastebasket")
    '''    