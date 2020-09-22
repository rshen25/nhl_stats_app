# NHL Stats App

A Python application that displays the stats of NHL players, teams, and boxscore data of NHL hockey games scheduled for the current day.
The application retrieves the data from the NHL API and utilizes SQLite for easy data retrieval and data manipulation.

<img src="https://github.com/rshen25/nhl_stats_app/blob/master/res/mainWindow.PNG" height="600" width="700"> 

# Prerequisites
Requires the following libraries to be installed if not using the executable:
- <a href=https://www.python.org/downloads/>Python 3</a>
- <a href=https://pandas.pydata.org/>Pandas</a>
- <a href=https://requests.readthedocs.io/en/master/user/install/#install>Requests</a>
- <a href=https://pypi.org/project/PyQt5/>PyQt5</a>

# Usage
Either download and run the executable here or follow the steps:
- Open a terminal in the location of `nhl_stats_app.py`
- Execute the python script with the following command `python nhl_stats_app.py`

You can view the boxscores of the current NHL games for the day by clicking on the top buttons.
It will display the score, player stats, and team stats if it is in progress.

<img src="https://github.com/rshen25/nhl_stats_app/blob/master/res/boxscore.PNG" height="500" width="500"> 

You can view more detailed player stats by clicking on a player in the player stats table or goalie stats table
and clicking on the respective more details button. Or you may search for the player's name in the text field to
the right of each table and double clicking on the desired player in the search result table after hitting the search button.
![PlayerSearch GIF](http://g.recordit.co/FSMs69esoP.gif)

<img src="https://github.com/rshen25/nhl_stats_app/blob/master/res/playerWindow.PNG" height="400" width="400"> 
