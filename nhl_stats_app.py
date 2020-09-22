import api
import pandas as pd
import sys
import nhl_parse_const as pc
import nhl_stats_db as db
import nhl_main_window as MainWindow
from sqlite3 import Error 
from PyQt5 import QtWidgets

# Load team ids on init
teams = {}

def init():
    # Create a connection to the database
    conn = db.create_connection('nhl_stats.db')
    
    conn.close()
    
    get_team_stats()
    create_teams_dict()
        
    get_stat_leaders()
    get_goalie_leaders()

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
    return all_player_ids
    
# Makes a request to get all the teams stats and adds it to the database
def get_team_stats():
    try:
        conn = db.create_connection('nhl_stats.db')
        # Request team and standing stats
        team_stats = api.get_all_team_stats()
        team_standings = api.get_standings()
        
        # If was not able to get the team stats from API
        if team_stats is None or team_standings is None:
            c = conn.cursor()
            team_stats = c.execute("SELECT * FROM teams")
        else:
            # Join the stats and standings table into one
            team_stats = team_stats.merge(team_standings, on=['Team_ID', 'Team_Name'])
            
            # Update the database
            team_stats.to_sql('teams', conn, if_exists='replace', index=False)
            
        conn.close()
        return team_stats
    except Error as e:
        print(e)
    
# Gets the stats of all NHL skaters as shown in the NHL stat leader page, filters out unwanted stats,
# and inserts it into the database.
def get_stat_leaders():
    conn = db.create_connection('nhl_stats.db')
    result = 0
    stat_leaders = pd.DataFrame()
    for i in range(9):
        result = api.get_stat_leaders(pc.CURRENT_SEASON, i)
        if result is None:
            c = conn.cursor()
            break
        stat_leaders = pd.concat([stat_leaders, result], ignore_index=True)
    if result is not None:
        stat_leaders.to_sql('players', con=conn, if_exists='replace', index=False)
    conn.close()

# Gets the stats of all NHL goalies as shown in the NHL stat leader page, filters out unwanted stats,
# and inserts it into the database.
def get_goalie_leaders():
    conn = db.create_connection('nhl_stats.db')
    goalie_leaders = pd.DataFrame()
    result = api.get_goalie_stats(pc.CURRENT_SEASON)
    
    if result is not None:
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
    