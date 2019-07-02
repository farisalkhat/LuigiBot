import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import sql
import itertools


conn = sqlite3.connect('db\gachaecon.db')  # You can create a new database by changing the name within the quotes
con = conn.cursor()

'''
These queries modify or pull info from the Heroes Table.
'''

def get_threestars(SERVERID):
    query = 'SELECT Name,HP,ATK,DEF,SDEF,SPD,Description,TYPE FROM Heroes WHERE SERVERID = :SERVERID AND Rating =3'
    rs = con.execute(query,dict(SERVERID=SERVERID))
    results = []
    for user in rs:
        results.append(list(user[:]))
    return results
def get_fourstars(SERVERID):
    query = 'SELECT Name,HP,ATK,DEF,SDEF,SPD,Description,TYPE FROM Heroes WHERE SERVERID = :SERVERID AND Rating =4'
    rs = con.execute(query,dict(SERVERID=SERVERID))
    results = []
    for user in rs:
        results.append(list(user[:]))
    return results
def get_fivestars(SERVERID):
    query = 'SELECT Name,HP,ATK,DEF,SDEF,SPD,Description,TYPE FROM Heroes WHERE SERVERID = :SERVERID AND Rating =5'
    rs = con.execute(query,dict(SERVERID=SERVERID))
    results = []
    for user in rs:
        results.append(list(user[:]))
    return results
def get_hero(input):
    (HERO_NAME,SERVERID) = input
    query = 'SELECT * FROM Heroes WHERE Name = :HERO_NAME AND SERVERID= :SERVERID'
    rs = con.execute(query,dict(HERO_NAME=HERO_NAME,SERVERID=SERVERID))
    results = []
    for user in rs:
        results = list(user[:])
    return results
def remove_hero(input):
    (SERVERID,HERONAME) = input
    query = 'DELETE FROM Heroes WHERE SERVERID = :SERVERID AND Name= :HERONAME'
    con.execute(query,dict(SERVERID=SERVERID,HERONAME=HERONAME))
    conn.commit()
def create_hero(input):
    (SERVERID,Name,Portrait,Description,Creator,Type,Rating,HP,ATK,DEF,SDEF,SPD) = input
    query = 'INSERT INTO Heroes VALUES(:SERVERID,:Name,:Portrait,:Description,:Creator,:Type,:Rating,:HP,:ATK,:DEF,:SDEF,:SPD)'
    con.execute(query,dict(SERVERID=SERVERID,Name=Name,Portrait=Portrait, Description=Description,Creator=Creator,Type=Type,Rating=Rating,HP=HP,ATK=ATK,DEF=DEF,SDEF=SDEF,SPD=SPD))
    conn.commit()


'''
These queries modify or pull info from the Barracks table.
'''

def add_hero(input):
    (SERVERID, MEMBERID,HERONAME,HP,ATK,DEF,SDEF,SPD,RARITY,ID,TYPE) = input
    query = 'INSERT INTO Barracks VALUES(:SERVERID,:MEMBERID,:HERONAME,:HP,:ATK,:DEF,:SDEF,:SPD,0,:RARITY,:ID,:TYPE)'
    con.execute(query,dict(SERVERID=SERVERID,MEMBERID=MEMBERID,HERONAME=HERONAME,HP=HP,ATK=ATK,DEF=DEF,SDEF=SDEF,SPD=SPD,RARITY=RARITY,ID=ID,TYPE=TYPE))
    conn.commit()
def get_heroes(input):
    (SERVER_ID,USERNAME) = input
    query = 'SELECT *  FROM Barracks WHERE SERVERID = :SERVER_ID AND MEMBERID= :USERNAME ORDER BY RARITY DESC, HERONAME ASC'
    rs = con.execute(query,dict(SERVER_ID=SERVER_ID,USERNAME=USERNAME))
    results = []
    for user in rs:
        results.append(list(user[:]))
    return results
def delete_barracks_hero(ID):
    query = 'DELETE FROM Barracks WHERE HEROID=:ID'
    con.execute(query,dict(ID=ID))
def get_barracks_hero(input):
    (SERVER_ID,USERNAME,ID) = input
    query = 'SELECT * FROM Barracks WHERE SERVERID = :SERVER_ID AND MEMBERID=:USERNAME AND HEROID=:ID'
    rs = con.execute(query,dict(SERVER_ID=SERVER_ID,USERNAME=USERNAME,ID=ID))
    results = []
    for result in rs:
        results = list(result[:])
    return results
def get_barracks_hero2(input):
    (SERVER_ID,HERO_NAME) = input
    query = 'SELECT * FROM Barracks WHERE SERVERID = :SERVER_ID AND HERONAME=:HERO_NAME'
    rs = con.execute(query,dict(SERVER_ID=SERVER_ID,HERO_NAME=HERO_NAME))
    results = []
    for result in rs:
        results = list(result[:])
    return results
