import api
import json
#from os import path
import csv
import pandas as pd
import nhl_stats_db as db

# Load team ids on init
team_ids = []

sql_create_teams_table = """ CREATE TABLE TEAMS
          ([Team_ID] INTEGER PRIMARY KEY, [Team_Name] TEXT, [Abbrv.] TEXT, [Games_Played] INTEGER, [Wins] INTEGER,
          [Losses] INTEGER, [OT] INTEGER, [Points] INTEGER, [GPG] FLOAT, [GAPG] FLOAT, [PP%] FLOAT, [PK%] FLOAT)"""

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
    init_team_ids()
    print(team_ids)

def init_team_ids():
    with open('resources/teamID.csv', 'r', encoding='utf-8-sig') as teamIds_file:
        reader = csv.DictReader(teamIds_file, delimiter=',')
        #Iterate through team IDs and get each player ID
        for row in reader:
            team_ids.append(row['teamID'])

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
    
# TODO: Takes in a list of player ids and requests their stats from the NHL API and 
# returns their player statistics for the current season in a pandas DataFrame
def get_player_stats(player_ids):
    
    # Iterate through all player ids
#    for id in team_ids:
##        player_ids = pd.read_csv("resources/player_ids/{}_players.csv".format(id))
##            
##            for player_id in player_ids
#        with open("resources/player_ids/{}_players.csv".format(id), 'r', encoding='utf-8-sig') as player_ids_file:
#            reader = csv.DictReader(player_ids_file, delimiter=',')
#            for player_id in reader:
#                # Request player stat from NHL API
#                print(player_id['0'])    
    return None

if __name__ == "__main__":
    # Create a connection to the database
    conn = db.create_connection('nhl_stats.db')
    
    if conn is not None:
        # Create the team and player tables
        db.create_table(conn, sql_create_teams_table)
        db.create_table(conn, sql_create_players_table)

#    init_program()
    
#    get_player_stats(['8476941', '8477290', '8473507'])
#    api.get_player_stats('8476941')
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