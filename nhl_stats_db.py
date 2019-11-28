import sqlite3
from sqlite3 import Error          

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

# Create Tables to hold team and player stats
def create_table(conn, sql_create_table):
    try:
        c = conn.cursor()
        c.execute(sql_create_table)
    except Error as e:
        print(e)