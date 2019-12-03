import sqlite3
from sqlite3 import Error          
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn
    
#    engine = None
##    conn = None
#    try:
#        engine = db.create_engine('sqlite:///{}')
#        return engine
#    except Error as e:
#        print(e)
#    return engine

def create_engine(db_file):
    engine = None
    try:
        engine = db.create_engine('sqlite:///{}'.format(db_file))
    except Error as e:
        print(e)
    return engine

# Create Tables to hold team and player stats
def create_teams_table(conn):
    
    sql_create_teams_table = """ CREATE TABLE IF NOT EXISTS teams
          ([Team_ID] INTEGER PRIMARY KEY, [Team_Name] TEXT, [Games_Played] INTEGER, [Wins] INTEGER,
          [Losses] INTEGER, [OT] INTEGER, [Points] INTEGER, [Regulation_Wins] INTEGER, [ROW] INTEGER, 
          [Goals_Scored] INTEGER, [Goals_Against] INTEGER, [Goal_Diff] INTEGER, [Streak] TEXT,
          [GPG] FLOAT, [GAPG] FLOAT, [PP_Percent] FLOAT, [PK_Percent] FLOAT, [Conference] TEXT, [Division] TEXT)"""
    
    try:
        c = conn.cursor()
        c.execute(sql_create_teams_table)
    except Error as e:
        print(e)
        
def create_players_table(conn):
    sql_create_players_table =  """ CREATE TABLE IF NOT EXISTS players
          ([Player_ID] INTEGER PRIMARY KEY, [Full_Name] TEXT, [Team_ID] INTEGER, [Team_Name] TEXT, [Age] INTEGER, 
          [Height] TEXT, [Weight] INTEGER, [Country] TEXT, [Number] INTEGER, [Shoots] TEXT, [Position] TEXT,
          [Games_Played] INTEGER, [Goals] INTEGER, [Assists] INTEGER, [Points] INTEGER, [Plus_Minus] INTEGER, [PIM] INTEGER,
          [PPG] INTEGER, [PPP] INTEGER, [SHG] INTEGER, [SHP] INTEGER, [GWG] INTEGER, [OTG] INTEGER, [S] INTEGER, [Shot_Percent] FLOAT,
          [Blk] INTEGER, [FO_Percent] FLOAT, [Hits] INTEGER, FOREIGN KEY(Team_ID) REFERENCES TEAMS(Team_ID))"""
             
    try:
        c = conn.cursor()
        c.execute(sql_create_players_table)
    except Error as e:
        print(e)
    
# Create a goalie table
def create_goalies_table(conn):
    sql_create_goalies_table = """ CREATE TABLE IF NOT EXISTS goalies ([Player_ID] INTEGER PRIMARY KEY, 
        [Full_Name] TEXT, [Team_ID] INTEGER, [Team_Name] TEXT, [Age] INTEGER, [Height] TEXT, 
        [Weight] INTEGER, [Country] TEXT, [Number] INTEGER, [Catches] TEXT, [Position] TEXT, [Games_Played] INTEGER,
        [Games_Started] INTEGER, [Wins] INTEGER, [Losses] INTEGER, [OT] INTEGER, [Shutouts] INTEGER, [Saves] INTEGER,
        [Save_Percentage] FLOAT, [GAA] FLOAT, [GA] INTEGER, [SA] INTEGER, FOREIGN KEY (Team_ID) REFERENCES TEAMS(Team_ID))"""    
    try:
        c = conn.cursor()
        c.execute(sql_create_goalies_table)
    except Error as e:
        print(e)