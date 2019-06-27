import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import sql
import itertools


conn = sqlite3.connect('db\gachaecon.db')  # You can create a new database by changing the name within the quotes
con = conn.cursor()





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

def get_balance(input):
    (SERVERID,MEMBERID) = input
    query = 'SELECT * FROM Economy WHERE SERVER_ID = :SERVERID AND USERNAME = :MEMBERID'
    rs = con.execute(query,dict(SERVERID=SERVERID,MEMBERID=MEMBERID))
    results = []
    for result in rs:
        results = list(result[:])
    return results

def add_econ_member(input):
    (SERVERID,MEMBERID,AMOUNT) = input
    query = 'INSERT INTO Economy VALUES(:SERVERID, :MEMBERID, :AMOUNT)'
    con.execute(query,dict(SERVERID=SERVERID,MEMBERID=MEMBERID,AMOUNT=AMOUNT))
    conn.commit()

def create_hero(input):
    (SERVERID,Name,Portrait,Description,Creator,Type,Rating,HP,ATK,DEF,SDEF,SPD) = input
    query = 'INSERT INTO Heroes VALUES(:SERVERID,:Name,:Portrait,:Description,:Creator,:Type,:Rating,:HP,:ATK,:DEF,:SDEF,:SPD)'
    con.execute(query,dict(SERVERID=SERVERID,Name=Name,Portrait=Portrait, Description=Description,Creator=Creator,Type=Type,Rating=Rating,HP=HP,ATK=ATK,DEF=DEF,SDEF=DEF,SPD=SPD))
    conn.commit()



def create_economy(input):
    (SERVERID,ENABLED) = input
    query = 'INSERT INTO Economy_Enabled VALUES(:SERVERID, :ENABLED)'
    con.execute(query,dict(SERVERID=SERVERID,ENABLED=ENABLED))
    conn.commit()
    





def print_heroes():
    query = 'SELECT * FROM Heroes'
    rs = con.execute(query)
    results = []
    for user in rs:
        results = list(user[:])
    print(results)
    return results

