import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import youtube_dl
from itertools import cycle



Client = discord.Client()
client = commands.Bot(command_prefix = "!")
#client.remove_command('help')

Msg1 = 'Pokemon Emerald'
Msg2 = 'Final Fantasy X'
Msg3 = 'Dark Souls'
Msg4= 'Fire Emblem'
'''https://stackoverflow.com/questions/3199171/append-multiple-values-for-one-key-in-a-dictionary'''
status = [Msg1,Msg2,Msg3,Msg4]

players = {}
queues = {}

extensions = ['MusicBot','Fun','Administration']

@client.command()
async def load(extension):
    try:
        client.load_extension(extension)
        print('Loaded {}'.format(extension))
    except Exception as error:
        print('{} cannot be loaded.[{}]'.format(extension,error))

@client.command()
async def unload(extension):
    try:
        client.unload_extension(extension)
        print('Unloaded {}'.format(extension))
    except Exception as error:
        print('{} cannot be loaded.[{}]'.format(extension,error))


'''
@client.command()
async def checklist():
    queue = '!queue \n'
    play = '!play \n'
    vol = '!vol \n'
    skip= '!skip \n'
    playing = '!playing \n'
    pause = '!pause \n'
    resume = '!resume \n'
    stop= '!stop \n'
    await client.say()




    embed = discord.Embed(
        title = 'LuigiBot To-Do List! ',
        description = '!queue\n  !play\n   !vol\n !skip\n  !playing\n !pause\n !resume\n !stop\n',
        colour = discord.Colour.blue())
    await client.say(embed=embed)
'''


#Embedding
@client.command()
async def displayembed():
    embed = discord.Embed(
        title = 'Title',
        description = 'This is a description.',
        colour = 0x16820d
    )
    embed.set_footer(text='This is a footer.')
    embed.set_image(url='')
    embed.set_thumbnail(url='')
    embed.set_author(name='Author Name', icon_url = '')
    embed.add_field(name='Field Name',value='Field Value',inline=True)
    embed.add_field(name='Field Name',value='Field Value',inline=False)
    embed.add_field(name='Field Name',value='Field Value',inline=True)
    await client.say(embed=embed)


async def change_status():
    await client.wait_until_ready()
    msgs= cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game = discord.Game(name=current_status))
        await asyncio.sleep(60*60)






#####################################################################################

####~~~~~ On Ready ~~~~####

#This will let us know when the bot is ready to go.
@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='Wizball'))
    print("Bot is ready!")


####~~~~~~ Events ~~~~~~####

@client.event
async def on_message(message):
    print('A user has sent a message.')

    if message.content.lower() == "i love anthony":
        await client.send_message(message.channel,"Me too :blush::heart:")

    if message.content.lower() == "1900490freak":
        await client.send_message(message.channel,"$2 a call ")
    await client.process_commands(message)









#Help Command
'''
@client.command(pass_context=True)
async def help(ctx):
	author = ctx.message.author
	embed = discord.Embed(colour = discord.Colour.orange())

	embed.set_author(name='Help')
	embed.add_field(name='.ping',value='Returns Pong',inline = False)
	await client.send_message(author,embed=embed)
'''


@client.event
async def on_reaction_add(reaction,user):
	channel = reaction.message.channel
	await client.send_message(channel,'{} has added {} to the message: {}',format(user.name,reaction.emoji,reaction.message.content))

@client.event
async def on_reaction_remove(reaction,user):
	channel = reaction.message.channel
	await client.send_message(channel,'{} has added {} to the message: {}',format(user.name,reaction.emoji,reaction.message.content))













client.loop.create_task(change_status())
if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded.[{}]'.format(extension,error))
    client.run("NTMzNDM4ODk1Njk5MDAxMzY0.DxrDTw.Y2Tptl--dp8BOygeCORS54V4zZY") #This is the bot's tokenID, used to turn on the bot.






'''
#This will let us know when the bot is ready to go.
@client.event
async def on_ready():
    print("Bot is ready!")

#This reads any chats and sees whenever "anthony sucks" is said, and sends out a message in response.
@client.event
async def on_message(message):
    if message.content == "anthony sucks":
        await client.send_message(message.channel,"yeah haha what a lameo")


#Similarly to above, this reads whenever "nice" is said, and sends out a message.
@client.event
async def on_message(message):
    if message.content == "nice":
        await client.send_message(message.channel,"nice.")

#This reads the first word written in everyones messages, and checks if !SAY or !PING are said, and sends a message in response.
@client.event
async def on_message(message):
    if message.content.upper().startswith('!PING'):
        userID = message.author.id  #We track the ID of the user who sent out the ping.
        await client.send_message(message.channel, "<@%s> Pong!" % (userID)) #We send out a pong response to the channel and ping the user.
    if message.content.upper().startswith('!SAY'):
        args = message.content.split(" ") #If the !SAY command is used, then we split the rest of the message.
        #args[0]= !SAY
        #args[1] = Hey
        #args[2] = There!
        await client.send_message(message.channel, "%s" % (" ".join(args[1:]))) #From arg1 onwards, we join the message and return it.

'''
