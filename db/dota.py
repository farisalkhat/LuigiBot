import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import sql
import itertools


conn = sqlite3.connect('db\Dota.db')  # You can create a new database by changing the name within the quotes
con = conn.cursor()

def set_steamid(input):
    (MEMBERID,STEAMID)= input
    query = 'INSERT INTO Dota_Profiles VALUES(:MEMBERID,:STEAMID)'
    con.execute(query,dict(MEMBERID=MEMBERID,STEAMID=STEAMID))
    conn.commit()


def get_steamid(MEMBERID):
    query = 'SELECT STEAMID from Dota_Profiles WHERE MEMBERID=:MEMBERID'
    rs = con.execute(query,dict(MEMBERID=MEMBERID))
    results = []
    for result in rs:
        results = list(result[:])
    if not results:
        return results
    actual = results[0]
    return actual

def delete_steamid(MEMBERID):
    query = 'DELETE FROM Dota_Profiles WHERE MEMBERID=:MEMBERID'
    con.execute(query,dict(MEMBERID=MEMBERID))
    conn.commit()

def set_dota_channel(input):
    (SERVERID,CHANNELID) = input
    query = 'INSERT INTO Dota_Channels VALUES(:SERVERID,:CHANNELID)'
    con.execute(query,dict(SERVERID=SERVERID,CHANNELID=CHANNELID))
    conn.commit()

def get_dota_channel(input):
    (SERVERID,CHANNELID) = input
    query = 'SELECT * FROM Dota_Channels WHERE SERVERID=:SERVERID AND CHANNELID=:CHANNELID'
    rs = con.execute(query,dict(SERVERID=SERVERID,CHANNELID=CHANNELID))
    results = []
    for result in rs:
        results = list(result[:])
    if results:
        return True
    return False