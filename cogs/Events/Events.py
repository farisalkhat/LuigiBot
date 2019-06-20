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

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
