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


initial_extensions = [ 'cogs.Administrator','cogs.Audio',
                      'cogs.SmashBros', 'cogs.Fun', 'cogs.Help','cogs.Search','cogs.Economy','cogs.Dota',
                      'cogs.Utility']
bot = commands.Bot(command_prefix=get_prefix,
                   description='LuigiBot: General Purpose Bot!')
bot.remove_command('help')
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    
    print(
        f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    await bot.change_presence(activity=discord.Game(name='World of Warcraft', type=1, url='https://twitch.tv/Lefty43'))

    print(f'Successfully logged in and booted...!')

@bot.event
async def on_command_error(ctx,error):
    serverid = str(ctx.guild.id)
    server = await jsondb.load_event_server(serverid)
    if server is not None:
        for channel in server['Channel_Permissions']:
            if str(ctx.channel.id) == channel:
                if isinstance(error, commands.CheckFailure):
                    return await ctx.send("You do not have the permission required to use this command, **{}**".format(ctx.author.mention),delete_after=5)
                elif isinstance(error, commands.CommandNotFound):
                    return await ctx.send("Command not found.",delete_after=5)
        return await ctx.send("This channel is not set to have bot commands.")
    else:
        return await ctx.send("This channel is not set to have bot commands.")


'''
@bot.event
async def on_message(message):
    print(message.author.id)
    await message.add_reaction(":WutFace:288534331763458048")
'''


bot.run(api_key, bot=True, reconnect=True)



# client.loop.create_task(change_status())
