import pandas as pd
from pandas.io.json import json_normalize
import json

# Class to hold and parse through live NHL boxscore data
class boxscore():    
    def __init__(self, boxscore_data):
        # Get the away and home team's ID
        self.away_id = boxscore_data['gameData']['teams']['away']['id']
        self.home_id = boxscore_data['gameData']['teams']['home']['id']
                
        # Get the names of the teams
        self.away_team = boxscore_data['gameData']['teams']['away']['name']
        self.home_team = boxscore_data['gameData']['teams']['home']['name']
        
        # Get the stats of each team
        self.away_team_stats = boxscore_data['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']
        self.home_team_stats = boxscore_data['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']
        
        # Get the player stats attained by both teams within the game
        self.away_player_stats, self.home_player_stats = self.parse_player_stats(boxscore_data)
        
        # Get the goals scored within the game and their timing
        self.goals, self.goals_time = self.get_goal_descriptions(boxscore_data)
        
    # Goes through all the scoring plays within the boxscore data and returns the description
    # of each goal scored, which includes goal scorer and the assists
    def get_goal_descriptions(self, boxscore_data):
        result = []
        time_result = []
        scoring_plays = boxscore_data['liveData']['plays']['scoringPlays']
        # Get every goal scored in the game so far and its description
        for score in scoring_plays:
            result.append(boxscore_data['liveData']['plays']['allPlays'][score]['result']['description'])
            time_result.append("{}, Time: {}".format(
                    boxscore_data['liveData']['plays']['allPlays'][score]['about']['ordinalNum'],
                    boxscore_data['liveData']['plays']['allPlays'][score]['about']['periodTime']))
        return result, time_result
    
    def parse_player_stats(self, boxscore_data):
        away_player_stats = pd.DataFrame()
        home_player_stats = pd.DataFrame()
        
        if len(boxscore_data['liveData']['boxscore']['teams']['away']['players']) != 0:
            
            # Get away player stats
            for player in boxscore_data['liveData']['boxscore']['teams']['away']['players']:
                tmp = json_normalize(boxscore_data['liveData']['boxscore']['teams']['away']['players'][player])
                away_player_stats = pd.concat([tmp, away_player_stats], ignore_index=True, sort=False)
    
            # Get home player stats
            for player in boxscore_data['liveData']['boxscore']['teams']['home']['players']:
                tmp = json_normalize(boxscore_data['liveData']['boxscore']['teams']['home']['players'][player])
                home_player_stats = pd.concat([tmp, home_player_stats], ignore_index=True, sort=False)
        
            # list of what stats we want
            stats_wanted = ['person.fullName', 'jerseyNumber', 'person.shootsCatches', 'position.abbreviation',
                            'stats.skaterStats.goals', 'stats.skaterStats.assists', 'stats.skaterStats.plusMinus', 
                            'stats.skaterStats.timeOnIce', 'stats.skaterStats.shots', 'stats.skaterStats.hits', 
                            'stats.skaterStats.powerPlayGoals', 'stats.skaterStats.powerPlayAssists', 
                            'stats.skaterStats.penaltyMinutes', 'stats.skaterStats.takeaways', 'stats.skaterStats.giveaways', 
                            'stats.skaterStats.faceoffTaken', 'stats.skaterStats.faceOffPct', 'stats.skaterStats.shortHandedGoals', 
                            'stats.skaterStats.shortHandedAssists', 'stats.skaterStats.blocked', 
                            'stats.goalieStats.timeOnIce', 'stats.goalieStats.saves', 'stats.goalieStats.savePercentage',
                            'stats.goalieStats.goals', 'stats.goalieStats.assists',
                            'stats.goalieStats.pim']
            try:
                away_player_stats = away_player_stats[stats_wanted].copy()
                home_player_stats = home_player_stats[stats_wanted].copy()
                
                stats_renamed = ['Name', 'Number', 'Handed', 'Pos', 'G', 'A', '+/-', 'TOI', 'Shots',
                                 'Hits', 'PPG', 'PPA', 'PIM', 'Takeaways', 'Giveaways', 'FO', 'FO%', 'SHG', 'SHA', 'Blocks', 'Goalie_TOI', 
                                 'Goalie_Saves', 'Goalie_Save%', 'Goalie_Goals', 'Goalie_Assists', 'Goalie_PIM']
            
            # If there is an error (typically it's because the game has not started and so there are missing key values)
            except KeyError as e:
                # If it is because the game has not started, then remove the key values that are missing and try again
                try:
                    stats_wanted = ['person.fullName', 'jerseyNumber', 'person.shootsCatches', 'position.abbreviation',
                    'stats.skaterStats.goals', 'stats.skaterStats.assists', 'stats.skaterStats.plusMinus', 
                    'stats.skaterStats.timeOnIce', 'stats.skaterStats.shots', 'stats.skaterStats.hits', 
                    'stats.skaterStats.powerPlayGoals', 'stats.skaterStats.powerPlayAssists', 
                    'stats.skaterStats.penaltyMinutes', 'stats.skaterStats.takeaways', 'stats.skaterStats.giveaways', 
                    'stats.skaterStats.faceoffTaken', 'stats.skaterStats.shortHandedGoals', 
                    'stats.skaterStats.shortHandedAssists', 'stats.skaterStats.blocked', 
                    'stats.goalieStats.timeOnIce', 'stats.goalieStats.saves',
                    'stats.goalieStats.goals', 'stats.goalieStats.assists',
                    'stats.goalieStats.pim']
                    
                    away_player_stats = away_player_stats[stats_wanted].copy()
                    home_player_stats = home_player_stats[stats_wanted].copy()
                    
                    stats_renamed = ['Name', 'Number', 'Handed', 'Pos', 'G', 'A', '+/-', 'TOI', 'Shots',
                                     'Hits', 'PPG', 'PPA', 'PIM', 'Takeaways', 'Giveaways', 'FO', 'SHG', 'SHA', 'Blocks', 'Goalie_TOI', 
                                     'Goalie_Saves', 'Goalie_Goals', 'Goalie_Assists', 'Goalie_PIM']
                    
                except KeyError as e:
                    print(e)
                print(e)
                
        away_player_stats.columns = stats_renamed
        home_player_stats.columns = stats_renamed
        
        away_player_stats = away_player_stats.sort_values(by=['G', 'A'], ascending=False)
        home_player_stats = home_player_stats.sort_values(by=['G', 'A'], ascending=False)
        
        away_player_stats = away_player_stats.fillna('')
        home_player_stats = home_player_stats.fillna('')
        
        return away_player_stats, home_player_stats
    
    def get_away_score(self):
        return self.away_team_stats['goals']
    
    def get_home_score(self):
        return self.home_team_stats['goals']
        
    def get_goals(self):
        result = list()
        for index, goal in enumerate(self.goals):
            result.append(self.goals_time[index] + " " + goal)
        return result
            
#if __name__ == "__main__":
#    # for testing
#    with open('live.json', 'r') as boxscore_file:
#        boxscore_data = json.load(boxscore_file)
#    boxscore_ = boxscore(boxscore_data)
#    for index, goals in enumerate(boxscore_.goals):
#        print(goals + " " + boxscore_.goals_time[index])
#        
#    for k in boxscore_.get_away_team_stats():
#        print(k + " : " + boxscore_.get_away_team_stats()[k])
    
    