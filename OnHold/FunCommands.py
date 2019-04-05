#Ping
'''
@client.command()
async def ping():
    await client.say('Pong!') #say can only be used in client commands, where say is similar to send_message, except it knows what channel to send the message to. 
'''
#Echo
@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)
