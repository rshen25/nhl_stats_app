import api
import json
import csv
#from os import path
import pandas as pd
import nhl_stats_db as db

# Load team ids on init
team_ids = [1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,28,29,30,52,53,54]

STANDING_STATS_WANTED = ['team.id', 'team.name', 'gamesPlayed', 'leagueRecord.wins', 'leagueRecord.losses', 
                         'leagueRecord.ot', 'points', 'regulationWins', 'row',
                         'goalsScored', 'goalsAgainst', 'goalDiff', 'streak.streakCode']

sql_create_teams_table = """ CREATE TABLE TEAMS
          ([Team_ID] INTEGER PRIMARY KEY, [Team_Name] TEXT, [Games_Played] INTEGER, [Wins] INTEGER,
          [Losses] INTEGER, [OT] INTEGER, [Points] INTEGER, [Regulation_Wins] INTEGER, [ROW] INTEGER, 
          [Goals_Scored] INTGER, [Goals_Against] INTEGER, [Goal_Diff] INTEGER, [Streak] TEXT,
          [GPG] FLOAT, [GAPG] FLOAT, [PP%] FLOAT, [PK%] FLOAT, [Conference] TEXT, [Division] TEXT)"""

sql_create_players_table =  """ CREATE TABLE PLAYERS
          ([Player_ID] INTEGER PRIMARY KEY, [Team_ID] INTEGER, [Team_Name] TEXT, [Full_Name] TEXT, [Age] INTEGER,
          [Games_Played] INTEGER, [Goals] INTEGER, [Assists] INTEGER, [Points] INTEGER, [+/-] INTEGER, [PIM] INTEGER,
          [PPG] INTEGER, [PPP] INTEGER, [SHG] INTEGER, [SHP] INTEGER, [GWG] INTEGER, [OTG] INTEGER, [S] INTEGER, [S%] FLOAT,
          [Blk] INTEGER, [FO%] FLOAT, [Hits] INTEGER, FOREIGN KEY(Team_ID) REFERENCES TEAMS(Team_ID))"""

def jprint(json_obj):
    with open('data.json', 'w', encoding='utf-8') as outfile:
        json.dump(json_obj, outfile, ensure_ascii=False, indent=4)
    text = json.dumps(json_obj, sort_keys=True, indent=4)
    print(text)

def init_program():    
#    init_team_ids()
    print(team_ids)

#def init_team_ids():
#    with open('resources/teamID.csv', 'r', encoding='utf-8-sig') as teamIds_file:
#        reader = csv.DictReader(teamIds_file, delimiter=',')
#        #Iterate through team IDs and get each player ID
#        for row in reader:
#            team_ids.append(row['teamID'])

# Saves all player ids for every team
def get_and_save_player_ids():
    all_player_ids = pd.DataFrame()
    
    #load team ids from file
#    with open('resources/teamID.csv', 'r', encoding='utf-8-sig') as teamIds_file:
#        reader = csv.DictReader(teamIds_file, delimiter=',')
        #teamIds = list(reader)
        #Iterate through team IDs and get each player ID
    for id in team_ids:
            # get playerids for each team
#            print(row['teamID'])
        result = api.get_player_ids_from_team(id)
        if result is None:
            return None
        else:
            all_player_ids = all_player_ids.append(result)
    
    # Testing Purposes:
#    result = api.get_player_ids_from_team(11)
#    if result is None:
#        return None
#    else:
#        all_player_ids = all_player_ids.append(result)
    
#    playerIds = pd.DataFrame()

    #iterate through all playerids
        # get the player stats via api & parser

# Makes a request to get all the teams stats and adds it to the database
def get_team_stats(conn):
    # Request team and standing stats
    team_stats = api.get_all_team_stats()
    team_standings = api.get_standings()
    
    # Join the stats and standings table into one
    team_stats = team_stats.merge(team_standings, on=['Team_ID', 'Team_Name'])
    
    # Update the database
    team_stats.to_sql('TEAMS', conn, if_exists='replace', index=False)
        
    return team_stats
    
# TODO: Takes in a list of player ids and requests their stats from the NHL API and 
# returns their player statistics for the current season in a pandas DataFrame
def get_player_stats(player_ids):
    # Iterate through all player ids
    with open("resources/player_ids/1_players.csv".format(id), 'r', encoding='utf-8-sig') as player_ids_file:
        reader = csv.DictReader(player_ids_file, delimiter=',')
        for player_id in reader:
        # Request player stat from NHL API
            print(player_id['0'])    
    return None

if __name__ == "__main__":
    # Create a connection to the database
    conn = db.create_connection('nhl_stats.db')
    
    if conn is not None:
        # Create the team and player tables
        db.create_table(conn, sql_create_teams_table)
        db.create_table(conn, sql_create_players_table)
        
    get_team_stats(conn)
    
    c = conn.cursor()
    c.execute("SELECT * FROM TEAMS WHERE TEAM_NAME = 'Vancouver Canucks'")
    rows = c.fetchall()
    for row in rows:
        print(row)

#    init_program()
    
#    api.get_player_stats('8476941', '8477290', '8473507')
    api.get_player_stats('8473507')
#    api.get_player_ids_from_team(23)
    #jprint(api.get_teams())
#    result = api.get_teams()
#    print(result)
#    result.to_csv('test2.csv')
    
#    metro, atlantic, central, pacific = api.get_standings()
#    metro.to_csv('metro.csv')
#    atlantic.to_csv('atlantic.csv')
#    central.to_csv('central.csv')
#    pacific.to_csv('pacific.csv')
    
#    if (not path.exists("resources/playerIDs")) and (not path.exists("resources/playerIDs/1_players.csv")):
#        get_and_save_player_ids()
    
#    api.get_player_ids_from_team()