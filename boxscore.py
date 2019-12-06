import pandas as pd
from pandas.io.json import json_normalize
import json

# Class to hold and parse through live NHL boxscore data
class boxscore():    
    def __init__(self, awayID, homeID, boxscore_data):
        self.away_id = awayID
        self.away_player_stats = []
        
        self.home_id = homeID
        self.home_player_stats = []
                
        self.away_team = boxscore_data['gameData']['teams']['away']['name']
        self.home_team = boxscore_data['gameData']['teams']['home']['name']
        
        self.away_team_stats = boxscore_data['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']
        self.home_team_stats = boxscore_data['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']
        
#        away_player_stats, home_player_stats = self.parse_player_stats(boxscore_data)
        
        self.goals, self.goals_time = self.get_goal_descriptions(boxscore_data)
        
    # Goes through all the scoring plays within the boxscore data and returns the description
    # of each goal scored, which includes goal scorer and the assists
    def get_goal_descriptions(self, boxscore_data):
        result = []
        time_result = []
        scoring_plays = boxscore_data['liveData']['plays']['scoringPlays']
        for score in scoring_plays:
            result.append(boxscore_data['liveData']['plays']['allPlays'][score]['result']['description'])
            time_result.append("{}, Time: {}".format(
                    boxscore_data['liveData']['plays']['allPlays'][score]['about']['ordinalNum'],
                    boxscore_data['liveData']['plays']['allPlays'][score]['about']['periodTime']))
        return result, time_result
    
    def parse_player_stats(self, boxscore_data):
        away_player_stats = pd.DataFrame()
        home_player_stats = pd.DataFrame()
        
        # Get away player stats
        for player in boxscore_data['liveData']['boxscore']['teams']['away']['players']:
            tmp = json_normalize(boxscore_data['liveData']['boxscore']['teams']['away']['players'][player])
            away_player_stats = pd.concat([tmp, away_player_stats], ignore_index=True, sort=False)

        # Get home player stats
        for player in boxscore_data['liveData']['boxscore']['teams']['home']['players']:
            tmp = json_normalize(boxscore_data['liveData']['boxscore']['teams']['home']['players'][player])
            home_player_stats = pd.concat([tmp, home_player_stats], ignore_index=True, sort=False)
        
        home_player_stats.to_csv('home_player_stats.csv')
        away_player_stats.to_csv('away_player_stats.csv')
        
        return away_player_stats, home_player_stats
            
# Taken from https://stackoverflow.com/questions/31475965/fastest-way-to-populate-qtableview-from-pandas-data-frame
#class PandasModel(QtCore.QAbstractTableModel):
#    def __init__(self, data, parent=None):
#        QtCore.QAbstractTableModel.__init__(self, parent)
#        self._data = data
#
#    def rowCount(self, parent=None):
#        return len(self._data.values)
#
#    def columnCount(self, parent=None):
#        return self._data.columns.size
#
#    def data(self, index, role=Qt.DisplayRole):
#        if index.isValid():
#            if role == Qt.DisplayRole:
#                return QtCore.QVariant(str(
#                    self._data.values[index.row()][index.column()]))
#        return QtCore.QVariant()

if __name__ == "__main__":
    # for testing
    with open('live.json', 'r') as boxscore_file:
        boxscore_data = json.load(boxscore_file)
    boxscore_ = boxscore(0, 0, boxscore_data)
    for index, goals in enumerate(boxscore_.goals):
        print(goals + " " + boxscore_.goals_time[index])
    
    