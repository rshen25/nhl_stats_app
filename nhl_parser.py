import pandas as pd
from pandas.io.json import json_normalize

TEAM_STATS_WANTED = ['team.name', 'stat.gamesPlayed', 'stat.wins', 'stat.losses', 'stat.ot',
                'stat.pts', 'stat.goalsPerGame', 'stat.goalsAgainstPerGame', 
                'stat.powerPlayPercentage', 'stat.penaltyKillPercentage']

STANDING_STATS_WANTED = ['team.id', 'team.name', 'gamesPlayed', 'leagueRecord.wins', 'leagueRecord.losses', 
                         'leagueRecord.ot', 'points', 'regulationWins', 'row',
                         'goalsScored', 'goalsAgainst', 'goalDiff', 'streak.streakCode']

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

# TODO: Given a json data of all players within a team, get all player ids
def parse_player_ids(team_player_data):
    player_ids = []
    for k in team_player_data['data']:
        player_ids.append(k['id'])
    player_ids = pd.DataFrame(player_ids)
    return player_ids

# TODO: Given the json data for a player, filter out unwanted stats
def parse_player_stats(json_data):
    return None