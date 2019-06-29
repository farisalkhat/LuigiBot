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
    query = 'SELECT Name,HP,ATK,DEF,SDEF,SPD,Description FROM Heroes WHERE SERVERID = :SERVERID AND Rating =3'
    rs = con.execute(query,dict(SERVERID=SERVERID))
    results = []
    for user in rs:
        results.append(list(user[:]))
    return results
def get_fourstars(SERVERID):
    query = 'SELECT Name,HP,ATK,DEF,SDEF,SPD,Description FROM Heroes WHERE SERVERID = :SERVERID AND Rating =4'
    rs = con.execute(query,dict(SERVERID=SERVERID))
    results = []
    for user in rs:
        results.append(list(user[:]))
    return results
def get_fivestars(SERVERID):
    query = 'SELECT Name,HP,ATK,DEF,SDEF,SPD,Description FROM Heroes WHERE SERVERID = :SERVERID AND Rating =5'
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
    (SERVERID, MEMBERID,HERONAME,HP,ATK,DEF,SDEF,SPD,RARITY,ID) = input
    query = 'INSERT INTO Barracks VALUES(:SERVERID,:MEMBERID,:HERONAME,:HP,:ATK,:DEF,:SDEF,:SPD,0,:RARITY,:ID)'
    con.execute(query,dict(SERVERID=SERVERID,MEMBERID=MEMBERID,HERONAME=HERONAME,HP=HP,ATK=ATK,DEF=DEF,SDEF=SDEF,SPD=SPD,RARITY=RARITY,ID=ID))
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





def place_primary_hero(input):
    (SERVERID,MEMBERID,HERONAME) = input
    query = 'INSERT INTO Primary_Hero VALUES(:SERVERID,:MEMBERID,:HERONAME)'
    con.execute(query,dict(SERVERID=SERVERID,MEMBERID=MEMBERID,HERONAME=HERONAME))
    conn.commit()
def remove_primary_hero(input):
    (SERVERID,MEMBERID) = input
    query = 'DELETE FROM Primary_Hero WHERE SERVERID=:SERVERID AND MEMBERID=:MEMBERID'
    con.execute(query,dict(SERVERID=SERVERID,MEMBERID=MEMBERID))
    conn.commit()
def get_primary_hero_ID(input):
    (SERVERID,MEMBERID)= input
    query = 'SELECT HEROID FROM Primary_Hero WHERE SERVERID=:SERVERID AND MEMBERID=:MEMBERID'
    rs = con.execute(query,dict(SERVERID=SERVERID,MEMBERID=MEMBERID))
    results = []
    for result in rs:
        results = list(result[:])
    return results
def get_primary_hero(HEROID):
    query = '''SELECT Barracks.HERONAME, Barracks.HP,Barracks.ATK,Barracks.DEF,Barracks.SDEF,Barracks.SPD FROM Barracks,
    Primary_Hero WHERE Primary_Hero.HEROID = :HEROID AND Barracks.HEROID = :HEROID '''
    rs = con.execute(query,dict(HEROID=HEROID))
    results = []
    for result in rs:
        results = list(result[:])
    return results
def get_primary_moves(input):
    (HEROID,SERVERID)= input
    query = """SELECT 
    Moveset.MOVENAME, Moveset.TYPE,Moveset.DETAIL, Moveset.POWERTYPE, Moveset.POWER,Moveset.STATUS1,Moveset.STATUS2,Moveset.STATUS3,Moveset.STATUS4,Moveset.STATUS5
    FROM Moveset,Primary_Hero,Barracks
    WHERE Primary_Hero.HEROID = :HEROID AND
    Primary_Hero.SERVERID = :SERVERID AND
    Primary_Hero.HEROID = Barracks.HEROID AND 
    Moveset.SERVERID = Primary_Hero.SERVERID AND
    Moveset.HERONAME = Barracks.HERONAME"""
    rs = con.execute(query,dict(HEROID=HEROID,SERVERID=SERVERID))
    results = []
    for user in rs:
        results.append(list(user[:]))
    return results