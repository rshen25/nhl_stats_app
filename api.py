# Taken and altered from: https://github.com/mhostetter/nhl

import requests
import json
import pandas as pd
import nhl_parser as parse

BASE = "https://statsapi.web.nhl.com/api/v1"
RECORDS_BASE = "https://records.nhl.com/site/api"

#
def get_conference(id):
    result = requests.get("{}/conferences/{}".format(BASE, id)).json()
    result = json.dumps(result, sort_keys=True, indent=4)
    result = pd.read_json(result)
    return result

def get_conferences():
    result = requests.get("{}/conferences/".format(BASE)).json()
    return result

def get_division(id):
    result = requests.get("{}/divisions/{}".format(BASE, id)).json()
    return result


def get_divisions():
    result = requests.get("{}/divisions/{}".format(BASE, "")).json()
    return result


def get_franchise(id):
    result = requests.get("{}/franchises/{}".format(BASE, id)).json()
    return result


def get_franchises():
    result = requests.get("{}/franchises/{}".format(BASE, "")).json()
    return result


def get_game(id):
    result = requests.get("{}/game/{}/feed/live".format(BASE, id)).json()
    return result


def get_player(id):
    result = requests.get("{}/people/{}".format(BASE, id)).json()
    return result

def get_players(ids):
    result = requests.get("{}/people/".format(BASE)).json()
    result = pd.read_json(result)
    return result

def get_team(id):
    result = requests.get("{}/teams/{}".format(BASE, id)).json()
    return result


# Gets all the teams in the NHL and their current season stats
def get_teams(ids=None):
    if isinstance(ids, list):
        suffix = ",".join(map(str, ids))
        result = requests.get("{}/teams/?teamId={}?expand=team.stats".format(BASE, suffix)).json()
        #result = json.dumps(result, sort_keys=True, indent=4)
        result = pd.read_json(path_or_buf=result, orient='records')
        return result

    else:
        #for testing purposes we will just use the file
        #result = requests.get("{}/teams/{}?expand=team.stats".format(BASE, "")).json()
        with open('data.json', 'r') as json_file:
            result = json.load(json_file)
        metro, atlantic, central, pacific = parse.parse_teams(result)
        return metro, atlantic, central, pacific
    
def get_standings():
    #response = requests.get("{}/standings".format(BASE)).json()
#    with open('standings.json', 'w') as json_file:
#        json.dump(response, json_file, sort_keys=True, indent=4)
    with open('standings.json', 'r') as json_file:
        response = json.load(json_file)
    result = parse.parse_standings(response)
    return result

# TODO: Gets the player Ids for a given team in a pandas DataFrame and writes it into a csv file
def get_player_ids_from_team(team_id):
    #print("{}/player/byTeam/{}".format(RECORDS_BASE, team_id))
    
    
    #TESTING PURPOSES -----------------------------
    with open('test_players.json', 'r') as json_file:
        response = json.load(json_file)
        print(response['data'][0]['id'])
        #response = response.json()
        result = parse.parse_player_ids(response)
        result.to_csv("resources/{}_players.csv".format(team_id))
#       json.dump(response, json_file, sort_keys=True, indent=4)
        return result
    
    #----------------------------------------------
    
#    response = requests.get("{}/player/byTeam/{}".format(RECORDS_BASE, team_id))
#    print(response.status_code)
#    if (response.status_code == 200):
#        response = response.json()
#        result = parse.parse_player_ids(response)
#        with open("{}_players.csv".format(team_id), 'w') as csv_file:
#            result.to_csv("../resources/{}".format(csv_file))
##            json.dump(response, json_file, sort_keys=True, indent=4)
#        return result
#    else:
#        return None


# TODO: Gets the stats for a player
def get_player_stats(teamId):
#    response = requests.get("{}/player/byTeam/{}".format(RECORDS_BASE, teamId)).json()
#    with open('{}.json'.format(teamId), 'w') as json_file:
#        json.dump(response, json_file, sort_keys=True, indent=4)
    return None

# TODO: Gets stats for a player year by year Modifier: ?stats=yearByYear