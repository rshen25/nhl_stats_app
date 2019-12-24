import pandas as pd
from pandas.io.json import json_normalize

TEAM_STATS_WANTED = ['team.id', 'team.name', 'stat.gamesPlayed', 'stat.wins', 'stat.losses', 'stat.ot',
                'stat.pts', 'stat.goalsPerGame', 'stat.goalsAgainstPerGame', 
                'stat.powerPlayPercentage', 'stat.penaltyKillPercentage']

TEAM_STATS_RENAMED = ['Team_ID', 'Team_Name', 'Games_Played', 'Wins', 'Losses', 'OT',
             'Points', 'GPG', 'GAPG', 'PP_Percent', 'PK_Percent']


STANDING_STATS_WANTED = ['team.id', 'team.name', 'regulationWins', 'row',
                         'goalsScored', 'goalsAgainst', 'goalDiff', 'streak.streakCode']

STANDINGS_STATS_RENAMED = ['Team_ID', 'Team_Name', 'Regulation_Wins', 'ROW', 'Goals_Scored', 
                           'Goals_Against' , 'Goal_Diff' , 'Streak']

PLAYER_STATS_WANTED = ['stat.games', 'stat.goals', 'stat.assists', 'stat.points', 'stat.plusMinus',
                       'stat.pim', 'stat.powerPlayGoals', 'stat.powerPlayPoints', 'stat.shortHandedGoals',
                       'stat.shortHandedPoints', 'stat.gameWinningGoals', 'stat.overTimeGoals', 
                       'stat.shots', 'stat.shotPct', 'stat.blocked', 'stat.faceOffPct', 'stat.hits']

PLAYER_DATA_WANTED = ['id', 'fullName', 'currentTeam.id', 'currentTeam.name', 'currentAge',
                      'height', 'weight', 'birthCountry', 'primaryNumber', 
                       'shootsCatches', 'primaryPosition.code']

PLAYER_STATS_RENAMED = ['Player_ID', 'Full_Name', 'Team_ID', 'Team_Name', 'Age', 'Height',
                        'Weight', 'Country', 'Number', 'Shoots', 'Position', 'Games_Played',
                        'Goals', 'Assists', 'Points', 'Plus_Minus', 'PIM', 'PPG', 'PPP', 'SHG', 'SHP', 
                        'GWG', 'OTG', 'S' , 'Shot_Percent', 'Blk', 'FO_Percent', 'Hits']

GOALIE_STATS_WANTED = ['stat.games', 'stat.gamesStarted', 'stat.wins', 'stat.losses', 
                       'stat.ot', 'stat.shutouts', 'stat.saves', 'stat.savePercentage', 
                       'stat.goalAgainstAverage', 'stat.goalsAgainst', 'stat.shotsAgainst']

GOALIE_STATS_RENAMED = ['Player_ID', 'Full_Name', 'Team_ID', 'Team_Name', 'Age', 'Height',
                        'Weight', 'Country', 'Number', 'Catches', 'Position', 'Games_Played',
                        'Games_Started', 'Wins', 'Losses', 'OT', 'Shutouts', 'Saves', 'Save_Percentage',
                        'GAA', 'GA', 'SA']

team_cols = ['Team_ID', 'Team_Name', 'Games_Played', 'Wins', 'Losses', 'OT',
             'Points', 'Regulation_Wins', 'ROW', 'Goals_Scored', 'Goals_Against', 
             'Goal_Diff', 'Streak', 'GPG', 'GAPG', 'PP_Percent', 'PK_Percent', 'Conference', 'Division']

player_cols = ['Player_ID', 'Full_Name', 'Team_ID', 'Team_Name', 'Age', 'Height', 'Weight', 'Country', 'Number',
               'Shoots', 'Position', 'Games_Played', 'Goals', 'Assists', 'Points', 'Plus_Minus', 'PIM',
               'PPG', 'PPP', 'SHG', 'SHP', 'GWG', 'OTG', 'S' , 'Shot_Percent', 'Blk', 'FO_Percent', 'Hits']


# Removes unnecessary columns and returns every team in the NHL and their season stats
def parse_teams(json_data):

    del json_data['copyright']
    # Get the team stats
    team_stats = pd.DataFrame()
    conference = pd.DataFrame()
    division = pd.DataFrame()
    abbreviation = pd.DataFrame(columns=['abbreviation'])
    for index, k in enumerate(json_data['teams']):
        tmp = json_normalize(k['teamStats'][0]['splits'][0])
        team_stats = team_stats.append(tmp, ignore_index = True)
        
        # Get conference/division
        tmp_c = json_normalize(k['conference'])
        conference = conference.append(tmp_c, ignore_index = True)
        
        tmp_d = json_normalize(k['division'])
        division = division.append(tmp_d, ignore_index = True)
        
        abbreviation.loc[index] = k['abbreviation']

    # Get only columns/stats that we want
    team_stats = team_stats[TEAM_STATS_WANTED].copy()
    
    # Rename the columns
    team_stats.columns = TEAM_STATS_RENAMED
    
    # Add conference/division column to results
    team_stats['Conference'] = conference['name']
    team_stats['Division'] = division['name']
    team_stats['Abbreviation'] = abbreviation['abbreviation']
    
    return team_stats