def remove_barracks_hero(input):
    (SERVER_ID,HERO_NAME) = input
    query = 'DELETE FROM Barracks WHERE SERVERID = :SERVER_ID AND HERONAME= :HERO_NAME'
    con.execute(query,dict(SERVER_ID=SERVER_ID,HERO_NAME=HERO_NAME))
    conn.commit()





def place_primary_hero1(input):
    (SERVERID,MEMBERID,HEROID1) = input
    query = 'INSERT INTO Primary_Hero(SERVERID,MEMBERID,HEROID1) VALUES(:SERVERID,:MEMBERID,:HEROID1)'
    con.execute(query,dict(SERVERID=SERVERID,MEMBERID=MEMBERID,HEROID1=HEROID1))
    conn.commit()
def place_primary_hero2(input):
    (SERVERID,MEMBERID,HEROID1,HEROID2) = input
    query = 'INSERT INTO Primary_Hero(SERVERID,MEMBERID,HEROID1,HEROID2) VALUES(:SERVERID,:MEMBERID,:HEROID1,:HEROID2)'
    con.execute(query,dict(SERVERID=SERVERID,MEMBERID=MEMBERID,HEROID1=HEROID1,HEROID2=HEROID2))
    conn.commit()
def place_primary_hero3(input):
    (SERVERID,MEMBERID,HEROID1,HEROID2,HEROID3) = input
    query = 'INSERT INTO Primary_Hero(SERVERID,MEMBERID,HEROID1,HEROID2,HEROID3) VALUES(:SERVERID,:MEMBERID,:HEROID1,:HEROID2,:HEROID3)'
    con.execute(query,dict(SERVERID=SERVERID,MEMBERID=MEMBERID,HEROID1=HEROID1,HEROID2=HEROID2,HEROID3=HEROID3))
    conn.commit()
def place_primary_hero4(input):
    (SERVERID,MEMBERID,HEROID1,HEROID2,HEROID3,HEROID4) = input
    query = 'INSERT INTO Primary_Hero(SERVERID,MEMBERID,HEROID1,HEROID2,HEROID3,HEROID4) VALUES(:SERVERID,:MEMBERID,:HEROID1,HEROID2,HEROID3,HEROID4)'
    con.execute(query,dict(SERVERID=SERVERID,MEMBERID=MEMBERID,HEROID1=HEROID1,HEROID2=HEROID2,HEROID3=HEROID3,HEROID4=HEROID4))
    conn.commit()


def remove_primary_hero(input):
    (SERVERID,MEMBERID) = input
    query = 'DELETE FROM Primary_Hero WHERE SERVERID=:SERVERID AND MEMBERID=:MEMBERID'
    con.execute(query,dict(SERVERID=SERVERID,MEMBERID=MEMBERID))
    conn.commit()
def get_primary_hero_ID(input):
    (SERVERID,MEMBERID)= input
    query = 'SELECT HEROID1,HEROID2,HEROID3,HEROID4 FROM Primary_Hero WHERE SERVERID=:SERVERID AND MEMBERID=:MEMBERID'
    rs = con.execute(query,dict(SERVERID=SERVERID,MEMBERID=MEMBERID))
    results = []
    for result in rs:
        results = list(result[:])
    return results


def get_primary_moves1(input):
    (HEROID,SERVERID)= input
    query = """SELECT 
    Moveset.MOVENAME, Moveset.TYPE,Moveset.DETAIL, Moveset.POWERTYPE, Moveset.POWER,Moveset.STATUS1,Moveset.STATUS2,Moveset.STATUS3,Moveset.STATUS4,Moveset.STATUS5
    FROM Moveset,Primary_Hero,Barracks
    WHERE Primary_Hero.HEROID1 = :HEROID AND
    Primary_Hero.SERVERID = :SERVERID AND
    Primary_Hero.HEROID1 = Barracks.HEROID AND 
    Moveset.SERVERID = Primary_Hero.SERVERID AND
    Moveset.HERONAME = Barracks.HERONAME"""
    rs = con.execute(query,dict(HEROID=HEROID,SERVERID=SERVERID))
    results = []
    for user in rs:
        results.append(list(user[:]))
    return results
def get_primary_moves2(input):
    (HEROID,SERVERID)= input
    query = """SELECT 
    Moveset.MOVENAME, Moveset.TYPE,Moveset.DETAIL, Moveset.POWERTYPE, Moveset.POWER,Moveset.STATUS1,Moveset.STATUS2,Moveset.STATUS3,Moveset.STATUS4,Moveset.STATUS5
    FROM Moveset,Primary_Hero,Barracks
    WHERE Primary_Hero.HEROID2 = :HEROID AND
    Primary_Hero.SERVERID = :SERVERID AND
    Primary_Hero.HEROID2 = Barracks.HEROID AND 
    Moveset.SERVERID = Primary_Hero.SERVERID AND
    Moveset.HERONAME = Barracks.HERONAME"""
    rs = con.execute(query,dict(HEROID=HEROID,SERVERID=SERVERID))
    results = []
    for user in rs:
        results.append(list(user[:]))
    return results
