#Clear
@client.command(pass_context=True)
async def clear(ctx,amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel,limit = int(amount)):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say('Messages deleted.')
    #Need to make sure to do error checks later, such as if the user doesn't input an integer, or also inputs a decimal value.
