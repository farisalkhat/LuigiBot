import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import sql
import itertools


conn = sqlite3.connect('db\sqldatabase.db')  # You can create a new database by changing the name within the quotes
con = conn.cursor()


'''
The following commands are meant for the SmashBros commands!
'''
def get_smashplayers(SERVERID):
    query = 'SELECT USERNAME, SWITCHCODE, MAIN  FROM SmashUsers WHERE SERVERID = :SERVERID'
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
    query = 'SELECT USERNAME, SWITCHCODE, MAIN  FROM SmashUsers WHERE SERVERID = :SERVERID AND USERNAME= :USERNAME'
    rs = con.execute(query,dict(SERVERID=SERVERID,USERNAME=USERNAME))
    results = []
    for user in rs:
        results = list(user[:])
    return results
def get_smashplayers_secondaries(SERVERID,USERNAME):
    query = 'SELECT SECONDARY FROM SmashUsers_Secondaries WHERE SERVERID = :SERVERID AND USERNAME= :USERNAME'
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
def edit_profile_switchcode(input):
    (SERVERID, USERNAME, SWITCHCODE) = input
    query = 'UPDATE SmashUsers SET SWITCHCODE = :SWITCHCODE WHERE SERVERID = :SERVERID AND USERNAME = :USERNAME ;'
    con.execute(query,dict(SERVERID=SERVERID,USERNAME=USERNAME,SWITCHCODE=SWITCHCODE))
    conn.commit()
def edit_profile_main(input):
    (SERVERID, USERNAME, MAIN) = input
    query = 'UPDATE SmashUsers SET MAIN = :MAIN WHERE SERVERID = :SERVERID AND USERNAME = :USERNAME ;'
    con.execute(query,dict(SERVERID=SERVERID,USERNAME=USERNAME,MAIN=MAIN))
    conn.commit()
def delete_secondaries(input):
    (SERVERID, USERNAME) = input
    query = 'DELETE FROM SmashUsers_Secondaries WHERE SERVERID = :SERVERID AND USERNAME = :USERNAME ;'
    con.execute(query,dict(SERVERID=SERVERID,USERNAME=USERNAME))
    conn.commit()
def delete_profile(input):
    (SERVERID, USERNAME) = input
    query = 'DELETE FROM SmashUsers WHERE SERVERID = :SERVERID AND USERNAME = :USERNAME ;'
    con.execute(query,dict(SERVERID=SERVERID,USERNAME=USERNAME))
    conn.commit()
    


         

'''
The following commands are all meant for game commands!
'''

def get_configs():
    query = 'SELECT * FROM Race_Configs'
    rs = con.execute(query)
    results = []
    for user in rs:
        results.append(list(user[:]))
    return results

def get_config(SERVERID):
    query = 'SELECT * FROM Race_Configs WHERE SERVERID=:SERVERID'
    rs = con.execute(query,dict(SERVERID=SERVERID))
    results = []
    for result in rs:
        results = list(result[:])
    return results

def set_prize(input):
    (SERVERID,MIN,MAX) = input
    query = 'UPDATE Race_Configs SET MIN_PRIZE = :MIN, MAX_PRIZE = MAX WHERE SERVERID =:SERVERID'
    con.execute(query,dict(SERVERID=SERVERID,MIN=MIN,MAX=MAX))
    conn.commit()


def create_config(SERVERID):
    query = 'INSERT INTO Race_Configs VALUES(:SERVERID,2,10,1,30)'
    con.execute(query,dict(SERVERID=SERVERID))
    conn.commit()

def delete_config(SERVERID):
    query = 'DELETE FROM Race_Configs WHERE SERVERID = :SERVERID'
    con.execute(query,dict(SERVERID=SERVERID))
    conn.commit()


'''
The following commands are meant for the server economy.
'''
def set_balance(input):
    (SERVERID,MEMBERID,BALANCE) = input
    query = 'UPDATE Economy  SET LUIGICOIN = :BALANCE WHERE SERVERID = :SERVERID AND MEMBERID = :MEMBERID'
    con.execute(query,dict(SERVERID=SERVERID,MEMBERID=MEMBERID,BALANCE=BALANCE))
    conn.commit()
def get_economy(SERVERID):
    query = 'SELECT * FROM Economy_Enabled WHERE SERVERID = :SERVERID'
    rs = con.execute(query,dict(SERVERID=SERVERID))
    results = []
    for result in rs:
        results = list(result[:])
    return results
def add_econ_member(input):
    (SERVERID,MEMBERID,AMOUNT) = input
    query = 'INSERT INTO Economy VALUES(:SERVERID, :MEMBERID, :AMOUNT)'
    con.execute(query,dict(SERVERID=SERVERID,MEMBERID=MEMBERID,AMOUNT=AMOUNT))
    conn.commit()
def create_economy(input):
    (SERVERID,ENABLED) = input
    query = 'INSERT INTO Economy_Enabled VALUES(:SERVERID, :ENABLED)'
    con.execute(query,dict(SERVERID=SERVERID,ENABLED=ENABLED))
    conn.commit()
def get_balance(input):
    (SERVERID,MEMBERID) = input
    query = 'SELECT * FROM Economy WHERE SERVERID = :SERVERID AND MEMBERID = :MEMBERID'
    rs = con.execute(query,dict(SERVERID=SERVERID,MEMBERID=MEMBERID))
    results = []
    for result in rs:
        results = list(result[:])
    return results


def set_botchannel(input):
    (SERVERID,CHANNELID) = input
    query = 'INSERT INTO Botcommand_Channels VALUES(:SERVERID,:CHANNELID)'
    con.execute(query,dict(SERVERID=SERVERID,CHANNELID=CHANNELID))
    conn.commit()

def get_botchannel(input):
    (SERVERID,CHANNELID) = input
    query = 'SELECT * FROM Botcommand_Channels WHERE SERVERID=:SERVERID AND CHANNELID=:CHANNELID'
    rs = con.execute(query,dict(SERVERID=SERVERID,CHANNELID=CHANNELID))
    results = []
    for result in rs:
        results = list(result[:])
    if results:
        return True
    return False