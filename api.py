# Taken and altered from: https://github.com/mhostetter/nhl

import requests
import boxscore as bs
import nhl_parser as parse

BASE = "https://statsapi.web.nhl.com/api/v1"
RECORDS_BASE = "https://records.nhl.com/site/api"

STAT_LEADERS_BASE = "https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D%5D"
GOALIE_STATS_BASE = "https://api.nhle.com/stats/rest/en/goalie/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22wins%22,%22direction%22:%22DESC%22%7D%5D"

def get_players(ids):
    result = requests.get("{}/people/".format(BASE)).json()
    return result

def get_team(id):
    result = requests.get("{}/teams/{}".format(BASE, id)).json()
    return result
    
def get_all_team_stats():
        result = requests.get("{}/teams/?expand=team.stats".format(BASE)).json()
        result = parse.parse_teams(result)
        return result
    
def get_standings():
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
        result = parse.parse_player_stats(player_data, player_stats)
    return result
    
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

# Gets the player data via the NHL API, parses it and returns it in a pandas dataframe
def get_player_data(player_id):
    response = requests.get("{}/people/{}".format(BASE, player_id))
    if response.status_code == 200:
        player_data = response.json()
        result = parse.parse_player_data(player_data)
        
    return result

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

# Gets the point leaders of all active players within the NHL
def get_stat_leaders(season, page): 
    response = requests.get(
            "{}&start={}&limit=100&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C={}%20and%20seasonId%3E={}"
            .format(STAT_LEADERS_BASE, page * 100, season, season))
    
    if response.status_code == 200:
        data = response.json()
        result = parse.parse_stat_leaders(data)
        return result
    else:    
        return None

# Gets the goalie leaders from the NHL API as displayed on the NHL goalie leaderboards webpage
def get_goalie_stats(season):
    response = requests.get("{}&start=0&limit=81&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C={}%20and%20seasonId%3E={}"
                            .format(GOALIE_STATS_BASE, season, season))
    if response.status_code == 200:
        goalie_data = response.json()
        result = parse.parse_goalie_leader_stats(goalie_data)
        return result
    else:
        return None

# Gets the game log for a given season and player via the NHL API, returns it as a pandas DataFrame
def get_game_log(player_id, season):
    response = requests.get("{}/people/{}/stats?stats=gameLog&season={}".format(BASE, player_id, season))
    if response.status_code == 200:
        game_log = response.json()
        result = parse.parse_game_log(game_log)
        return result
    else:
        return None
    
# Gets the game log for a given season and goalie via the NHL API, returns it as a pandas DataFrame
def get_goalie_game_log(player_id, season):
    response = requests.get("{}/people/{}/stats?stats=gameLog&season={}".format(BASE, player_id, season))
    if response.status_code == 200:
        game_log = response.json()
        result = parse.parse_goalie_game_log(game_log)
        return result
    else:
        return None