import api
import csv
import pandas as pd
import sys
import nhl_stats_db as db
import nhl_main_window as MainWindow
from sqlite3 import Error 
from PyQt5 import QtWidgets

# Load team ids on init
teams = {}

PLAYER_STATS_RENAMED = ['Player_ID', 'Full_Name', 'Team_ID', 'Team_Name', 'Age', 'Height',
                        'Weight', 'Country', 'Number', 'Shoots', 'Position', 'Games_Played',
                        'Goals', 'Assists', 'Points', 'Plus_Minus', 'PIM', 'PPG', 'PPP', 'SHG', 'SHP', 
                        'GWG', 'OTG', 'S' , 'Shot_Percent', 'Blk', 'FO_Percent', 'Hits']

GOALIE_STATS_RENAMED = ['Player_ID', 'Full_Name', 'Team_ID', 'Team_Name', 'Age', 'Height',
                        'Weight', 'Country', 'Number', 'Catches', 'Position', 'Games_Played',
                        'Games_Started', 'Wins', 'Losses', 'OT', 'Shutouts', 'Saves', 'Save_Percentage',
                        'GAA', 'GA', 'SA']

def init():
    # Create a connection to the database
    conn = db.create_connection('nhl_stats.db')
    
    if conn is not None:
        # Create the team and player tables
        db.create_teams_table(conn)
        db.create_players_table(conn)
        db.create_goalies_table(conn)
    conn.close()
    
    get_team_stats()
    create_teams_dict()
        
#    get_stat_leaders()
#    get_goalie_leaders()
#    get_player_stats()

# Saves all player ids for every team
def get_and_save_player_ids():
    all_player_ids = pd.DataFrame()
    for id in teams.keys():
        # get playerids for each team
        result = api.get_player_ids_from_team(id)
        if result is None:
            return None
        else:
            all_player_ids = all_player_ids.append(result)
    all_player_ids.to_csv("resources/player_ids/players.csv", index=False)
    return all_player_ids
    
# Makes a request to get all the teams stats and adds it to the database
def get_team_stats():
    try:
        conn = db.create_connection('nhl_stats.db')
        # Request team and standing stats
        team_stats = api.get_all_team_stats()
        team_standings = api.get_standings()
        
        # Join the stats and standings table into one
        team_stats = team_stats.merge(team_standings, on=['Team_ID', 'Team_Name'])
            
        # Update the database
        team_stats.to_sql('teams', conn, if_exists='replace', index=False)
        conn.close()
        return team_stats
    except Error as e:
        print(e)
    
# Takes in a list of player ids and requests their stats from the NHL API and 
# returns their player statistics for the current season in a pandas DataFrame
#def get_player_stats():
#    conn = db.create_connection('nhl_stats.db')
#    goalies = pd.DataFrame()
#    players = pd.DataFrame()
#    # Iterate through all player ids
#    try:
##        player_ids = pd.read_csv("resources/player_ids/players.csv")
##        print(player_ids)
##        players, goalies = api.get_all_player_season_stats(player_ids, '20192020')
#        
#        with open("resources/player_ids/players.csv".format(id), 'r', encoding='utf-8-sig') as player_ids_file:
#            reader = csv.DictReader(player_ids_file, delimiter=',')
#            for player_id in reader:
#            # Request player stat from NHL API
#                result, isGoalie = api.get_player_stats(player_id['playerIDs'], '20192020')
#                
#                # Insert data into players database table
#                if (isGoalie):
#                    goalies = pd.concat([result, goalies], ignore_index=True)
#                else:
#                    players = pd.concat([result, players], ignore_index=True)
#            
#            goalies.to_sql('tmp_goalies', con=conn, if_exists='append', index=False)
#            players.to_sql('tmp_players', con=conn, if_exists='append', index=False)
#        
#        goalies.to_sql('goalies', con=conn, if_exists='replace', index=False)
#        players.to_sql('players', con=conn, if_exists='replace', index=False)
#                
#    except IOError as e:
#        # Get all player ids from teams
#        player_ids = get_and_save_player_ids()
#        
#        # Use player ids to get player stats
#        for player_id in player_ids.itertuples():
#            # Request player stat from NHL API
#            result, isGoalie = api.get_player_stats(player_id[0], '20192020')
#            
#            # Insert data into players database table
#            if (isGoalie):
#                goalies = pd.concat([result, goalies], ignore_index=True)
#            else:
#                players = pd.concat([result, players], ignore_index=True)
#        
#        goalies.to_sql('goalies', con=conn, if_exists='replace', index=False)
#        players.to_sql('players', con=conn, if_exists='replace', index=False)
#        
#        print(e)
#        
#    conn.close()

# Gets the stats of all NHL skaters as shown in the NHL stat leader page, filters out unwanted stats,
# and inserts it into the database.
def get_stat_leaders():
    conn = db.create_connection('nhl_stats.db')
    
    stat_leaders = pd.DataFrame()
    for i in range(9):
        result = api.get_stat_leaders('20192020', i)
        stat_leaders = pd.concat([stat_leaders, result], ignore_index=True)
    stat_leaders.to_sql('players', con=conn, if_exists='replace', index=False)
    conn.close()

# Gets the stats of all NHL goalies as shown in the NHL stat leader page, filters out unwanted stats,
# and inserts it into the database.
def get_goalie_leaders():
    conn = db.create_connection('nhl_stats.db')
    goalie_leaders = pd.DataFrame()
    result = api.get_goalie_stats('20192020')
    goalie_leaders = pd.concat([goalie_leaders, result], ignore_index=True)

    goalie_leaders.to_sql('goalies', con=conn, if_exists='replace', index=False)
    conn.close()    

def create_teams_dict():
    conn = db.create_connection('nhl_stats.db')
    c = conn.cursor()
    c.execute("SELECT Team_ID, Abbreviation FROM teams")
    rows = c.fetchall()
    for row in rows:
        teams[row[0]] = row[1]
    conn.close()
    
    
if __name__ == "__main__":
    init()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow.NHL_MainWindow(teams)
    MainWindow.show()
    sys.exit(app.exec_())
    