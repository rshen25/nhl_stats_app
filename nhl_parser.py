import pandas as pd
import nhl_parse_const as pc
from pandas.io.json import json_normalize


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
    team_stats = team_stats[pc.TEAM_STATS_WANTED].copy()
    
    # Rename the columns
    team_stats.columns = pc.TEAM_STATS_RENAMED
    
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
    metro = metro[pc.STANDING_STATS_WANTED].copy()
    atlantic = calculate_goal_difference(atlantic)
    atlantic = atlantic[pc.STANDING_STATS_WANTED].copy()
    central = calculate_goal_difference(central)
    central = central[pc.STANDING_STATS_WANTED].copy()
    pacific = calculate_goal_difference(pacific)
    pacific = pacific[pc.STANDING_STATS_WANTED].copy()
    
    # Rename the columns to math the database
    metro.columns = pc.STANDINGS_STATS_RENAMED
    atlantic.columns = pc.STANDINGS_STATS_RENAMED
    central.columns = pc.STANDINGS_STATS_RENAMED
    pacific.columns = pc.STANDINGS_STATS_RENAMED
    
    result = pd.concat([metro, atlantic, central, pacific], ignore_index=True)
    
    return result

def calculate_goal_difference(df):
    df['goalDiff'] = df['goalsScored'] - df['goalsAgainst']
    return df

# Parses the json data of the given NHL standings
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

# Parses the player data from the NHL API and filters out unwanted data and only leaves
# the desired data as described in PLAYER_DATA_WANTED
def parse_player_data(player_data):
    result = json_normalize(player_data['people'])
    
    try:
        result = result[pc.PLAYER_DATA_WANTED]
        result.columns = pc.PLAYER_DATA_RENAMED
        
    except KeyError as e:
        print(e)
        return None
    
    return result

# Parses the player data from the NHL API and filters out unwanted data and only leaves
# the desired data as described in STAT_LEADER_WANTED
def parse_stat_leaders(data):
    try:
        result = json_normalize(data['data'])
        
        result = result[pc.STAT_LEADER_WANTED].copy()        
        result.columns = pc.STAT_LEADER_RENAMED
        
    except KeyError as e:
        print(e)
        return None
    
    return result

# Parses the player data from the NHL API and filters out unwanted data and only leaves
# the desired data as described in GOALIE_LEADER_WANTED
def parse_goalie_leader_stats(goalie_data):
    try:
        result = json_normalize(goalie_data['data'])
        
        result = result[pc.GOALIE_LEADER_WANTED].copy()        
        result.columns = pc.GOALIE_LEADER_RENAMED
        
    except KeyError as e:
        print(e)
        return None
    return result

# Parses the player career data from the NHL API and filters out unwanted data and only leaves
# the desired data as described in PLAYER_DATA_WANTED
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

# Parses the gaolie career stats from the NHL API and filters out unwanted data and only leaves
# the desired data as described in GOALIE_STATS_WANTED
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

# Parses the game log json data from the NHL API
def parse_game_log(game_log):
    result = json_normalize(game_log['stats'][0]['splits'])
    
    result = result[pc.PLAYER_GAME_LOG_STATS].copy()
    result.columns = pc.PLAYER_GAME_LOG_RENAMED
        
    return result

# Parses the goalie game log json data from the NHL API
def parse_goalie_game_log(game_log):
    result = json_normalize(game_log['stats'][0]['splits'])
        
    result = result[pc.GOALIE_GAME_LOG_STATS].copy()
    result.columns = pc.GOALIE_GAME_LOG_RENAMED
        
    return result