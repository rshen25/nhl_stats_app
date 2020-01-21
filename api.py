# Taken and altered from: https://github.com/mhostetter/nhl

import requests
import json
import pandas as pd
import boxscore as bs
import nhl_parser as parse

BASE = "https://statsapi.web.nhl.com/api/v1"
RECORDS_BASE = "https://records.nhl.com/site/api"

STAT_LEADERS_BASE = "https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D%5D"

def get_players(ids):
    result = requests.get("{}/people/".format(BASE)).json()
#    result = pd.read_json(result)
    return result

def get_team(id):
    result = requests.get("{}/teams/{}".format(BASE, id)).json()
    return result
    
def get_all_team_stats():
        result = requests.get("{}/teams/?expand=team.stats".format(BASE)).json()
        result = parse.parse_teams(result)
        return result
    
def get_standings():
    # https://statsapi.web.nhl.com/api/v1/teams/?expand=team.stats
    response = requests.get("{}/standings".format(BASE))
    if response.status_code == 200:
        response = response.json()
        result = parse.parse_standings(response)
    
    # TESTING --------------------------
#    with open('standings.json', 'r') as json_file:
#        response = json.load(json_file)
#        result = parse.parse_standings(response)
    # -------------------------------------
        return result

# Gets the player Ids and their name for a given team in a pandas DataFrame and writes it into a csv file
def get_player_ids_from_team(team_id):    
    
    #TESTING PURPOSES -----------------------------
#    with open('test_roster.json', 'r') as json_file:
#        response = json.load(json_file)
#        #print(response['data'][0]['id'])
#        #response = response.json()
#        result = parse.parse_player_ids(response)
#        result.to_csv("test_players.csv".format(team_id))
#       json.dump(response, json_file, sort_keys=True, indent=4)
#        return result
    
    #----------------------------------------------
    
    response = requests.get("{}/teams/{}/roster".format(BASE, team_id))
#    print(response.status_code)
    if (response.status_code == 200):
        response = response.json()
        result = parse.parse_player_ids(response)
        return result
    else:
        return None
    
    
#    response = requests.get("{}/player/byTeam/{}".format(RECORDS_BASE, team_id))
#    print(response.status_code)
#    if (response.status_code == 200):
#        response = response.json()
#        result = parse.parse_player_ids(response)
#        result.to_csv("resources/player_ids/{}_players.csv".format(team_id))
#        return result
#    else:
#        return None


# Gets the stats for a player via the NHL API, parses it so that it contains desired statistics
# and returns in a pandas DataFrame
def get_player_stats(player_id, season):
    
    response = requests.get("{}/people/{}".format(BASE, player_id))
    if response.status_code == 200:
        player_data = response.json()
    
    response = requests.get("{}/people/{}/stats?stats=statsSingleSeason&season={}".format(BASE, player_id, season))
#    print(response.status_code)
    if response.status_code == 200:
        player_stats = response.json()
        # Parse the data to include only stats that we want
        result, isGoalie = parse.parse_player_stats(player_data, player_stats)
    return result, isGoalie
    
    # TESTING ----------------------------
#    with open('test_player_data.json', 'r') as data_file:
#        player_data = json.load(data_file)
#        
#    with open('test_player_stats.json', 'r') as stats_file:
#        player_stats = json.load(stats_file)
#        
#    result = parse.parse_player_stats(player_data, player_stats)
#    return result
    
    # ------------------------------------
    
# Gets the career stats for a player via the NHL API, parses it so that it contains desired statistics
# and returns in a pandas DataFrame
def get_player_career_stats(player_id):    
    response = requests.get("{}/people/{}/stats?stats=yearByYear".format(BASE, player_id))
    print(response.status_code)
    if response.status_code == 200:
        player_stats = response.json()
        # Parse the data to include only stats that we want
        result = parse.parse_player_career_stats(player_stats)
    return result

# Gets the career stats for a goalie via the NHL API, parses it so that it contains desired statistics
# and returns in a pandas DataFrame
def get_goalie_career_stats(player_id):
    response = requests.get("{}/people/{}/stats?stats=yearByYear".format(BASE, player_id))
    print(response.status_code)
    if response.status_code == 200:
        player_stats = response.json()
        # Parse the data to include only stats that we want
        result = parse.parse_goalie_career_stats(player_stats)
    return result

# Requests for the current scheduled NHL games for the day and returns it in a pandas DataFrame format
def get_current_games():
    response = requests.get("{}/schedule".format(BASE))
    if response.status_code == 200:
        game_data = response.json()
        if game_data['totalGames'] > 0:
            result = parse.parse_games(game_data)
            return result
        else:
            return None
    else:
        return None

# Requests the current NHL game data for a given game ID and returns a parsed boxscore object that stores the relevant data
def get_live_game_feed(id):
    response = requests.get("{}/game/{}/feed/live".format(BASE, id))
    if response.status_code == 200:
        game_data = response.json()
        result = bs.boxscore(game_data)
        return result
    else:
        return None


def get_stat_leaders(season, page):
    
    # Testing ------------------------------------
#    with open('summary.json', 'r') as data_file:
#        data = json.load(data_file)
#        result = parse.parse_stat_leaders(data)
#    
#    return result
    # --------------------------------------------
    
    response = requests.get(
            "{}&start={}&limit=100&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C={}%20and%20seasonId%3E={}"
            .format(STAT_LEADERS_BASE, page * 100, season, season))
    
    if response.status_code == 200:
        data = response.json()
        result = parse.parse_stat_leaders(data)
        return result
    else:    
        return None
    

# Requests the NHL api to get the player stats in json form
# input - a pandas dataframe of the player ids
# output - two dataframes, one for players, the other for goalies
#def get_all_player_season_stats(player_ids, season):
#    player_data_response = list()
#    player_stats_response = list()
#    for id in player_ids.itertuples():
#        response = requests.get("{}/people/{}/stats?stats=statsSingleSeason&season={}".format(BASE, id[0], season))
#        
#        if response.status_code == 200:
#            player_stats_response.append(response.json())
#            
#        response = response = requests.get("{}/people/{}".format(BASE, id[0]))
#        if response.status_code == 200:
#            player_data_response.append(response.json())
#        
#            
#    player_stats = None
#    goalie_stats = None
#    
#    if len(player_data_response) > 0 and len(player_stats_response) > 0:
#        player_stats, goalie_stats = parse.parse_all_player_stats(player_data_response, player_stats_response)
#    
#    return player_stats, goalie_stats