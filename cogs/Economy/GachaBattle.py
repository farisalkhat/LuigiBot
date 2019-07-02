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
from core.helper import gacha_allowed
import datetime
import threading

class Owner:
    def __init__(self,Player_Primaries):
        self.Owner = Player_Primaries[4]
        self.Player_Number = Player_Primaries[6]
        serverid = Player_Primaries[5]

        P1_Hero1 = gachadatabase.get_primary_hero1(Player_Primaries[0])
        P1_HeroMoves1 = gachadatabase.get_primary_moves1([Player_Primaries[0],serverid])
        for move in  P1_HeroMoves1:
            P1_Hero1.append(move)
        self.Hero1 = Hero(P1_Hero1)


        P1_Hero2 = gachadatabase.get_primary_hero2(Player_Primaries[1])
        if not P1_Hero2:
            self.Hero2 = Hero(['None',0,0,0,0,0,'None',['None','None','None','None',0,'None','None','None','None','None'],['None','None','None','None',0,'None','None','None','None','None'],
            ['None','None','None','None',0,'None','None','None','None','None'],['None','None','None','None',0,'None','None','None','None','None']])

        else:
            P1_HeroMoves2 = gachadatabase.get_primary_moves2([Player_Primaries[1],serverid])
            
            for move in  P1_HeroMoves2:
                P1_Hero2.append(move)
            self.Hero2 = Hero(P1_Hero2)



        P1_Hero3 = gachadatabase.get_primary_hero3(Player_Primaries[2])
        if not P1_Hero3:
            self.Hero3 = Hero(['None',0,0,0,0,0,'None',['None','None','None','None',0,'None','None','None','None','None'],['None','None','None','None',0,'None','None','None','None','None'],
            ['None','None','None','None',0,'None','None','None','None','None'],['None','None','None','None',0,'None','None','None','None','None']])
        else:
            P1_HeroMoves3 = gachadatabase.get_primary_moves3([Player_Primaries[2],serverid])
            for move in  P1_HeroMoves3:
                P1_Hero3.append(move)
            self.Hero3 = Hero(P1_Hero3)


        P1_Hero4 = gachadatabase.get_primary_hero4(Player_Primaries[3])
        if not P1_Hero4:
            self.Hero4 = Hero(['None',0,0,0,0,0,'None',['None','None','None','None',0,'None','None','None','None','None'],['None','None','None','None',0,'None','None','None','None','None'],
            ['None','None','None','None',0,'None','None','None','None','None'],['None','None','None','None',0,'None','None','None','None','None']])
        else:
            P1_HeroMoves4 = gachadatabase.get_primary_moves4([Player_Primaries[3],serverid])
            for move in  P1_HeroMoves4:
                P1_Hero4.append(move)
            self.Hero4 = Hero(P1_Hero4)
        

        self.Current = self.Hero1
        
    def print_heros(self):
        msg = []
        msg.append("**{}**'s team!".format(self.Owner))
        msg.append('Hero1: **' + self.Hero1.HeroName + '**  HP: ' + str(self.Hero1.HP) +'  ATK: ' + 
        str(self.Hero1.ATK) + '  DEF: ' + str(self.Hero1.DEF) +'  SDEF: ' + str(self.Hero1.SDEF) +'  SPD: ' + str(self.Hero1.SPD))

        if self.Hero2.HeroName is not 'None':
            msg.append('Hero2: **' + self.Hero2.HeroName + '**  HP: ' + str(self.Hero2.HP) +'  ATK: ' + 
            str(self.Hero2.ATK) + '  DEF: ' + str(self.Hero2.DEF) +'  SDEF: ' + str(self.Hero2.SDEF) +'  SPD: ' + str(self.Hero2.SPD))
        if self.Hero3.HeroName is not 'None':
            msg.append('Hero3: **' + self.Hero3.HeroName + '**  HP: ' + str(self.Hero3.HP) +'  ATK: ' + 
            str(self.Hero3.ATK) + '  DEF: ' + str(self.Hero3.DEF) +'  SDEF: ' + str(self.Hero3.SDEF) +'  SPD: ' + str(self.Hero3.SPD))
        if self.Hero4.HeroName is not 'None':
            msg.append('Hero4: **' + self.Hero4.HeroName + '**  HP: ' + str(self.Hero4.HP) +'  ATK: ' + 
            str(self.Hero4.ATK) + '  DEF: ' + str(self.Hero4.DEF) +'  SDEF: ' + str(self.Hero4.SDEF) +'  SPD: ' + str(self.Hero4.SPD))
        
        log = ""
        for message in msg:
            log = log + message + " \n"
        return log