def get_primary_moves3(input):
    (HEROID,SERVERID)= input
    query = """SELECT 
    Moveset.MOVENAME, Moveset.TYPE,Moveset.DETAIL, Moveset.POWERTYPE, Moveset.POWER,Moveset.STATUS1,Moveset.STATUS2,Moveset.STATUS3,Moveset.STATUS4,Moveset.STATUS5
    FROM Moveset,Primary_Hero,Barracks
    WHERE Primary_Hero.HEROID3 = :HEROID AND
    Primary_Hero.SERVERID = :SERVERID AND
    Primary_Hero.HEROID3 = Barracks.HEROID AND 
    Moveset.SERVERID = Primary_Hero.SERVERID AND
    Moveset.HERONAME = Barracks.HERONAME"""
    rs = con.execute(query,dict(HEROID=HEROID,SERVERID=SERVERID))
    results = []
    for user in rs:
        results.append(list(user[:]))
    return results
def get_primary_moves4(input):
    (HEROID,SERVERID)= input
    query = """SELECT 
    Moveset.MOVENAME, Moveset.TYPE,Moveset.DETAIL, Moveset.POWERTYPE, Moveset.POWER,Moveset.STATUS1,Moveset.STATUS2,Moveset.STATUS3,Moveset.STATUS4,Moveset.STATUS5
    FROM Moveset,Primary_Hero,Barracks
    WHERE Primary_Hero.HEROID4 = :HEROID AND
    Primary_Hero.SERVERID = :SERVERID AND
    Primary_Hero.HEROID4 = Barracks.HEROID AND 
    Moveset.SERVERID = Primary_Hero.SERVERID AND
    Moveset.HERONAME = Barracks.HERONAME"""
    rs = con.execute(query,dict(HEROID=HEROID,SERVERID=SERVERID))
    results = []
    for user in rs:
        results.append(list(user[:]))
    return results
def get_primary_hero1(HEROID):
    query = '''SELECT Barracks.HERONAME, Barracks.HP,Barracks.ATK,Barracks.DEF,Barracks.SDEF,Barracks.SPD,Barracks.TYPE FROM Barracks,
    Primary_Hero WHERE Primary_Hero.HEROID1 = :HEROID AND Barracks.HEROID = :HEROID '''
    rs = con.execute(query,dict(HEROID=HEROID))
    results = []
    for result in rs:
        results = list(result[:])
    return results
def get_primary_hero2(HEROID):
    query = '''SELECT Barracks.HERONAME, Barracks.HP,Barracks.ATK,Barracks.DEF,Barracks.SDEF,Barracks.SPD,Barracks.TYPE FROM Barracks,
    Primary_Hero WHERE Primary_Hero.HEROID2 = :HEROID AND Barracks.HEROID = :HEROID '''
    rs = con.execute(query,dict(HEROID=HEROID))
    results = []
    for result in rs:
        results = list(result[:])
    return results
def get_primary_hero3(HEROID):
    query = '''SELECT Barracks.HERONAME, Barracks.HP,Barracks.ATK,Barracks.DEF,Barracks.SDEF,Barracks.SPD,Barracks.TYPE FROM Barracks,
    Primary_Hero WHERE Primary_Hero.HEROID3 = :HEROID AND Barracks.HEROID = :HEROID '''
    rs = con.execute(query,dict(HEROID=HEROID))
    results = []
    for result in rs:
        results = list(result[:])
    return results
def get_primary_hero4(HEROID):
    query = '''SELECT Barracks.HERONAME, Barracks.HP,Barracks.ATK,Barracks.DEF,Barracks.SDEF,Barracks.SPD,Barracks.TYPE FROM Barracks,
    Primary_Hero WHERE Primary_Hero.HEROID4 = :HEROID AND Barracks.HEROID = :HEROID '''
    rs = con.execute(query,dict(HEROID=HEROID))
    results = []
    for result in rs:
        results = list(result[:])
    return results





def set_gacha_channel(input):
    (SERVERID,CHANNELID) = input
    query = 'INSERT INTO Gacha_Channels VALUES(:SERVERID,:CHANNELID)'
    con.execute(query,dict(SERVERID=SERVERID,CHANNELID=CHANNELID))
    conn.commit()

