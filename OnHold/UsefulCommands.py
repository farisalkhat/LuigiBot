#~~~~~ Miscellaneous ~~~~~#
@client.command(pass_context=True)
async def avatar(ctx):
    if (ctx.message.mentions.__len__()>0):
        for user in ctx.message.mentions:
            await client.say(user.avatar_url)
        
    else:
        await client.say('You need to mention a user to get their image url.')