# Parses the standings data to only keep the stats that we want
def parse_standings(json_data):
    del json_data['copyright']
    
    # Normalize the json data and separate the standings based on division
    metro = json_normalize(json_data['records'][0]['teamRecords'])
    atlantic = json_normalize(json_data['records'][1]['teamRecords'])
    central = json_normalize(json_data['records'][2]['teamRecords'])
    pacific = json_normalize(json_data['records'][3]['teamRecords'])
    
    # Calculate the goal differential for each team and filter 
    metro = calculate_goal_difference(metro)
    metro = metro[STANDING_STATS_WANTED].copy()
    atlantic = calculate_goal_difference(atlantic)
    atlantic = atlantic[STANDING_STATS_WANTED].copy()
    central = calculate_goal_difference(central)
    central = central[STANDING_STATS_WANTED].copy()
    pacific = calculate_goal_difference(pacific)
    pacific = pacific[STANDING_STATS_WANTED].copy()
    
    # Rename the columns to math the database
    metro.columns = STANDINGS_STATS_RENAMED
    atlantic.columns = STANDINGS_STATS_RENAMED
    central.columns = STANDINGS_STATS_RENAMED
    pacific.columns = STANDINGS_STATS_RENAMED
    
    result = pd.concat([metro, atlantic, central, pacific], ignore_index=True)
    
    return result

def calculate_goal_difference(df):
    df['goalDiff'] = df['goalsScored'] - df['goalsAgainst']
    return df

def get_standing_stats(division_json):
    standings = pd.DataFrame()
    for k in division_json:
        tmp = json_normalize(k['teamRecords'])
        standings = standings.append(tmp, ignore_index=True)
    return standings

# Given a json data of all players within a team, get all player ids within the team
def parse_player_ids(team_player_data):
    del team_player_data['copyright']
    player_ids = []
    player_names = []
    for k in team_player_data['roster']:
        player_ids.append(k['person']['id'])
        player_names.append(k['person']['fullName'])
    player_data = {'playerIDs': player_ids, 'playerNames': player_names}
    result = pd.DataFrame(player_data, columns=['playerIDs', 'playerNames'])
    return result

# Given the json data for a player, filter out unwanted stats and return in pandas Dataframe
def parse_player_stats(player_data, player_stats):    
    isGoalie = False
    
    # Get normalize the json data into pandas DataFrames
    player_stats = json_normalize(player_stats['stats'][0]['splits'])
    player_data = json_normalize(player_data['people'])
        
    player_data = player_data[PLAYER_DATA_WANTED]
    
    # Filter out the stats that we do not want
    try:
        if len(player_stats.columns) > 0:
            if (player_data['primaryPosition.code'][0] == 'G'):
                player_stats = player_stats[GOALIE_STATS_WANTED].copy()
                
                # Merge the player data and statistic DataFrames
                result = player_data.merge(player_stats, left_index=True, right_index=True)
    
                # Rename the column names to match the database
                result.columns = GOALIE_STATS_RENAMED

                isGoalie = True
                
                return result, isGoalie
                
            else:
                player_stats = player_stats[PLAYER_STATS_WANTED].copy()
                
        else:
            player_stats = pd.DataFrame(columns=PLAYER_STATS_WANTED)

    except KeyError as e:
        player_stats = pd.DataFrame(columns=PLAYER_STATS_WANTED)
        print(e)    
    
    # Merge the player data and statistic DataFrames
    result = player_data.merge(player_stats, left_index=True, right_index=True)
    
    # Rename the column names to match the database
    result.columns = PLAYER_STATS_RENAMED
    
    # Testing ------------------------------------------
#    result.to_csv('test_player_stats.csv')
#    player_data.to_csv('test_player_data.csv')
    # --------------------------------------------------
    
    return result, isGoalie

