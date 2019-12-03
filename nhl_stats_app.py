import api
import csv
import pandas as pd
import nhl_stats_db as db

# Load team ids on init
team_ids = [1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,28,29,30,52,53,54]

PLAYER_STATS_RENAMED = ['Player_ID', 'Full_Name', 'Team_ID', 'Team_Name', 'Age', 'Height',
                        'Weight', 'Country', 'Number', 'Shoots', 'Position', 'Games_Played',
                        'Goals', 'Assists', 'Points', 'Plus_Minus', 'PIM', 'PPG', 'PPP', 'SHG', 'SHP', 
                        'GWG', 'OTG', 'S' , 'Shot_Percent', 'Blk', 'FO_Percent', 'Hits']

GOALIE_STATS_RENAMED = ['Player_ID', 'Full_Name', 'Team_ID', 'Team_Name', 'Age', 'Height',
                        'Weight', 'Country', 'Number', 'Catches', 'Position', 'Games_Played',
                        'Games_Started', 'Wins', 'Losses', 'OT', 'Shutouts', 'Saves', 'Save_Percentage',
                        'GAA', 'GA', 'SA']

def init_program():    
    print(team_ids)


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
    team_stats.to_sql('teams', conn, if_exists='replace', index=False)
        
    return team_stats
    
# Takes in a list of player ids and requests their stats from the NHL API and 
# returns their player statistics for the current season in a pandas DataFrame
def get_player_stats(conn):
    # Iterate through all player ids
    with open("resources/player_ids/1_players.csv".format(id), 'r', encoding='utf-8-sig') as player_ids_file:
        reader = csv.DictReader(player_ids_file, delimiter=',')
        for player_id in reader:
        # Request player stat from NHL API
#            print(player_id['0'])
            result, isGoalie = api.get_player_stats(player_id['0'], '20192020')
            
            # Insert data into players database table
            result = result.to_sql('tmp_players', con=conn, if_exists='replace', index=False)
            
            c = conn.cursor()
            
            c.execute("SELECT * FROM tmp_players")
            rows = c.fetchall()
            if (isGoalie):
                for row in rows:
                    conn.execute("""
                                 REPLACE INTO goalies({})
                                 VALUES (?, ?, ?, ?, ? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,?)
                                 """.format(','.join(GOALIE_STATS_RENAMED)),
                                 row)
            else:
                for row in rows:
                    conn.execute("""
                                 REPLACE INTO players({})
                                 VALUES (?, ?, ?, ?, ? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,?, ?, ?, ?, ?)
                                 """.format(','.join(PLAYER_STATS_RENAMED)),
                                 row)
            

if __name__ == "__main__":
    # Create a connection to the database
    conn = db.create_connection('nhl_stats.db')
    engine = db.create_engine('nhl_stats.db')
    
    if conn is not None:
        # Create the team and player tables
        db.create_teams_table(conn)
        db.create_players_table(conn)
        db.create_goalies_table(conn)
        
    get_team_stats(conn)
    c = conn.cursor()
    
    
    get_player_stats(conn)
    
    conn.close()
    