import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import sql
import itertools


conn = sqlite3.connect('db\gachaecon.db')  # You can create a new database by changing the name within the quotes
con = conn.cursor()


def get_hero(HERO_NAME):
    query = 'SELECT * FROM Heroes WHERE Name = :HERO_NAME'
    rs = con.execute(query,dict(HERO_NAME=HERO_NAME))
    results = []
    for user in rs:
        results = list(user[:])
    return results

def print_heroes():
    query = 'SELECT * FROM Heroes'
    rs = con.execute(query)
    results = []
    for user in rs:
        results = list(user[:])
    print(results)
    return results

