import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import youtube_dl
from itertools import cycle


#
#   LuigiBot - Discord Bot ver.0.1.0
#
#   Made by Faris (Lefty) Al-khatahtbeh
#


status = ['Pokemon Emerald', 'Final Fantasy X', 'Dark Souls', 'Fire Emblem Heroes']


def get_prefix(bot, message):
    prefixes = ['!']
    #If bot is in DM, then they can only use commands starting with ?
    if not message.guild:
        return '?'
    return commands.when_mentioned_or(*prefixes)(bot,message)

initial_extensions = ['cogs.Admin','cogs.Audio','cogs.SmashBros','cogs.Events','cogs.Fun','cogs.Help']
bot = commands.Bot(command_prefix = get_prefix, description = 'LuigiBot: General Purpose Bot!')
bot.remove_command('help')
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)



@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    await bot.change_presence(activity=discord.Game(name='World of Warcraft', type=1, url='https://twitch.tv/Lefty43'))

    print(f'Successfully logged in and booted...!')



async def change_status():
    await bot.wait_until_ready()
    msgs= cycle(status)

    while not bot.is_closed():
        current_status = next(msgs)
        activity = discord.Game(name=current_status)
        await bot.change_presence(status=discord.Status.idle, activity=activity)
        await asyncio.sleep(60*60)




bot.run("",bot=True,reconnect=True)

#client.loop.create_task(change_status())
