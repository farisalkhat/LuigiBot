    

    @commands.command(name='createmove')
    async def addgachamove(self,ctx,*,arg):
        arg = arg.split(';')
        author = ctx.message.author
        SERVERID = str(ctx.message.guild.id)
        CHANNELID = str(ctx.message.channel.id)

        if not author.guild_permissions.administrator:
            await ctx.send('Sorry good sir, you do not have permission to modify the database!',delete_after=10)
            return
        gachadatabase.add_gacha_move(arg)
    

    @commands.command(name='setgacha')
    async def setgacha(self,ctx,*,arg):
        """
        Sets the channel for gacha commands to occur.
        """
        author = ctx.message.author
        SERVERID = str(ctx.message.guild.id)
        CHANNELID = str(ctx.message.channel.id)


        if not author.guild_permissions.administrator:
            await ctx.send('Sorry good sir, you do not have permission to modify the database!',delete_after=10)
            return
        gachadatabase.set_battle_channel([SERVERID,CHANNELID])
        await ctx.send("Battles have been set to the **{}** channel.".format(ctx.message.channel),delete_after = 10)
    @commands.command(name='setbotcommands')
    async def setbotcommands(self,ctx,*,arg):
        """
        Sets the channel for botcommands to occur.
        """
        author = ctx.message.author
        SERVERID = str(ctx.message.guild.id)
        CHANNELID = str(ctx.message.channel.id)

        if not author.guild_permissions.administrator:
            await ctx.send('Sorry good sir, you do not have permission to modify the database!',delete_after=10)
            return
        database.set_bottcommands([SERVERID,CHANNELID])
        await ctx.send("Botcommands have been set to the **{}** channel.".format(ctx.message.channel),delete_after = 10)

def bot_allowed(serverid,channelid):
    SERVERID = str(ctx.message.guild.id)
    CHANNELID = str(ctx.message.channel.id)
    allowed = database.get_botchannel([SERVERID,CHANNELID])
    if not allowed:
        return False
    return True
def gacha_allowed(serverid,channelid):
    SERVERID = str(ctx.message.guild.id)
    CHANNELID = str(ctx.message.channel.id)
    allowed = gachadatabase.get_battle_channel([SERVERID,CHANNELID])

    if not allowed:
        return False
    return True
 
    '''        
    if allowed([serverid,channel]) is False:
        return await ctx.send("You cannot use this channel for gacha commands!!",delete_after=10)
    '''




        '''

        #Heroname;Movename;Type;PT;Power;
        if len(arg)==5:
            i = 0
            while i!=5:
                arg.append("NA")
                i=i+1
            arg.append(0,SERVERID)
            gachadatabase.add_gacha_move(arg)
            return await ctx.send("You have created the move **{}** for the Hero: **{}**.".format(arg[2],arg[1]))

        #Heroname;Movename;Type;PT;Power;Status1;
        if len(arg)==6:
            i = 0
            while i!=4:
                arg.append("NA")
                i=i+1
            arg.append(0,SERVERID)
            gachadatabase.add_gacha_move(arg)
            return await ctx.send("You have created the move **{}** for the Hero: **{}**.".format(arg[2],arg[1]))
            
        #Heroname;Movename;Type;PT;Power;Status1;Status2;
        if len(arg)==7:
            i = 0
            while i!=3:
                arg.append("NA")
                i=i+1
            arg.append(0,SERVERID)
            gachadatabase.add_gacha_move(arg)
            return await ctx.send("You have created the move **{}** for the Hero: **{}**.".format(arg[2],arg[1]))
        #Heroname;Movename;Type;PT;Power;Status1;Status2;Status3;
        if len(arg)==8:
            i = 0
            while i!=2:
                arg.append("NA")
                i=i+1
            arg.append(0,SERVERID)
            gachadatabase.add_gacha_move(arg)
            return await ctx.send("You have created the move **{}** for the Hero: **{}**.".format(arg[2],arg[1]))
        #Heroname;Movename;Type;PT;Power;Status1;Status2;Status3;Status4;
        if len(arg)==9:
            arg.append("NA")
            arg.append(0,SERVERID)
            gachadatabase.add_gacha_move(arg)
            return await ctx.send("You have created the move **{}** for the Hero: **{}**.".format(arg[2],arg[1]))
        #Heroname;Movename;Description;Type;PT;Power;Status1;Status2;Status3;Status4;Status5
        if len(arg)==10:
            gacha

        '''