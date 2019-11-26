import api
import json
import csv
import pandas as pd

def jprint(json_obj):
    with open('data.json', 'w', encoding='utf-8') as outfile:
        json.dump(json_obj, outfile, ensure_ascii=False, indent=4)
    text = json.dumps(json_obj, sort_keys=True, indent=4)
    print(text)

def init_program():
    return None

# TODO: saves all the player stats?
def save_player_ids():
    all_player_ids = pd.DataFrame()
    
    #load team ids from file
#    with open('teamID.csv', 'r', encoding='utf-8-sig') as teamIds_file:
#        reader = csv.DictReader(teamIds_file, delimiter=',')
#        #teamIds = list(reader)
#        #Iterate through team IDs and get each player ID
#        for row in reader:
#            # get playerids for each team
#            result = api.get_player_ids_from_team(row['teamID'])
#            if result is None:
#                return None
#            else:
#                all_player_ids = all_player_ids.append(result)
    
    # Testing Purposes:
    result = api.get_player_ids_from_team(1)
    all_player_ids = all_player_ids.append(result)
#    playerIds = pd.DataFrame()
    print(all_player_ids)
    #iterate through all playerids
        # get the player stats via api & parser
    return all_player_ids

if __name__ == "__main__":
    #jprint(api.get_teams())
#    result = api.get_teams()
#    print(result)
#    result.to_csv('test2.csv')
    
#    metro, atlantic, central, pacific = api.get_standings()
#    metro.to_csv('metro.csv')
#    atlantic.to_csv('atlantic.csv')
#    central.to_csv('central.csv')
#    pacific.to_csv('pacific.csv')
    
    save_player_ids()
    
#    api.get_player_ids_from_team()