import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import sql
import itertools


conn = sqlite3.connect('db\gachaecon.db')  # You can create a new database by changing the name within the quotes
con = conn.cursor()



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

def get_economy(SERVERID):
    query = 'SELECT * FROM Economy_Enabled WHERE SERVERID = :SERVERID'
    rs = con.execute(query,dict(SERVERID=SERVERID))
    results = []
    for result in rs:
        results = list(result[:])
    return results

def remove_hero(input):
    (SERVERID,HERONAME) = input
    query = 'DELETE FROM Heroes WHERE SERVERID = :SERVERID AND Name= :HERONAME'
    con.execute(query,dict(SERVERID=SERVERID,HERONAME=HERONAME))
    conn.commit()

def remove_barracks_hero(input):
    (SERVER_ID,HERO_NAME) = input
    query = 'DELETE FROM Barracks WHERE SERVER_ID = :SERVER_ID AND HERO_NAME= :HERO_NAME'
    con.execute(query,dict(SERVER_ID=SERVER_ID,HERO_NAME=HERO_NAME))
    conn.commit()




def get_balance(input):
    (SERVERID,MEMBERID) = input
    query = 'SELECT * FROM Economy WHERE SERVER_ID = :SERVERID AND USERNAME = :MEMBERID'
    rs = con.execute(query,dict(SERVERID=SERVERID,MEMBERID=MEMBERID))
    results = []
    for result in rs:
        results = list(result[:])
    return results

def set_balance(input):
    (SERVERID,MEMBERID,BALANCE) = input
    query = 'UPDATE Economy  SET LUIGICOIN = :BALANCE WHERE SERVER_ID = :SERVERID AND USERNAME = :MEMBERID'
    con.execute(query,dict(SERVERID=SERVERID,MEMBERID=MEMBERID,BALANCE=BALANCE))
    conn.commit()



def add_hero(input):
    (SERVERID, MEMBERID,HERONAME,HP,ATK,DEF,SDEF,SPD,RARITY,ID) = input
    query = 'INSERT INTO Barracks VALUES(:SERVERID,:MEMBERID,:HERONAME,:HP,:ATK,:DEF,:SDEF,:SPD,0,:RARITY,:ID)'
    con.execute(query,dict(SERVERID=SERVERID,MEMBERID=MEMBERID,HERONAME=HERONAME,HP=HP,ATK=ATK,DEF=DEF,SDEF=SDEF,SPD=SPD,RARITY=RARITY,ID=ID))
    conn.commit()

def delete_barracks_hero(ID):
    query = 'DELETE FROM Barracks WHERE ID=:ID'
    con.execute(query,dict(ID=ID))

def get_barracks_hero(input):
    (SERVER_ID,USERNAME,ID) = input
    query = 'SELECT * FROM Barracks WHERE SERVER_ID = :SERVER_ID AND USERNAME=:USERNAME AND ID=:ID'
    rs = con.execute(query,dict(SERVER_ID=SERVER_ID,USERNAME=USERNAME,ID=ID))
    results = []
    for result in rs:
        results = list(result[:])
    return results

def get_barracks_hero2(input):
    (SERVER_ID,HERO_NAME) = input
    query = 'SELECT * FROM Barracks WHERE SERVER_ID = :SERVER_ID AND HERO_NAME=:HERO_NAME'
    rs = con.execute(query,dict(SERVER_ID=SERVER_ID,HERO_NAME=HERO_NAME))
    results = []
    for result in rs:
        results = list(result[:])
    return results





'''
UPDATE table
SET column_1 = new_value_1,
    column_2 = new_value_2
WHERE
    search_condition
'''


def add_econ_member(input):
    (SERVERID,MEMBERID,AMOUNT) = input
    query = 'INSERT INTO Economy VALUES(:SERVERID, :MEMBERID, :AMOUNT)'
    con.execute(query,dict(SERVERID=SERVERID,MEMBERID=MEMBERID,AMOUNT=AMOUNT))
    conn.commit()

def create_hero(input):
    (SERVERID,Name,Portrait,Description,Creator,Type,Rating,HP,ATK,DEF,SDEF,SPD) = input
    query = 'INSERT INTO Heroes VALUES(:SERVERID,:Name,:Portrait,:Description,:Creator,:Type,:Rating,:HP,:ATK,:DEF,:SDEF,:SPD)'
    con.execute(query,dict(SERVERID=SERVERID,Name=Name,Portrait=Portrait, Description=Description,Creator=Creator,Type=Type,Rating=Rating,HP=HP,ATK=ATK,DEF=DEF,SDEF=SDEF,SPD=SPD))
    conn.commit()



def create_economy(input):
    (SERVERID,ENABLED) = input
    query = 'INSERT INTO Economy_Enabled VALUES(:SERVERID, :ENABLED)'
    con.execute(query,dict(SERVERID=SERVERID,ENABLED=ENABLED))
    conn.commit()





def get_heroes(input):
    (SERVER_ID,USERNAME) = input
    query = 'SELECT *  FROM Barracks WHERE SERVER_ID = :SERVER_ID AND USERNAME= :USERNAME ORDER BY RARITY DESC, HERO_NAME ASC'
    rs = con.execute(query,dict(SERVER_ID=SERVER_ID,USERNAME=USERNAME))
    results = []
    for user in rs:
        results.append(list(user[:]))
    return results




