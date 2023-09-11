import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import youtube_dl
from itertools import cycle
import sqlite3
import tokens
import json
from core import jsondb
from discord.ext.commands import has_permissions, MissingPermissions
import winreg as reg  
import getpass
import os
import random
from pathlib import Path
USER_NAME = getpass.getuser()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.typing = True
intents.presences = True
intents.messages = True


api_key = tokens.discord_api
#
#   LuigiBot - Discord Bot ver.0.1.0
#
#   Made by Faris (Lefty) Al-khatahtbeh
#


status = ['Pokemon Emerald', 'Final Fantasy X',
          'Dark Souls', 'Fire Emblem Heroes']
servers = {}



def get_prefix(bot, message):
    prefixes = ['!']
    # If bot is in DM, then they can only use commands starting with ?
    if not message.guild:
        return '?'
    return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = [ 'cogs.Administrator',
                      'cogs.SmashBros', 'cogs.Fun', 'cogs.Help','cogs.Utility','cogs.Dota','cogs.DrWilyDB','cogs.Yugioh','cogs.Economy']
bot = commands.Bot(command_prefix=get_prefix,
                   description='LuigiBot: General Purpose Bot!',intents=intents)
bot.remove_command('help')

        


@bot.event
async def on_ready():
    
    game = random_game()
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    await bot.change_presence(activity=discord.Game(name=game, type=1, url='https://twitch.tv/Lefty43'))
    print(f'Successfully logged in and booted...!')

    if __name__ == '__main__':
        for extension in initial_extensions:
            await bot.load_extension(extension)
            print(extension)
    # helptext = "```"
    # for command in bot.commands:
    #     helptext+=f"{command}\n"
    # helptext+="```"
    # print(helptext)




def random_game():
    games_list = ['World of Warcraft','Donkey Kong 64',"Cheggars' Party Quiz",'Family Feud','Project M','Shadow the Hedgehog','Sonic 06','Comic Bakery']
    game = random.randrange(0,len(games_list)-1)
    return games_list[game]


@bot.event
async def on_command_error(ctx,error):
    print(error)
    serverid = str(ctx.guild.id)
    server = await jsondb.load_event_server(serverid)
    if server is not None:
        for channel in server['Channel_Permissions']:
            if str(ctx.channel.id) == channel:
                if isinstance(error, commands.MissingPermissions):
                    return await ctx.send("You do not have the permission required to use this command, **{}**".format(ctx.author.mention),delete_after=5)
                elif isinstance(error, commands.CommandNotFound):
                    return await ctx.send("Command not found.",delete_after=5)
                else:
                    return await ctx.send("{}".format(error))
        return await ctx.send("Unknown error")
    else:
        return await ctx.send("This channel is not set to have bot commands.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # if not message.guild:
    #     try:
    #         await message.channel.send("This is a DM.")
    #     except discord.errors.Forbidden:
    #         pass
    # else:
    #     pass
    await bot.process_commands(message)

'''
@bot.event
async def on_message(message):
    print(message.author.id)
    await message.add_reaction(":WutFace:288534331763458048")
'''






bot.run(api_key, reconnect=True)



# client.loop.create_task(change_status())
