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
from random import randint
from db import gachadatabase
import datetime
import threading


class Hero:
        def __init__(self,hero):
            self.Owner = hero[10]
            self.Number = hero[11]
            self.HeroName = hero[0]
            #self.Description = hero[]

            self.HP = hero[1]
            self.ATK = hero[2]
            self.DEF = hero[3]
            self.SDEF = hero[4]
            self.SPD =  hero[5]

            self.Move1 = hero[6]
            self.Move2 = hero[7]
            self.Move3 = hero[8]
            self.Move4 = hero[9]

            self.Status = []




class Battle:
    def __init__(self,Hero1,Hero2):
        self.Hero1 = Hero1
        self.Hero2 = Hero2
        self.Done = []

        if(self.Hero1.SPD > self.Hero2.SPD):
            self.Turn = [self.Hero1,self.Hero2]
        else:
            self.Turn = [self.Hero2,self.Hero1]

    def can_play(self,player):
        if player == self.Turn[0].Owner:
            return True
        return False

    def can_continue(self):
        return self.Turn

    def execute_status(self,input):
        heronum = input[0] #This has the number of the hero currently attacking.
        statuses = input[1:3] #This has both status effects of the move being executed.
        msg = input[3] #This has the message that we will return once the move has been completed.

        for status in statuses: #We will run through both statuses to see what is up!
            #There are 5 unique 2 character statuses. We will go through all 5 of them first, and then go through the 1 character ones if no match.
            if status[0:2] == 'NA': 
                #NA = Not available. No status effect, go to the next one. 
                continue

            elif status[0:2] == 'SB': 
                #SB = Self Buff. The next 3 characters will be either ATK,DEF,SDEF or SPD. The other characters is the value, so we extract those values.
                stat = status[2:5]
                value = int(status[5:])


                #Buff their own attack.
                if stat =='ATK':
                    if heronum == 1:
                        self.Hero1.ATK = self.Hero1.ATK + value
                        msg.append("**" +self.Hero1.HeroName + '** has increased their attack by **{}**'.format(value))
                    else:
                        self.Hero2.ATK = self.Hero2.ATK + value
                        msg.append("**" +self.Hero2.HeroName + '** has increased their attack by **{}**'.format(value))

                #Buff their own defense.  
                if stat == 'DEF':
                    if heronum == 1:
                        self.Hero1.DEF = self.Hero1.DEF + value
                        msg.append("**" +self.Hero1.HeroName + '** has increased their defense by **{}**'.format(value))
                    else:
                        self.Hero2.DEF = self.Hero2.DEF + value
                        msg.append("**" +self.Hero2.HeroName + '** has increased their defense by **{}**'.format(value))
                    
                #Buff their own special defense.
                if stat =='SDF':
                    if heronum == 1:
                        self.Hero1.SDEF = self.Hero1.SDEF + value
                        msg.append("**" +self.Hero1.HeroName + '** has increased their special defense by **{}**'.format(value))
                    else:
                        self.Hero2.SDEF = self.Hero2.SDEF + value
                        msg.append("**" +self.Hero2.HeroName + '** has increased their special defense by **{}**'.format(value))
                #Buff their own speed.
                if stat == 'SPD':
                    if heronum == 1:
                        self.Hero1.SPD = self.Hero1.SPD + value
                        msg.append("**" +self.Hero1.HeroName + '** has increased their speed by **{}**'.format(value))
                    else:
                        self.Hero2.SPD = self.Hero2.SPD + value
                        msg.append("**" +self.Hero2.HeroName + '** has increased their speed by **{}**'.format(value))

            
            #This checks if we're buffing the enemy.
            elif status[0:2] == 'EB':
                stat = status[2:5]
                value = int(status[5:])

                #Buff enemy attack.
                if stat =='ATK':
                    if heronum == 2:
                        self.Hero1.ATK = self.Hero1.ATK + value
                        msg.append("**" +self.Hero1.HeroName + '** got their attack increased by **{}**'.format(value))
                    else:
                        self.Hero2.ATK = self.Hero2.ATK + value
                        msg.append("**" +self.Hero2.HeroName + '** got their attack increased by **{}**'.format(value))

                #Buff enemy defense.    
                if stat == 'DEF':
                    if heronum == 2:
                        self.Hero1.DEF = self.Hero1.DEF + value
                        msg.append("**" +self.Hero1.HeroName + '** got their defense increased by **{}**'.format(value))
                    else:
                        self.Hero2.DEF = self.Hero2.DEF + value
                        msg.append("**" +self.Hero2.HeroName + '** got their defense increased by **{}**'.format(value))
                    
                #Buff enemy special defense.    
                if stat =='SDF':
                    if heronum == 2:
                        self.Hero1.SDEF = self.Hero1.SDEF + value
                        msg.append("**" +self.Hero1.HeroName + '** got their special defense increased by **{}**'.format(value))
                    else:
                        self.Hero2.SDEF = self.Hero2.SDEF + value
                        msg.append("**" +self.Hero2.HeroName + '** got their special defense increased by **{}**'.format(value))

                #Buff enemy speed.    
                if stat == 'SPD':
                    if heronum == 2:
                        self.Hero1.SPD = self.Hero1.SPD + value
                        msg.append("**" +self.Hero1.HeroName + '** got their speed increased by **{}**'.format(value))
                    else:
                        self.Hero2.SPD = self.Hero2.SPD + value
                        msg.append("**" +self.Hero2.HeroName + '** got their speed increased by **{}**'.format(value))
                
                






            elif status[0:2] == 'SD':
                stat = status[2:5]
                value = int(status[5:])


                if stat =='ATK':
                    if heronum == 1:
                        self.Hero1.ATK = self.Hero1.ATK - value
                        msg.append("**" +self.Hero1.HeroName + '** has decreased their attack by **{}**'.format(value))
                    else:
                        self.Hero2.ATK = self.Hero2.ATK - value
                        msg.append("**" +self.Hero2.HeroName + '** has decreased their attack by **{}**'.format(value))

                    
                if stat == 'DEF':
                    if heronum == 1:
                        self.Hero1.DEF = self.Hero1.DEF - value
                        msg.append("**" +self.Hero1.HeroName + '** has decreased their defense by **{}**'.format(value))
                    else:
                        self.Hero2.DEF = self.Hero2.DEF - value
                        msg.append("**" +self.Hero2.HeroName + '** has decreased their defense by **{}**'.format(value))
                    
                    
                if stat =='SDF':
                    if heronum == 1:
                        self.Hero1.SDEF = self.Hero1.SDEF - value
                        msg.append("**" +self.Hero1.HeroName + '** has decreased their special defense by **{}**'.format(value))
                    else:
                        self.Hero2.SDEF = self.Hero2.SDEF - value
                        msg.append("**" +self.Hero2.HeroName + '** has decreased their special defense by **{}**'.format(value))
                    
                if stat == 'SPD':
                    if heronum == 1:
                        self.Hero1.SPD = self.Hero1.SPD - value
                        msg.append("**" +self.Hero1.HeroName + '** has decreased their speed by **{}**'.format(value))
                    else:
                        self.Hero2.SPD = self.Hero2.SPD - value
                        msg.append("**" +self.Hero2.HeroName + '** has decreased their speed by **{}**'.format(value))




                
            elif status[0:2] == 'ED':
                stat = status[2:5]
                value = int(status[5:])


                if stat =='ATK':
                    if heronum == 2:
                        self.Hero1.ATK = self.Hero1.ATK - value
                        msg.append("**" +self.Hero1.HeroName + '** has decreased their attack by **{}**'.format(value))
                    else:
                        self.Hero2.ATK = self.Hero2.ATK - value
                        msg.append("**" +self.Hero2.HeroName + '** has decreased their attack by **{}**'.format(value))

                    
                if stat == 'DEF':
                    if heronum == 2:
                        self.Hero1.DEF = self.Hero1.DEF - value
                        msg.append("**" +self.Hero1.HeroName + '** has decreased their defense by **{}**'.format(value))
                    else:
                        self.Hero2.DEF = self.Hero2.DEF - value
                        msg.append("**" +self.Hero2.HeroName + '** has decreased their defense by **{}**'.format(value))
                    
                    
                if stat =='SDF':
                    if heronum == 2:
                        self.Hero1.SDEF = self.Hero1.SDEF - value
                        msg.append("**" +self.Hero1.HeroName + '** has decreased their special defense by **{}**'.format(value))
                    else:
                        self.Hero2.SDEF = self.Hero2.SDEF - value
                        msg.append("**" +self.Hero2.HeroName + '** has decreased their special defense by **{}**'.format(value))
                    
                if stat == 'SPD':
                    if heronum == 2:
                        self.Hero1.SPD = self.Hero1.SPD - value
                        msg.append("**" +self.Hero1.HeroName + '** has decreased their speed by **{}**'.format(value))
                    else:
                        self.Hero2.SPD = self.Hero2.SPD - value
                        msg.append("**" +self.Hero2.HeroName + '** has decreased their speed by **{}**'.format(value))
                
    


            if status[0] == 'S':
                print('lmao')
            if status[0] == 'E':
                print('lmao')



        return msg
        

    def execute_move(self,move):
        Attack = ''
        if move==1:
            Attack = self.Turn[0].Move1
        if move==2:
            Attack = self.Turn[0].Move2
        if move==3:
            Attack = self.Turn[0].Move3
        if move==4:
            Attack = self.Turn[0].Move4

        Hero_Number = self.Turn[0].Number
        Attack_Name = Attack[0]
        Attack_Type = Attack[1]
        Attack_Desc = Attack[2]
        Attack_A_Type = Attack[3]
        Attack_Power = Attack[4]
        Attack_Status1 = Attack[5]
        Attack_Status2 = Attack[6]

        msg = []

        '''
        if Attack_Type == self.Turn[0].Type:
                Attack_Power = Attack_Power * 1.5
        '''
        #TODO: If move is super effective against enemy


        for status in self.Turn[0].Status:
            if status == 'P':
                random = randint(1,2)
                if random == 1:
                    msg.append( self.Turn[0].HeroName + "is paralyzed and cannot attack!")
                    self.Turn.pop(0)
                    break
            if status == 'C':
                random = randint(1,5)
                if random == 3:
                    self.Turn[0].HP = self.Turn[0].HP-3
                    msg.append(self.Turn[0].HeroName + "hit themselves in confusion for 3HP!")
                    self.Turn.pop(0)
                    break
                    
            if status == 'BN':
                Attack_Power = Attack_Power * .5
            



        if self.Turn:
            if Attack_Power == 0:
                Attack_Power = 0
            else:
                Attack_Power = Attack_Power + self.Turn[0].ATK
            #TODO: Status effects of the move
            if self.Turn[0].Number==1:
                if Attack_A_Type == 'A':
                    DMG = Attack_Power - self.Hero2.DEF
                    if DMG > 0:
                        self.Hero2.HP = self.Hero2.HP - DMG
                        msg.append('**{}** used **{}**!  **{}** has taken **{}** damage!'.format(self.Turn[0].HeroName,Attack_Name,self.Hero2.HeroName, DMG ))
                    else:
                        msg.append('**{}** used **{}**!  **{}** has taken **{}** damage!'.format(self.Turn[0].HeroName,Attack_Name,self.Hero2.HeroName, 0 ))
                    self.Turn.pop(0)
                else:
                    DMG = Attack_Power - self.Hero2.SDEF
                    if DMG > 0:
                        self.Hero2.HP = self.Hero2.HP - DMG
                        msg.append('**{}** used **{}**!  **{}** has taken **{}** damage!'.format(self.Turn[0].HeroName,Attack_Name,self.Hero2.HeroName, DMG ))
                    else:
                        msg.append('**{}** used **{}**!  **{}** has taken **{}** damage!'.format(self.Turn[0].HeroName,Attack_Name,self.Hero2.HeroName, 0 ))
                    self.Turn.pop(0)

            else:
                if Attack_A_Type == 'A':
                    DMG = Attack_Power - self.Hero1.DEF
                    if DMG >0:
                        self.Hero1.HP = self.Hero1.HP - DMG
                        msg.append('**{}** used **{}**!  **{}** has taken **{}** damage!'.format(self.Turn[0].HeroName,Attack_Name,self.Hero1.HeroName, DMG ))
                    else:
                        msg.append('**{}** used **{}**!  **{}** has taken **{}** damage!'.format(self.Turn[0].HeroName,Attack_Name,self.Hero1.HeroName, 0 ))
                    self.Turn.pop(0)
                else:
                    DMG = Attack_Power - self.Hero1.SDEF
                    if DMG > 0:
                        self.Hero1.HP = self.Hero1.HP - DMG
                        msg.append('**{}** used **{}**!  **{}** has taken **{}** damage!'.format(self.Turn[0].HeroName,Attack_Name,self.Hero1.HeroName, DMG ))
                    else:
                        msg.append('**{}** used **{}**!  **{}** has taken **{}** damage!'.format(self.Turn[0].HeroName,Attack_Name,self.Hero1.HeroName, 0 ))
                    self.Turn.pop(0)


        input = [Hero_Number,Attack_Status1,Attack_Status2,msg]
        msg = self.execute_status(input) 

        if self.Hero1.HP <= 0 and self.Hero2.HP <= 0:
            msg.append("Cut the credits, it's a draw!")
            return
        if self.Hero1.HP <= 0:
            msg.append("**{}** faints. **{}** wins!".format(self.Hero1.HeroName,self.Hero2.HeroName))
            return
        if self.Hero2.HP <= 0:
            msg.append("**{}** faints. **{}** wins!".format(self.Hero2.HeroName,self.Hero1.HeroName))
            return
        


        if not self.Turn:
            if(self.Hero1.SPD > self.Hero2.SPD):
                self.Turn = [self.Hero1,self.Hero2]
            else:
                self.Turn = [self.Hero2,self.Hero1]
            msg.append("It is now **{}**'s turn!".format(self.Turn[0].HeroName))

        else:
            msg.append("It is now **{}**'s turn!".format(self.Turn[0].HeroName))

        return msg





    






