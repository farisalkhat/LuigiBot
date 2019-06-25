import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import sql
import itertools


conn = sqlite3.connect('db\sqldatabase.db')  # You can create a new database by changing the name within the quotes
con = conn.cursor()


def get_smashplayers(SERVERID):
    query = 'SELECT USERNAME, SWITCHCODE, MAIN  FROM SmashUsers WHERE SERVER_ID = :SERVERID'
    rs = con.execute(query,dict(SERVERID=SERVERID))
    results = {}
    for user in rs:
        results[user[0]] = list(user[:])
        #results[user.USERNAME] = list(user[:])
    return results


def get_smashprofile(SERVERID,USERNAME):
    profile = get_smashplayer(SERVERID,USERNAME)
    if not profile:
        return profile
    secondaries = get_smashplayers_secondaries(SERVERID,USERNAME)
    profile.append(secondaries)
    return profile


def get_smashplayer(SERVERID,USERNAME):
    query = 'SELECT USERNAME, SWITCHCODE, MAIN  FROM SmashUsers WHERE SERVER_ID = :SERVERID AND USERNAME= :USERNAME'
    rs = con.execute(query,dict(SERVERID=SERVERID,USERNAME=USERNAME))
    results = []
    for user in rs:
        results = list(user[:])
    return results


def get_smashplayers_secondaries(SERVERID,USERNAME):
    query = 'SELECT SECONDARY FROM SmashUsers_Secondaries WHERE SERVER_ID = :SERVERID AND USERNAME= :USERNAME'
    rs = con.execute(query,dict(SERVERID=SERVERID,USERNAME=USERNAME))
    results = []
    for user in rs:
        results.append(user)
    results2 = list(itertools.chain.from_iterable(results))
    return results2



def make_profile(input):
    (SERVERID, USERNAME,SWITCHCODE, MAIN) = input
    query = 'INSERT INTO SmashUsers VALUES (:SERVERID,:USERNAME,:SWITCHCODE,:MAIN);'
    con.execute(query,dict(SERVERID=SERVERID,USERNAME=USERNAME,SWITCHCODE=SWITCHCODE,MAIN=MAIN))
    conn.commit()

def make_profile_secondaries(input):
    (SERVERID, USERNAME, SECONDARY) = input
    query = 'INSERT INTO SmashUsers_Secondaries VALUES (:SERVERID,:USERNAME,:SECONDARY);'
    con.execute(query,dict(SERVERID=SERVERID,USERNAME=USERNAME,SECONDARY=SECONDARY))
    conn.commit()



         