class Hero:
        def __init__(self,hero):
            self.HeroName = hero[0]

            self.HP = hero[1]
            self.ATK = hero[2]
            self.DEF = hero[3]
            self.SDEF = hero[4]
            self.SPD =  hero[5]

            self.Move1 = hero[7]
            self.Move2 = hero[8]
            self.Move3 = hero[9]
            self.Move4 = hero[10]

            self.Type = hero[6]
            self.Status = []




class Battle:
    def __init__(self,Player1,Player2):
        self.Player1 = Player1
        self.Player2 = Player2
        self.HeroSwap = 0
        


        self.Hero1 = Player1.Current
        self.Hero2 = Player2.Current
        

        if self.Hero1.SPD > self.Hero2.SPD:
            self.Turn = [self.Hero1,self.Hero2]
            self.HeroTurn = 1
        elif self.Hero2.SPD > self.Hero1.SPD:
            self.Turn = [self.Hero2,self.Hero1]
            self.HeroTurn = 2
        elif self.Hero1.SPD == self.Hero2.SPD:
            self.Turn = [self.Hero1,self.Hero2]
            self.HeroTurn = 1





    def can_play(self,player):
        playername = player.name + "#" + player.discriminator

        if self.HeroSwap==1:
            if playername == self.Player1.Owner:
                return True
            else:
                return False
        
        if self.HeroSwap==2:
            if playername == self.Player2.Owner:
                return True
            else:
                return False
        if self.HeroTurn==1:
            if playername == self.Player1.Owner:
                return True
            else:
                return False
        if self.HeroTurn==2:
            if playername == self.Player2.Owner:
                return True
            else:
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
                continue
            
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
                continue
                






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
                continue



                
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
                continue
                
    


            else:
                give_status = ''
                if status[1:3] == 'PZ':
                    print('Attempting paralysis..')
                    chance = int(status[3:])
                    r = randint(1,100)
                    if r <= chance:
                        give_status = 'PARALYZED'
                        if status[0] == 'S':
                            if heronum == 1 and give_status not in self.Hero1.Status:
                                self.Hero1.Status.append(give_status)
                                msg.append("**" +self.Hero1.HeroName + '** has paralyzed themself!')
                            elif give_status not in self.Hero2.Status:
                                self.Hero2.Status.append(give_status)
                                msg.append("**" +self.Hero2.HeroName + '** has paralyzed themself!')
                                
                        else:
                            if heronum == 1 and give_status not in self.Hero2.Status:
                                self.Hero2.Status.append(give_status)
                                msg.append("**" +self.Hero1.HeroName + '** has paralyzed **{}**!'.format(self.Hero2.HeroName))
                            elif give_status not in self.Hero1.Status:
                                self.Hero1.Status.append(give_status)
                                msg.append("**" +self.Hero2.HeroName + '** has paralyzed **{}**!'.format(self.Hero1.HeroName))
                        print('Paralysis success!')
                if status[1:3] == 'NB':
                    print('Attempting burn..')
                    chance = int(status[3:])
                    r = randint(1,100)
                    if r <= chance:
                        give_status = 'BURNED'
                        if status[0] == 'S':
                            if heronum == 1 and give_status not in self.Hero1.Status:
                                self.Hero1.Status.append(give_status)
                                msg.append("**" +self.Hero1.HeroName + '** has burned themself!')
                            elif give_status not in self.Hero2.Status:
                                self.Hero2.Status.append(give_status)
                                msg.append("**" +self.Hero2.HeroName + '** has burned themself!')
                                
                        else:
                            if heronum == 1 and give_status not in self.Hero2.Status:
                                self.Hero2.Status.append(give_status)
                                msg.append("**" +self.Hero1.HeroName + '** has burned **{}**!'.format(self.Hero2.HeroName))
                            elif give_status not in self.Hero1.Status:
                                self.Hero1.Status.append(give_status)
                                msg.append("**" +self.Hero2.HeroName + '** has burned **{}**!'.format(self.Hero1.HeroName))
                        print('Burn success!')
                if status[1:3] == 'CF':
                    print('Attempting confusion..')
                    chance = int(status[3:])
                    r = randint(1,100)
                    if r <= chance:
                        give_status = 'CONFUSED'
                        if status[0] == 'S':
                            if heronum == 1 and give_status not in self.Hero1.Status:
                                self.Hero1.Status.append(give_status)
                                msg.append("**" +self.Hero1.HeroName + '** has confused themself!')
                            elif give_status not in self.Hero2.Status:
                                self.Hero2.Status.append(give_status)
                                msg.append("**" +self.Hero2.HeroName + '** has confused themself!')
                                
                        else:
                            if heronum == 1 and give_status not in self.Hero2.Status:
                                self.Hero2.Status.append(give_status)
                                msg.append("**" +self.Hero1.HeroName + '** has confused **{}**!'.format(self.Hero2.HeroName))
                            elif give_status not in self.Hero1.Status:
                                self.Hero1.Status.append(give_status)
                                msg.append("**" +self.Hero2.HeroName + '** has confused **{}**!'.format(self.Hero1.HeroName))
                        print('Confusion success!')
                if status[1:3] == 'PO':
                    print('Attempting poison..')
                    chance = int(status[3:])
                    r = randint(1,100)
                    if r <= chance:
                        give_status = 'POISONED'
                        if status[0] == 'S':
                            if heronum == 1 and give_status not in self.Hero1.Status:
                                self.Hero1.Status.append(give_status)
                                msg.append("**" +self.Hero1.HeroName + '** has poisoned themself!')
                            elif give_status not in self.Hero2.Status:
                                self.Hero2.Status.append(give_status)
                                msg.append("**" +self.Hero2.HeroName + '** has poisoned themself!')
                                
                        else:
                            if heronum == 1 and give_status not in self.Hero2.Status:
                                self.Hero2.Status.append(give_status)
                                msg.append("**" +self.Hero1.HeroName + '** has poisoned **{}**!'.format(self.Hero2.HeroName))
                            elif give_status not in self.Hero1.Status:
                                self.Hero1.Status.append(give_status)
                                msg.append("**" +self.Hero2.HeroName + '** has poisoned **{}**!'.format(self.Hero1.HeroName))
                        print('Poison success!')
                if status[1:3] == 'RE':
                    print('Recoil damage!')
                    damage = int(status[3:])
                    if status[0] == 'S':
                        if heronum == 1:
                            self.Hero1.HP = self.Hero1.HP - damage
                            msg.append("**" +self.Hero1.HeroName + '** has takend **{}** recoil damage!'.format(damage))
                        else:
                            self.Hero2.HP = self.Hero2.HP - damage
                            msg.append("**" +self.Hero2.HeroName + '** has takend **{}** recoil damage!'.format(damage))
                                

                '''
                if status[1:3] == 'CF':
                    chance = int(status[3:])
                if status[1:3] == 'PO':
                    chance = int(status[3:])
                if status[1:3] == 'NB':
                    chance = int(status[3:])
                '''
                continue



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

        Hero_Number = self.HeroTurn
        Attack_Name = Attack[0]
        Attack_Type = Attack[1]
        Attack_Desc = Attack[2]
        Attack_A_Type = Attack[3]
        Attack_Power = Attack[4]
        Attack_Status1 = Attack[5]
        Attack_Status2 = Attack[6]
        Attack_Status3 = Attack[7]
        Attack_Status4 = Attack[8]
        Attack_Status5 = Attack[9]

        msg = []

        print('Hero Type: ' + self.Turn[0].Type)
        print('Used Move Power: ' + str(Attack_Power))
        print('Used Move Type: ' + str(Attack_Type))
        if Attack_Type == self.Turn[0].Type:
                Attack_Power = Attack_Power * 1.5

        print('Attack Power after same type calc:' + str(Attack_Power))
        
        #TODO: If move is super effective against enemy
        #TODO: Critical chance.

        
        ContinueTurn = True

        for status in self.Turn[0].Status:
            if status == 'PARALYZED':
                r = randint(1,100)
                if r <=50:
                    msg.append( self.Turn[0].HeroName + " is paralyzed and cannot attack!")
                    ContinueTurn = False
            if status == 'CONFUSED':
                r = randint(1,100)
                if r <=33:
                    msg.append( self.Turn[0].HeroName + " hits themselves in confusion!")
                    self.Turn[0].HP = self.Turn[0].HP - 3
                    ContinueTurn = False
            if status == 'BURNED':
                Attack_Power = Attack_Power * .5
            if status == 'POISONED':
                self.Turn[0].HP = self.Turn[0].HP - 5
                msg.append(self.Turn[0].HeroName + " loses 5HP from poison!")
                if self.Turn[0].HP <=0:
                    self.Turn[0].HP = 1
                    msg.append(self.Turn[0].HeroName + ' survived with 1HP!')


        if ContinueTurn:



            if Attack_Power == 0:
                Attack_Power = 0
            else:
                Attack_Power = Attack_Power + self.Turn[0].ATK
            #TODO: Status effects of the move
            if self.HeroTurn==1:
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


            """Poor way to check statuses, fix this later."""
            input = [Hero_Number,Attack_Status1,Attack_Status2,msg]
            msg = self.execute_status(input) 
            input = [Hero_Number,Attack_Status3,Attack_Status4,msg]
            msg = self.execute_status(input)
            input = [Hero_Number,Attack_Status5,'NA',msg]
            msg = self.execute_status(input)

        else:
            self.Turn.pop(0)

        if self.Hero1.HP <= 0 and self.Hero2.HP <= 0:
            msg.append("Cut the credits, it's a draw! (Draws force close for now, sorry! :3)")
            return msg
        if self.Hero1.HP <= 0:
            msg.append("**{}** faints.".format(self.Hero1.HeroName))
            gameover = self.check_hp(1)
            if gameover:
                msg.append('**{}** wins!'.format(self.Hero2.HeroName))
                self.Turn = None
            else:
                msg.append('**{}**, please select a new hero.'.format(self.Player1.Owner))
                print('This is heroswap after hero1 faints: ' +str(self.HeroSwap))
            return msg
        elif self.Hero2.HP <= 0:
            msg.append("**{}** faints. **{}** wins!".format(self.Hero2.HeroName,self.Hero1.HeroName))
            gameover = self.check_hp(2)
            if gameover:
                msg.append('**{}** wins!'.format(self.Hero1.HeroName))
                self.Turn = None
            else:
                msg.append('**{}**, please select a new hero.'.format(self.Player2.Owner))
                print('This is heroswap after hero2 faints: '+str(self.HeroSwap))
            return msg
        


        if not self.Turn:
            self.set_Turn()
            if self.HeroTurn == 1:
                msg.append("It is now **{}({})**'s turn!".format(self.Hero1.HeroName,self.Player1.Owner))
                msg.append("**" + self.Hero1.HeroName + " HP:** " + str(self.Hero1.HP) + "   **" +self.Hero2.HeroName + " HP:** " + str(self.Hero2.HP))
            elif self.HeroTurn==2:
                msg.append("It is now **{}({})**'s turn!".format(self.Hero2.HeroName,self.Player2.Owner))
                msg.append("**" + self.Hero1.HeroName + " HP:** " + str(self.Hero1.HP) + "   **" +self.Hero2.HeroName + " HP:** " + str(self.Hero2.HP))

        else:
            if self.HeroTurn == 1:
                self.HeroTurn = 2
                msg.append("It is now **{}({})**'s turn!".format(self.Hero2.HeroName,self.Player2.Owner))
                msg.append("**" + self.Hero1.HeroName + " HP:** " + str(self.Hero1.HP) + "   **" +self.Hero2.HeroName + " HP:** " + str(self.Hero2.HP))
            elif self.HeroTurn==2:
                self.HeroTurn = 1
                msg.append("It is now **{}({})**'s turn!".format(self.Hero1.HeroName,self.Player1.Owner))
                msg.append("**" + self.Hero1.HeroName + " HP:** " + str(self.Hero1.HP) + "   **" +self.Hero2.HeroName + " HP:** " + str(self.Hero2.HP))
            

        
        return msg



    def set_Turn(self):
        if(self.Hero1.SPD > self.Hero2.SPD):
            self.Turn = [self.Hero1,self.Hero2]
            self.HeroTurn = 1
        elif self.Hero1:
            self.Turn = [self.Hero2,self.Hero1]
            self.HeroTurn = 2

    

    def check_hp(self,player):
        if player == 1:
            print(self.Player1.Hero1.HP )
            print(self.Player1.Hero2.HP )
            print(self.Player1.Hero3.HP )
            print(self.Player1.Hero4.HP )
            if self.Player1.Hero1.HP <=0 and self.Player1.Hero2.HP <=0 and self.Player1.Hero3.HP <=0 and self.Player1.Hero4.HP <=0:
                return True
            else:
                self.HeroSwap = 1
                print('Player 1 must swap now.')
                return False

        if player == 2:
            print(self.Player2.Hero1.HP )
            print(self.Player2.Hero2.HP )
            print(self.Player2.Hero3.HP )
            print(self.Player2.Hero4.HP )
            if self.Player2.Hero1.HP <=0 and self.Player2.Hero2.HP <=0 and self.Player2.Hero3.HP <=0 and self.Player2.Hero4.HP <=0:
                return True
            else:
                self.HeroSwap = 2
                print('Player 2 must swap now.')
                return False

    def check_continue(self,player):
        if player == 1:
            if self.Player1.Hero1.HP <=0 and self.Player1.Hero2.HP <=0 and self.Player1.Hero3.HP <=0 and self.Player1.Hero4.HP <=0:
                return True
            else:
                return False

        if player == 2:
            if self.Player2.Hero1.HP <=0 and self.Player2.Hero2.HP <=0 and self.Player2.Hero3.HP <=0 and self.Player2.Hero4.HP <=0:
                return True
            else:
                return False







