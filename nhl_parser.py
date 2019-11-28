import pandas as pd
from pandas.io.json import json_normalize
import json

TEAM_STATS_WANTED = ['team.name', 'stat.gamesPlayed', 'stat.wins', 'stat.losses', 'stat.ot',
                'stat.pts', 'stat.goalsPerGame', 'stat.goalsAgainstPerGame', 
                'stat.powerPlayPercentage', 'stat.penaltyKillPercentage']

STANDING_STATS_WANTED = ['team.id', 'team.name', 'gamesPlayed', 'leagueRecord.wins', 'leagueRecord.losses', 
                         'leagueRecord.ot', 'points', 'regulationWins', 'row',
                         'goalsScored', 'goalsAgainst', 'goalDiff', 'streak.streakCode']

PLAYER_STATS_WANTED = ['stat.games', 'stat.goals', 'stat.assists', 'stat.points', 'stat.plusMinus',
                       'stat.pim', 'stat.powerPlayGoals', 'stat.powerPlayPoints', 'stat.shortHandedGoals',
                       'stat.shortHandedPoints', 'stat.gameWinningGoals', 'stat.overTimeGoals', 
                       'stat.shots', 'stat.shotPct', 'stat.blocked', 'stat.faceOffPct', 'stat.hits']


team_cols = ['Team_ID', 'Team_Name', 'Abbrv', 'Games_Played', 'Wins', 'Losses', 'OT',
             'Points', 'GPG', 'GAPG', 'PP%', 'PK%']

player_cols = ['Player_ID', 'Team_ID', 'Team_Name', 'Full_Name', 'Age', 'Games_Played', 
               'Goals', 'Assists', 'Points', '+/-', 'PIM', 'PPG', 'PPP', 'SHG', 'SHP', 
               'GWG', 'OTG', 'S' , 'S%', 'Blk', 'FO%', 'Hits']


# Removes unnecessary columns and returns every team in the NHL and their season stats
def parse_teams(json_data):

    del json_data['copyright']
    # Get the team stats
    team_stats = pd.DataFrame()
    conference = pd.DataFrame()
    division = pd.DataFrame()
    for k in json_data['teams']:
        tmp = json_normalize(k['teamStats'][0]['splits'][0])
        team_stats = team_stats.append(tmp, ignore_index = True)
        
        # Get conference/division
        tmp_c = json_normalize(k['conference'])
        conference = conference.append(tmp_c, ignore_index = True)
        
        tmp_d = json_normalize(k['division'])
        division = division.append(tmp_d, ignore_index = True)
        
    # Get only columns/stats that we want
    team_stats = team_stats[TEAM_STATS_WANTED].copy()
    
    # Add conference/division column to results
    team_stats['conference'] = conference['name']
    team_stats['division'] = division['name']
    
    return team_stats

# Parses the standings data to only keep the stats that we want and separates them into their
# respective divisions
def parse_standings(json_data):
    del json_data['copyright']
    
    metro = json_normalize(json_data['records'][0]['teamRecords'])
    atlantic = json_normalize(json_data['records'][1]['teamRecords'])
    central = json_normalize(json_data['records'][2]['teamRecords'])
    pacific = json_normalize(json_data['records'][3]['teamRecords'])
    
    metro = calculate_goal_difference(metro)
    metro = metro[STANDING_STATS_WANTED].copy()
    atlantic = calculate_goal_difference(atlantic)
    atlantic = atlantic[STANDING_STATS_WANTED].copy()
    central = calculate_goal_difference(central)
    central = central[STANDING_STATS_WANTED].copy()
    pacific = calculate_goal_difference(pacific)
    pacific = pacific[STANDING_STATS_WANTED].copy()
    
    return metro, atlantic, central, pacific

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
#    player_ids = []
#    for k in team_player_data['data']:
#        player_ids.append(k['id'])
#    player_ids = pd.DataFrame(player_ids)
#    return player_ids
    del team_player_data['copyright']
    player_ids = []
    player_names = []
    for k in team_player_data['roster']:
        player_ids.append(k['person']['id'])
        player_names.append(k['person']['fullName'])
    player_data = {'playerIDs': player_ids, 'playerNames': player_names}
    result = pd.DataFrame(player_data, columns=['playerIDs', 'playerNames'])
    return result


# TODO: Given the json data for a player, filter out unwanted stats and return in pandas Dataframe
def parse_player_stats(player_data):
#    del player_data['copyright']
#    result = pd.DataFrame()
#    for k in player_data['splits']:
    
    # Testing ------------------------------------------
    with open('test_stats.json', 'r') as json_file:
        stats = json.load(json_file)
        player_data = json_normalize(stats['stats'][0]['splits'])
        print(player_data)
        result = player_data[PLAYER_STATS_WANTED].copy()
#        result.to_csv('test_stats.csv')
#        result = pd.read_json(player_data)
#    result = pd.read_json(player_data['stats']['splits'])
#    print (result)
    return result