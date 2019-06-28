class Hero:
        def __init__(self,hero):
            self.Owner = hero[]
            self.Turn = 0
            self.HeroName = hero[]
            self.Description = hero[]

            self.HP = hero[]
            self.ATK = hero[]
            self.DEF = hero[]
            self.SDEF = hero[]
            self.SPD =  hero[]

            self.Move1 = hero[]
            self.Move2 = hero[]
            self.Move3 = hero[]
            self.Move4 = hero[]

            self.Status = []




class Battle:
    def __init__(self,player1,player2):
        self.p1 = p1    #Player 1 ID
        self.p2 = p2    #Player 2 ID
        self.p1_hero = gachadatabase.get_primary_hero([serverid,p1]) #Player 1 Hero Stats and Type
        self.p2_hero = gachadatabase.get_primary_hero([serverid,p2]) #Player 2 Hero Stats and Type
        self.p1_moves = gachadatabase.get_primary_moves([self.guild.id,p1_hero[1]])
        self.p2_moves = gachadatabase.get_primary_moves([self.guild.id,p2_hero[1]])

        self.Hero1 = Hero(p1_hero,p1_moves)
        self.Hero2 = Hero(p2_hero,p2_moves)

        if(Hero1.SPD > Hero2.SPD):
            self.Hero1.Turn = 2
        else:
            self.Hero2.Turn = 1

        self.Turn = 0


    def dead_hero(self):
        if self.Hero1.HP <= 0:
            return 11
        if self.Hero2.HP <=0:
            return 22
        return 0

    def can_play(self,player):
        if player == self.Hero1.Owner:
            return True
        if player == self.Hero2.Owner:
            return True
        return False

    def reset_turn(self):
        if(Hero1.SPD > Hero2.SPD):
            self.Hero1.Turn = 2
        else:
            self.Hero2.Turn = 1

        self.Turn = 2


    def update(self,input):
        #input = [player,input]
        print('updated!')
    def check(self,player,input):
        switcher = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            'f': "May",
            }
        print switcher.get(argument, "Invalid month")









        update_input = []

        if player==self.Hero1.Owner and self.Hero1.Turn == self.Turn:
                case
                HeroType = Hero1.Type
                Move = Hero1.Move1

            else:
                print('DEAD')

        elif player==self.Hero2.Owner and self.Hero2.Turn == self.Turn:
            if input == '1' or input == '2' or input =='3' or input =='4' or input =='f':


            else:
                print('DEAD')
        else:
            print(DEAD)