class GachaBattle(commands.Cog):
    __slots__ = ('bot','battles',)
    def __init__(self,bot):
        self.bot = bot
        self.battles = {}

    def create(self,serverid,player1,player2):
        self.battles[serverid] = Battle(player1,player2)

    @commands.command(name='gachateam',aliases =['gteam','gt','team'])
    async def team(self,ctx):
        channelid = ctx.message.channel.id
        serverid = ctx.message.guild.id
        if not gachadatabase.get_gacha_channel([serverid,channelid]):
            return await ctx.send("This channel was not set for Gacha Commands to be used.")
        authorid = ctx.message.author.id
        serverid = ctx.message.guild.id
        author = ctx.message.author

        Author_Primaries = gachadatabase.get_primary_hero_ID([serverid,authorid])
        if not Author_Primaries:
            return await ctx.send("You do not have any primaries set!")
        Author_Primaries.append(author.name + "#" + author.discriminator)
        Author_Primaries.append(serverid)
        Author_Primaries.append(1)
        Player = Owner(Author_Primaries)
        log = Player.print_heros()
        await ctx.send(log,delete_after=20)

        




    @commands.command(name='battleswap')
    async def battleswap(self,ctx,move:int):
        battle = self.battles.get(ctx.message.guild.id)
        serverid= ctx.message.guild.id
        channelid = ctx.message.channel.id
        if not gachadatabase.get_gacha_channel([serverid,channelid]):
            return await ctx.send("This channel was not set for Gacha Commands to be used.")
        if not battle:
            return await ctx.send("There isn't a battle currently!")
        if not battle.can_play(ctx.message.author):
            return await ctx.send("You cannot play right now!")
        
        if battle.HeroSwap == 1:
            if move==1 and battle.Player1.Hero1.HP > 0 and battle.Hero1 != battle.Player1.Hero1:
                    battle.Hero1 = battle.Player1.Hero1
                    battle.set_Turn()
            elif move==2 and battle.Player1.Hero2.HP > 0 and battle.Hero1 != battle.Player1.Hero2:
                    battle.Hero1 = battle.Player1.Hero2
                    battle.set_Turn()
                    
            elif move==3 and battle.Player1.Hero3.HP > 0 and battle.Hero1 != battle.Player1.Hero3:
                    battle.Hero1 = battle.Player1.Hero3
                    battle.set_Turn()
            elif move==4 and battle.Player1.Hero4.HP > 0 and battle.Hero1 != battle.Player1.Hero4:
                    battle.Hero1 = battle.Player1.Hero4
                    battle.set_Turn()
            else:
                return await ctx.send("You cannot use this hero! You're either already own it, or they have no HP!")

            battle.HeroSwap=0
            log = print_turn(battle)
            return await ctx.send(log) 




        if battle.HeroSwap == 2:
            if move==1 and battle.Player2.Hero1.HP > 0 and battle.Hero2 != battle.Player2.Hero1:
                    battle.Hero2 = battle.Player2.Hero1
                    battle.set_Turn()
            elif move==2 and battle.Player2.Hero2.HP > 0 and battle.Hero2 != battle.Player2.Hero2:
                    battle.Hero2 = battle.Player2.Hero2
                    battle.set_Turn()
            elif move==3 and battle.Player2.Hero3.HP > 0 and battle.Hero2 != battle.Player2.Hero3:
                    battle.Hero2 = battle.Player2.Hero3
                    battle.set_Turn()
            elif move==4 and battle.Player2.Hero4.HP > 0 and battle.Hero2 != battle.Player2.Hero4:
                    battle.Hero2 = battle.Player2.Hero4
                    battle.set_Turn()
            else:
                return await ctx.send("You cannot use this hero! You're either already own it, or they have no HP!")

            battle.HeroSwap=0

            log = print_turn(battle)
            return await ctx.send(log) 
            



        if battle.HeroTurn == 1:
            if move==1 and battle.Player1.Hero1.HP > 0 and battle.Hero1 != battle.Player1.Hero1:
                    battle.Hero1 = battle.Player1.Hero1
                    if len(battle.Turn)==2:
                        battle.Turn.pop()
                        battle.HeroTurn = 2
                    else:
                        battle.set_Turn()
            elif move==2 and battle.Player1.Hero2.HP > 0 and battle.Hero1 != battle.Player1.Hero2:
                    battle.Hero1 = battle.Player1.Hero2
                    if len(battle.Turn)==2:
                        battle.Turn.pop()
                        battle.HeroTurn = 2
                    else:
                        battle.set_Turn()
            elif move==3 and battle.Player1.Hero3.HP > 0 and battle.Hero1 != battle.Player1.Hero3:
                    battle.Hero1 = battle.Player1.Hero3
                    if len(battle.Turn)==2:
                        battle.Turn.pop()
                        battle.HeroTurn = 2
                    else:
                        battle.set_Turn()
            elif move==4 and battle.Player1.Hero4.HP > 0 and battle.Hero1 != battle.Player1.Hero4:
                    battle.Hero1 = battle.Player1.Hero4
                    if len(battle.Turn)==2:
                        battle.Turn.pop()
                        battle.HeroTurn = 2
                    else:
                        battle.set_Turn()
            else:
                return await ctx.send("You cannot use this hero! You're either already own it, or they have no HP!")
            
            battle.HeroSwap=0
            log = print_turn(battle)
            return await ctx.send(log) 




        if battle.HeroTurn == 2:
            if move==1 and battle.Player2.Hero1.HP > 0 and battle.Hero2 != battle.Player2.Hero1:
                    battle.Hero2 = battle.Player2.Hero1
                    if len(battle.Turn)==2:
                        battle.Turn.pop()
                        battle.HeroTurn = 1
                    else:
                        battle.set_Turn()
            elif move==2 and battle.Player2.Hero2.HP > 0 and battle.Hero2 != battle.Player2.Hero2:
                    battle.Hero2 = battle.Player2.Hero2
                    if len(battle.Turn)==2:
                        battle.Turn.pop()
                        battle.HeroTurn = 1
                    else:
                        battle.set_Turn()
            elif move==3 and battle.Player2.Hero3.HP > 0 and battle.Hero2 != battle.Player2.Hero3:
                    battle.Hero2 = battle.Player2.Hero3
                    if len(battle.Turn)==2:
                        battle.Turn.pop()
                        battle.HeroTurn = 1
                    else:
                        battle.set_Turn()
            elif move==4 and battle.Player2.Hero4.HP > 0 and battle.Hero2 != battle.Player2.Hero4:
                    battle.Hero2 = battle.Player2.Hero4
                    if len(battle.Turn)==2:
                        battle.Turn.pop()
                        battle.HeroTurn = 1
                    else:
                        battle.set_Turn()
            else:
                return await ctx.send("You cannot use this hero! You're either already own it, or they have no HP!")
            battle.HeroSwap=0


            log = print_turn(battle)
            return await ctx.send(log)         

    @commands.command(name='battlemove')
    async def battlemove(self,ctx,move:int):
        battle = self.battles.get(ctx.message.guild.id)
        serverid = ctx.message.guild.id
        channelid = ctx.message.channel.id

        if not gachadatabase.get_gacha_channel([serverid,channelid]):
            return await ctx.send("This channel was not set for Gacha Commands to be used.")
        if not battle:
            return await ctx.send("There isn't a battle currently!")
        if not battle.can_play(ctx.message.author):
            return await ctx.send("You cannot play right now!")
        

        if battle.HeroSwap != 0:
            return await ctx.send("Hold up! Someone needs to swap their Hero out for another.")



        if move!= 0 and move!= 1 and move!= 2 and move!= 3 and move!= 4:
            return ctx.send("You didn't select a move! Try again with a move from 1-4, or 0 to forfeit.")
        
        if move==0:
            if(battle.HeroTurn==1):
                self.battles.pop(ctx.message.guild.id)
                return await ctx.send("**{}** has forfeited. **{}** has won!".format(battle.Hero1.Owner,battle.Hero2.Owner))
            else:
                self.battles.pop(ctx.message.guild.id)
                return await ctx.send("**{}** has forfeited. **{}** has won!".format(battle.Hero2.Owner,battle.Hero1.Owner))
        
        msg = battle.execute_move(move)
        log = ""
        
        for message in msg:
            log = log + message + " \n"

        await ctx.send(log)

        if battle.check_continue(1) == True or battle.check_continue(2)==True:
            self.battles.pop(ctx.message.guild.id)
        
    @commands.command(name="battlestats")
    async def battle_stats(self,ctx):
        authorid = ctx.message.author.id
        serverid = ctx.message.guild.id
        channelid = ctx.message.channel.id
        battle =  self.battles.get(serverid,None)
        if not battle:
            return await ctx.send("There's no battle currently happening!")
        if not gachadatabase.get_gacha_channel([serverid,channelid]):
            return await ctx.send("This channel was not set for Gacha Commands to be used.")
        
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
        channelid = ctx.message.channel.id
        
        battle =  self.battles.get(serverid,None)
        if not battle:
            return await ctx.send("There's no battle currently happening!")
        if not gachadatabase.get_gacha_channel([serverid,channelid]):
            return await ctx.send("This channel was not set for Gacha Commands to be used.")
        
        Hero1 = battle.Hero1
        Hero2 = battle.Hero2

        Hero1_Info = "__**" + Hero1.HeroName + "**__\n"  
        Hero1_Info= Hero1_Info + "**" + Hero1.Move1[0]+ "** -  \t**Type:** "  + Hero1.Move1[1] +  "   **Attack Type:** " + Hero1.Move1[3] + "  **Power:** " + str(Hero1.Move1[4]) 
        Hero1_Info= Hero1_Info + "  **S1:** " + Hero1.Move1[5] + "  **S2:** " +Hero1.Move1[6] + "   **S3:** " + Hero1.Move1[7] + "  **S4:** " +Hero1.Move1[8] + "  **S5:** " +Hero1.Move1[9] + " \n" 
        Hero1_Info= Hero1_Info + "**" + Hero1.Move2[0]+ "** -   \t**Type:** " + Hero1.Move2[1]  +   " **Attack Type:** " + Hero1.Move2[3] + "  **Power:** " + str(Hero1.Move2[4])  
        Hero1_Info= Hero1_Info + "  **S1:** " + Hero1.Move2[5] + "  **S2:** " +Hero1.Move2[6] + "   **S3:** " + Hero1.Move2[7] + "  **S4:** " +Hero1.Move2[8] +"  **S5:** " +Hero1.Move2[9] +" \n" 
        Hero1_Info= Hero1_Info + "**" + Hero1.Move3[0]+ "** -   \t**Type:** " + Hero1.Move3[1]  +   " **Attack Type:** " + Hero1.Move3[3] + "  **Power:** " + str(Hero1.Move3[4])  
        Hero1_Info= Hero1_Info + "  **S1:** " + Hero1.Move3[5] + "  **S2:** " +Hero1.Move3[6] + "   **S3:** " + Hero1.Move3[7] + "  **S4:** " +Hero1.Move3[8] +"  **S5:** " +Hero1.Move3[9] +" \n" 
        Hero1_Info= Hero1_Info + "**" + Hero1.Move4[0]+ "** -   \t**Type:** " + Hero1.Move4[1]  +  "  **Attack Type:** " + Hero1.Move4[3] + "  **Power:** " + str(Hero1.Move4[4])  
        Hero1_Info= Hero1_Info + "  **S1:** " + Hero1.Move4[5] + "  **S2:** " +Hero1.Move4[6] + "   **S3:** " + Hero1.Move4[7] + "  **S4:** " +Hero1.Move4[8] +"  **S5:** " +Hero1.Move4[9] +" \n"
        
        Hero2_Info = "\n__**" + Hero2.HeroName + "**__\n" 
        Hero2_Info= Hero2_Info + "**" + Hero2.Move1[0]+ "** -   \t**Type:** " + Hero2.Move1[1]  + "   **Attack Type:** " + Hero2.Move1[3] + "  **Power:** " + str(Hero2.Move1[4]) 
        Hero2_Info= Hero2_Info + "  **S1:** " + Hero2.Move1[5] + "  **S2:** " +Hero2.Move1[6] + "   **S3:** " + Hero2.Move1[7] + "  **S4:** " +Hero2.Move1[8] +"  **S5:** " +Hero2.Move1[9] +" \n" 
        Hero2_Info= Hero2_Info + "**" + Hero2.Move2[0]+ "** -   \t**Type:** " + Hero2.Move2[1]  + "   **Attack Type:** " + Hero2.Move2[3] + "  **Power:** " + str(Hero2.Move2[4])  
        Hero2_Info= Hero2_Info + "  **S1:** " + Hero2.Move2[5] + "  **S2:** " +Hero2.Move2[6] + "   **S3:** " + Hero2.Move2[7] + "  **S4:** " +Hero2.Move2[8] +"  **S5:** " +Hero2.Move2[9] +" \n" 
        Hero2_Info= Hero2_Info + "**" + Hero2.Move3[0]+ "** -   \t**Type:** " + Hero2.Move3[1]  + "   **Attack Type:** " + Hero2.Move3[3] + "  **Power:** " + str(Hero2.Move3[4])  
        Hero2_Info= Hero2_Info + "  **S1:** " + Hero2.Move3[5] + "  **S2:** " +Hero2.Move3[6] + "   **S3:** " + Hero2.Move3[7] + "  **S4:** " +Hero2.Move3[8] +"  **S5:** " +Hero2.Move3[9] +" \n" 
        Hero2_Info= Hero2_Info + "**" +Hero2.Move4[0]+ "** -   \t**Type:** " + Hero2.Move4[1]   + "   **Attack Type:** " + Hero2.Move4[3] + "  **Power:** " + str(Hero2.Move4[4]) 
        Hero2_Info= Hero2_Info + "  **S1:** " + Hero2.Move4[5] + "  **S2:** " +Hero2.Move4[6] + "   **S3:** " + Hero2.Move4[7] + "  **S4:** " +Hero2.Move4[8] +"  **S5:** " +Hero2.Move4[9] + " \n"

        Hero_Info = Hero1_Info + Hero2_Info

        await ctx.send(Hero_Info)
    
    @commands.command(name="battle")
    async def battle(self,ctx, member: discord.Member):
        
        authorid = ctx.message.author.id
        serverid = ctx.message.guild.id
        channelid = ctx.message.channel.id

        if not gachadatabase.get_gacha_channel([serverid,channelid]):
            return await ctx.send("This channel was not set for Gacha Commands to be used.")

        author = ctx.message.author
        current_battle = self.battles.get(serverid,None)

        Player1_Primaries = gachadatabase.get_primary_hero_ID([serverid,authorid])
        Player2_Primaries = gachadatabase.get_primary_hero_ID([serverid,member.id])

        print(Player1_Primaries)
        print(Player2_Primaries)

        if member == ctx.message.guild.me:
            return await ctx.send("Sorry, I don't have any heroes to use. :(")
        if member.id == authorid:
            return await ctx.send("You cannot battle yourself, IDIOT.")
        if current_battle:
            return await ctx.send("There is a battle in progress. Wait until it is done!")
        if not Player1_Primaries or not Player2_Primaries:
            return await ctx.send("One of the players does not have any primaries set!")


        Player1_Primaries.append(author.name + "#" + author.discriminator)
        Player1_Primaries.append(serverid)
        Player1_Primaries.append(1)
        Player1 = Owner(Player1_Primaries)

        Player2_Primaries.append(member.name + "#" + member.discriminator)
        Player2_Primaries.append(serverid)
        Player2_Primaries.append(2)
        Player2 = Owner(Player2_Primaries)
        

        self.create(ctx.message.guild.id,Player1,Player2)
        battle =  self.battles.get(serverid,None)
        msg= "A battle has just started between **{}** and **{}**! No other battles on this server can take place until this is over!".format(battle.Player1.Owner,battle.Player2.Owner)
        log = print_turn(battle)
        await ctx.send(msg)
        await ctx.send(log)
        

        
        

def print_turn(battle):
    msg = []
    if battle.HeroTurn == 1:
        msg.append("It is now **{}({})**'s turn!".format(battle.Hero1.HeroName,battle.Player1.Owner))
    else:
         msg.append("It is now **{}({})**'s turn!".format(battle.Hero2.HeroName,battle.Player2.Owner)) 
    log = ""
    for message in msg:
        log = log + message + " \n"
    return log