def parse_player_career_stats(player_stats):
    career_stats = pd.DataFrame()
    for stats in player_stats['stats'][0]['splits']:
        tmp = json_normalize(stats)
        career_stats = pd.concat([career_stats, tmp], ignore_index=True, sort=False)

    career_stats = career_stats[['season', 'league.name', 'team.name','stat.games', 'stat.goals',
                                 'stat.assists', 'stat.points', 'stat.plusMinus', 'stat.pim', 
                                 'stat.powerPlayGoals', 'stat.powerPlayPoints', 'stat.shortHandedGoals',
                                 'stat.shortHandedPoints', 'stat.gameWinningGoals', 'stat.overTimeGoals',
                                 'stat.shots', 'stat.shotPct', 'stat.hits', 'stat.blocked']].copy()  
    
    career_stats.columns = ['Season', 'League', 'Team', 'GP', 'G', 'A', 'P', '+/-', 'PIM',
                            'PPG', 'PPP', 'SHG', 'SHP', 'GWG', 'OTG', 'S', 'S%', 'Hits', 'Blk']
    career_stats = career_stats.sort_values(by=['Season'], ascending=False)
    
    career_stats = career_stats.fillna('')
    
    return career_stats

def parse_goalie_career_stats(player_stats):
    career_stats = pd.DataFrame()
    for stats in player_stats['stats'][0]['splits']:
        tmp = json_normalize(stats)
        career_stats = pd.concat([career_stats, tmp], ignore_index=True, sort=False)

    career_stats = career_stats[['season', 'league.name', 'team.name','stat.games', 'stat.gamesStarted', 'stat.wins',
                                 'stat.losses', 'stat.ot', 'stat.ties', 'stat.goalAgainstAverage', 'stat.goalsAgainst',
                                 'stat.timeOnIce', 'stat.shutouts', 'stat.saves', 'stat.savePercentage', 
                                 'stat.powerPlaySaves', 'stat.powerPlayShots', 'stat.powerPlaySavePercentage', 
                                 'stat.shortHandedSaves', 'stat.shortHandedShots', 'stat.shortHandedSavePercentage',
                                 'stat.evenSaves', 'stat.evenShots', 'stat.evenStrengthSavePercentage']].copy()  
    
    career_stats.columns = ['Season', 'League', 'Team', 'GP', 'GS', 'W', 'L', 'OT', 'Ties',
                            'GAA', 'GA', 'TOI', 'Shutouts', 'Saves', 'Save%', 'ppSaves', 'ppShots',
                            'ppSave%', 'shSaves', 'shShots', 'shSave%', 'evenSaves', 'evenShots', 'evenSave%']
    career_stats = career_stats.sort_values(by=['Season'], ascending=False)
    
    career_stats = career_stats.fillna('')

    return career_stats
    

# Parses the data for each scheduled NHL game for the current day
def parse_games(games_data):
    
    games = pd.DataFrame()
    
    games = json_normalize(games_data['dates'][0]['games'])
    result = games[['gamePk', 'teams.away.team.id', 'teams.home.team.id']].copy()
    result.columns = ['gameID', 'awayID', 'homeID']
    
    return result

# Parses through the json player data files, filters through to get the desired stats and returns them in a dataframe
#def parse_all_player_stats(players_data, players_stats):
#    player_stats = pd.DataFrame()
#    player_data = pd.DataFrame()
#    goalie_stats = pd.DataFrame()
#    goalie_data = pd.DataFrame()
#
#    # parse player data
#    for index, player in enumerate(players_data):
#        if (player['primaryPosition.code'][0] == 'G'):
#            goalie_data = pd.concat([goalie_data, json_normalize(player_data['people'])], ignore_index=True, sort=False)
#            goalie_stats = pd.concat([goalie_stats, json_normalize(players_stats[index]['stats'][0]['splits'])], ignore_index=True, sort=False)
#            
#        else:
#            player_data = pd.concat([player_data, json_normalize(player_data['people'])], ignore_index=True, sort=False)
#            player_stats = pd.concat([player_stats, json_normalize(players_stats[index]['stats'][0]['splits'])], ignore_index=True, sort=False)
#    
#    # Filter out unwanted columns
#    player_data = player_data[PLAYER_DATA_WANTED]
#    goalie_data = goalie_data[PLAYER_DATA_WANTED]
#    
#    player_stats = player_stats[PLAYER_STATS_WANTED].copy()
#    goalie_stats = goalie_stats[GOALIE_STATS_WANTED].copy()
#        
#    # Merge player data and stats
#    goalie_stats = goalie_data.merge(goalie_stats, left_index=True, right_index=True)
#    player_stats = player_data.merge(player_stats, left_index=True, right_index=True)
#    
#    # Rename columns
#    goalie_stats.columns = GOALIE_STATS_RENAMED
#    player_stats.columns = PLAYER_STATS_RENAMED
#    
#    # TESTING ---------------------------
#    goalie_stats.to_csv("goalie_test.csv")
#    player_stats.to_csv("player_test.csv")
#    # ----------------------------------
#    
#    return player_stats, goalie_stats    