class GachaBattle(commands.Cog):
    __slots__ = ('bot','battles',)
    def __init__(self,bot):
        self.bot = bot
        self.battles = {}

    def create(self,serverid,player1,player2):
        self.battles[serverid] = Battle(player1,player2)


    @commands.command(name='battlemove')
    async def battlemove(self,ctx,move:int):
        battle = self.battles.get(ctx.message.guild.id)
        if not battle:
            return await ctx.send("There isn't a battle currently!")
        if not battle.can_play(ctx.message.author):
            return await ctx.send("You cannot play right now!")
        
        if move!= 0 and move!= 1 and move!= 2 and move!= 3 and move!= 4:
            return ctx.send("You didn't select a move! Try again with a move from 1-4, or 0 to forfeit.")
        
        if move==0:
            if(battle.turn[0].Number==1):
                return await ctx.send("**{}** has forfeited. **{}** has won!".format(battle.Hero1.Owner,battle.Hero2.Owner))
            else:
                return await ctx.send("**{}** has forfeited. **{}** has won!".format(battle.Hero2.Owner,battle.Hero1.Owner))
        
        msg = battle.execute_move(move)
        log = ""
        print(msg)
        for message in msg:
            log = log + message + " \n"

        await ctx.send(log)

        if not battle.can_continue():
            self.battles.pop(ctx.message.guild.id)
        


    @commands.command(name="battlestats")
    async def battle_stats(self,ctx):
        authorid = ctx.message.author.id
        serverid = ctx.message.guild.id
        battle =  self.battles.get(serverid,None)
        if not battle:
            return await ctx.send("There's no battle currently happening!")
        
        Hero1 = battle.Hero1
        Hero2 = battle.Hero2

        Hero1_Info = "Name: **" + Hero1.HeroName + "**  HP: " + str(Hero1.HP) + " ATK: " + str(Hero1.ATK) + " DEF: " + str(Hero1.DEF) + " SDEF: " + str(Hero1.SDEF) + " SPD: " + str(Hero1.SPD) + " \n"
        Hero2_Info = "Name: **" + Hero2.HeroName + "**  HP: " + str(Hero2.HP) + " ATK: " + str(Hero2.ATK) + " DEF: " + str(Hero2.DEF) + " SDEF: " + str(Hero2.SDEF) + " SPD: " + str(Hero2.SPD) + " \n"

        Hero_Info = Hero1_Info + Hero2_Info

        await ctx.send(Hero_Info)
        
    @commands.command(name="battlemovesets")   
    async def battle_movesets(self,ctx):
        authorid = ctx.message.author.id
        serverid = ctx.message.guild.id
        battle =  self.battles.get(serverid,None)
        if not battle:
            return await ctx.send("There's no battle currently happening!")
        
        Hero1 = battle.Hero1
        Hero2 = battle.Hero2

        Hero1_Info = "__**" + Hero1.HeroName + "**__\n"  
        Hero1_Info= Hero1_Info + "**" + Hero1.Move1[0]+ "** -  **Type:** " + Hero1.Move1[1] + "  **Description:** " + Hero1.Move1[2] + "  **Attack Type:** " + Hero1.Move1[3] + "  **Power:** " + str(Hero1.Move1[4]) 
        Hero1_Info= Hero1_Info + "  **S1:** " + Hero1.Move1[5] + "  **S2:** " +Hero1.Move1[6] + " \n" 
        Hero1_Info= Hero1_Info + "**" + Hero1.Move2[0]+ "** -   **Type:** " + Hero1.Move2[1] + "  **Description:** " + Hero1.Move2[2] + "  **Attack Type:** " + Hero1.Move2[3] + "  **Power:** " + str(Hero1.Move2[4])  
        Hero1_Info= Hero1_Info + "  **S1:** " + Hero1.Move2[5] + "  **S2:** " +Hero1.Move2[6] + " \n" 
        Hero1_Info= Hero1_Info + "**" + Hero1.Move3[0]+ "** -   **Type:** " + Hero1.Move3[1] + "  **Description:** " + Hero1.Move3[2] + "  **Attack Type:** " + Hero1.Move3[3] + "  **Power:** " + str(Hero1.Move3[4])  
        Hero1_Info= Hero1_Info + "  **S1:** " + Hero1.Move3[5] + "  **S2:** " +Hero1.Move3[6] + " \n" 
        Hero1_Info= Hero1_Info + "**" + Hero1.Move4[0]+ "** -   **Type:** " + Hero1.Move4[1] + "  **Description:** " + Hero1.Move4[2] + "  **Attack Type:** " + Hero1.Move4[3] + "  **Power:** " + str(Hero1.Move4[4])  
        Hero1_Info= Hero1_Info + "  **S1:** " + Hero1.Move4[5] + "  **S2:** " +Hero1.Move4[6] + " \n"
        
        Hero2_Info = "__**" + Hero2.HeroName + "**__\n" 
        Hero2_Info= Hero2_Info + "**" + Hero2.Move1[0]+ "** -   **Type:** " + Hero2.Move1[1] + "  **Description:** " + Hero2.Move1[2] + "  **Attack Type:** " + Hero2.Move1[3] + "  **Power:** " + str(Hero2.Move1[4]) 
        Hero2_Info= Hero2_Info + "  **S1:** " + Hero2.Move1[5] + "  **S2:** " +Hero2.Move1[6] + " \n" 
        Hero2_Info= Hero2_Info + "**" + Hero2.Move2[0]+ "** -   **Type:** " + Hero2.Move2[1] + "  **Description:** " + Hero2.Move2[2] + "  **Attack Type:** " + Hero2.Move2[3] + "  **Power:** " + str(Hero2.Move2[4])  
        Hero2_Info= Hero2_Info + "  **S1:** " + Hero2.Move2[5] + "  **S2:** " +Hero2.Move2[6] + " \n" 
        Hero2_Info= Hero2_Info + "**" + Hero2.Move3[0]+ "** -   **Type:** " + Hero2.Move3[1] + "  **Description:** " + Hero2.Move3[2] + "  **Attack Type:** " + Hero2.Move3[3] + "  **Power:** " + str(Hero2.Move3[4])  
        Hero2_Info= Hero2_Info + "  **S1:** " + Hero2.Move3[5] + "  **S2:** " +Hero2.Move3[6] + " \n" 
        Hero2_Info= Hero2_Info + "**" +Hero2.Move4[0]+ "** -   **Type:** " + Hero2.Move4[1] + "  **Description:** " + Hero2.Move4[2] + "  **Attack Type:** " + Hero2.Move4[3] + "  **Power:** " + str(Hero2.Move4[4]) 
        Hero2_Info= Hero2_Info + "  **S1:** " + Hero2.Move4[5] + "  **S2:** " +Hero2.Move4[6] + " \n"

        Hero_Info = Hero1_Info + Hero2_Info

        await ctx.send(Hero_Info)
    

    
    @commands.command(name="battle")
    async def battle(self,ctx, member: discord.Member):
        authorid = ctx.message.author.id
        serverid = ctx.message.guild.id


        current_battle = self.battles.get(serverid,None)

        if member == ctx.message.guild.me:
            return await ctx.send("Sorry, I don't have any heroes to use. :(")
        if member.id == authorid:
            return await ctx.send("You cannot battle yourself, IDIOT.")
        if current_battle:
            return await ctx.send("There is a battle in progress. Wait until it is done!")

        Hero1_Data = gachadatabase.get_primary_hero_ID([serverid,authorid])
        Hero1_ID = Hero1_Data[0]
        HeroStats1 = gachadatabase.get_primary_hero(Hero1_ID)
        HeroMoves1 = gachadatabase.get_primary_moves([Hero1_ID,serverid])
        for move in HeroMoves1:
            HeroStats1.append(move)
        HeroStats1.append(ctx.message.author)
        HeroStats1.append(1)

        opponentid = member.id
        Hero2_Data = gachadatabase.get_primary_hero_ID([serverid,opponentid])
        Hero2_ID = Hero2_Data[0]
        HeroStats2 = gachadatabase.get_primary_hero(Hero2_ID)
        HeroMoves2 = gachadatabase.get_primary_moves([Hero2_ID,serverid])
        for move in HeroMoves2:
            HeroStats2.append(move)
        opponent = member.name + "#" + member.discriminator
        HeroStats2.append(opponent)
        HeroStats2.append(2)


        Hero1_Info = Hero(HeroStats1)
        Hero2_Info = Hero(HeroStats2)

        self.create(ctx.message.guild.id,Hero1_Info,Hero2_Info)
        msg = "A battle has just started between {} and {}! No other battles on this server can take place until this is over!".format(Hero1_Info.Owner,Hero2_Info.Owner)
        print(Hero1_Info.Owner)
        print(Hero2_Info.Owner)
        await ctx.send(msg)
        





    