def get_gacha_channel(input):
    (SERVERID,CHANNELID) = input
    query = 'SELECT * FROM Gacha_Channels WHERE SERVERID=:SERVERID AND CHANNELID=:CHANNELID'
    rs = con.execute(query,dict(SERVERID=SERVERID,CHANNELID=CHANNELID))
    results = []
    for result in rs:
        results = list(result[:])
    if results:
        return True
    return False

def add_gacha_move(input):
    if len(input) == 6:
    #Serverid;Heroname;Movename;Type;PT;Power;
        (SERVERID,HERONAME,MOVENAME,TYPE,PT,POWER) = input
        query = "INSERT INTO Moveset VALUES(:SERVERID,:HERONAME,:MOVENAME,:TYPE,'No detail',:PT,:POWER,'NA','NA','NA','NA','NA')"
        rs = con.execute(query,dict(SERVERID=SERVERID,HERONAME=HERONAME,MOVENAME=MOVENAME,TYPE=TYPE,PT=PT,POWER=POWER))
        conn.commit
        return
    if len(input) == 7:
    #Serverid;Heroname;Movename;Type;PT;Power,Status1;
        (SERVERID,HERONAME,MOVENAME,TYPE,PT,POWER,STATUS1) = input
        query = "INSERT INTO Moveset VALUES(:SERVERID,:HERONAME,:MOVENAME,:TYPE,'No detail',:PT,:POWER,:STATUS1,'NA','NA','NA','NA')"
        rs = con.execute(query,dict(SERVERID=SERVERID,HERONAME=HERONAME,MOVENAME=MOVENAME,TYPE=TYPE,PT=PT,POWER=POWER,STATUS1=STATUS1))
        conn.commit
        return
    if len(input) == 8:
    #Serverid;Heroname;Movename;Type;PT;Power;Status1;Status2
        (SERVERID,HERONAME,MOVENAME,TYPE,PT,POWER,STATUS1,STATUS2) = input
        query = "INSERT INTO Moveset VALUES(:SERVERID,:HERONAME,:MOVENAME,:TYPE,'No detail',:PT,:POWER,:STATUS1,:STATUS2,'NA','NA','NA')"
        rs = con.execute(query,dict(SERVERID=SERVERID,HERONAME=HERONAME,MOVENAME=MOVENAME,TYPE=TYPE,PT=PT,POWER=POWER,STATUS1=STATUS1,STATUS2=STATUS2))
        conn.commit
        return
    if len(input) == 9:
    #Serverid;Heroname;Movename;Type;PT;Power;
        (SERVERID,HERONAME,MOVENAME,TYPE,PT,POWER,STATUS1,STATUS2,STATUS3) = input
        query = "INSERT INTO Moveset VALUES(:SERVERID,:HERONAME,:MOVENAME,:TYPE,'No detail',:PT,:POWER,:STATUS1,:STATUS2,:STATUS3,'NA','NA')"
        rs = con.execute(query,dict(SERVERID=SERVERID,HERONAME=HERONAME,MOVENAME=MOVENAME,TYPE=TYPE,PT=PT,POWER=POWER,STATUS1=STATUS1,STATUS2=STATUS2,STATUS3=STATUS3))
        conn.commit
        return
    if len(input) == 10:
    #Serverid;Heroname;Movename;Type;PT;Power;
        (SERVERID,HERONAME,MOVENAME,TYPE,PT,POWER,STATUS1,STATUS2,STATUS3,STATUS4) = input
        query = "INSERT INTO Moveset VALUES(:SERVERID,:HERONAME,:MOVENAME,:TYPE,'No detail',:PT,:POWER,:STATUS1,:STATUS2,:STATUS3,:STATUS4,'NA')"
        rs = con.execute(query,dict(SERVERID=SERVERID,HERONAME=HERONAME,MOVENAME=MOVENAME,TYPE=TYPE,PT=PT,POWER=POWER,STATUS1=STATUS1,STATUS2=STATUS2,STATUS3=STATUS3,STATUS4=STATUS4))
        conn.commit
        return
    if len(input) == 11:
    #Serverid;Heroname;Movename;Type;PT;Power;
        (SERVERID,HERONAME,MOVENAME,TYPE,PT,POWER,STATUS1,STATUS2,STATUS3,STATUS4,STATUS5) = input
        query = "INSERT INTO Moveset VALUES(:SERVERID,:HERONAME,:MOVENAME,:TYPE,'No detail',:PT,:POWER,:STATUS1,:STATUS2,:STATUS3,:STATUS4,:STATUS5)"
        rs = con.execute(query,dict(SERVERID=SERVERID,HERONAME=HERONAME,MOVENAME=MOVENAME,TYPE=TYPE,PT=PT,POWER=POWER,STATUS1=STATUS1,STATUS2=STATUS2,STATUS3=STATUS3,STATUS4=STATUS4,STATUS5=STATUS5))
        conn.commit
        return
    
        
   