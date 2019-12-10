import api
import csv
import pandas as pd
import sys
import nhl_stats_db as db
from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
from nhl_stats_boxscore import Boxscore_Window
from functools import partial
from nhl_stats_player_info import Player_Window
from custom_table import CustomTable

class NHL_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(NHL_MainWindow, self).__init__(*args, **kwargs)
        self.dialogs = list()
        self.conn = db.create_connection('nhl_stats.db')
        self.games = api.get_current_games()
        self.setupUi()
        
    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1198, 968)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label_standings = QtWidgets.QLabel(self.centralwidget)
        self.label_standings.setGeometry(QtCore.QRect(10, 580, 47, 13))
        self.label_standings.setObjectName("label_standings")
        self.label_west_conference = QtWidgets.QLabel(self.centralwidget)
        self.label_west_conference.setGeometry(QtCore.QRect(20, 590, 121, 16))
        self.label_west_conference.setObjectName("label_west_conference")
        self.label_east_conference = QtWidgets.QLabel(self.centralwidget)
        self.label_east_conference.setGeometry(QtCore.QRect(610, 590, 121, 16))
        self.label_east_conference.setObjectName("label_east_conference")
        self.label_player_stats = QtWidgets.QLabel(self.centralwidget)
        self.label_player_stats.setGeometry(QtCore.QRect(10, 90, 81, 16))
        self.label_player_stats.setObjectName("label_player_stats")
        self.label_games = QtWidgets.QLabel(self.centralwidget)
        self.label_games.setGeometry(QtCore.QRect(560, 0, 47, 13))
        self.label_games.setObjectName("label_games")
        self.label_goalie_stats = QtWidgets.QLabel(self.centralwidget)
        self.label_goalie_stats.setGeometry(QtCore.QRect(20, 340, 81, 16))
        self.label_goalie_stats.setObjectName("label_goalie_stats")
        self.btn_update_player_stats = QtWidgets.QPushButton(self.centralwidget)
        self.btn_update_player_stats.setGeometry(QtCore.QRect(70, 90, 75, 23))
        self.btn_update_player_stats.setObjectName("btn_update_player_stats")
        self.btn_update_goalie_stats = QtWidgets.QPushButton(self.centralwidget)
        self.btn_update_goalie_stats.setGeometry(QtCore.QRect(90, 340, 75, 23))
        self.btn_update_goalie_stats.setObjectName("btn_update_goalie_stats")
        self.btn_update_standings = QtWidgets.QPushButton(self.centralwidget)
        self.btn_update_standings.setGeometry(QtCore.QRect(130, 580, 75, 23))
        self.btn_update_standings.setObjectName("btn_update_standings")
        self.btn_player_details = QtWidgets.QPushButton(self.centralwidget)
        self.btn_player_details.setGeometry(QtCore.QRect(1110, 330, 75, 23))
        self.btn_player_details.setObjectName("pushButton_4")
        
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(1030, 330, 75, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        
        self.table_west_standings = CustomTable(self.centralwidget)
        self.table_west_standings.setGeometry(QtCore.QRect(10, 610, 581, 311))
        self.table_west_standings.setObjectName("table_west_standings")
#        self.table_west_standings.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        
        self.table_player_stats = CustomTable(self.centralwidget)
        self.table_player_stats.setGeometry(QtCore.QRect(10, 110, 1181, 221))
        self.table_player_stats.setObjectName("table_player_stats")
#        self.table_player_stats.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        
        self.table_goalie_stats = CustomTable(self.centralwidget)
        self.table_goalie_stats.setGeometry(QtCore.QRect(10, 360, 1181, 221))
        self.table_goalie_stats.setObjectName("table_goalie_stats")
#        self.table_goalie_stats.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        
        self.table_east_standings = CustomTable(self.centralwidget)
        self.table_east_standings.setGeometry(QtCore.QRect(610, 610, 581, 311))
        self.table_east_standings.setObjectName("table_east_standings")
#        self.table_east_standings.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 1181, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.gamesLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.gamesLayout.setContentsMargins(0, 0, 0, 0)
        self.gamesLayout.setObjectName("gamesLayout")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1198, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        
        self.db = self.create_connection()
        
        self.set_standings_table(self.table_west_standings, self.table_east_standings)
                
        self.set_player_stats_table(self.table_player_stats)
        self.set_goalie_stats_table(self.table_goalie_stats)
                
        self.create_current_games_buttons(self.gamesLayout)              
        
        # Set up the more player details button
        self.btn_player_details.clicked.connect(self.open_player_info)
        
        self.db.close()
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_standings.setText(_translate("MainWindow", "Standings"))
        self.label_west_conference.setText(_translate("MainWindow", "Western Conference"))
        self.label_east_conference.setText(_translate("MainWindow", "Eastern Conference"))
        self.label_player_stats.setText(_translate("MainWindow", "Player Stats"))
        self.label_games.setText(_translate("MainWindow", "Games"))
        self.label_goalie_stats.setText(_translate("MainWindow", "Goalies Stats"))
        self.btn_update_player_stats.setText(_translate("MainWindow", "Update"))
        self.btn_update_goalie_stats.setText(_translate("MainWindow", "Update"))
        self.btn_update_standings.setText(_translate("MainWindow", "Update"))
        self.btn_player_details.setText(_translate("MainWindow", "More Player Details"))
        self.pushButton_5.setText(_translate("MainWindow", "PushButton"))
        

    def create_connection(self):
        db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("nhl_stats.db")
        if not db.open():
            QtWidgets.QMessageBox.critical(None, "Cannot open database",
                             "Unable to establish a database connection.\n"
                             "This example needs SQLite support. Please read "
                             "the Qt SQL driver documentation for information how "
                             "to build it.\n\n"
                             "Click Cancel to exit.", QtWidgets.QMessageBox.Cancel)
            return False
        
        return db

    # Sets the database to the standings table
    def set_standings_table(self, table_west_standings, table_east_standings):
        # Set the western conference standings table
        west_model = QtSql.QSqlQueryModel()
        west_model.setQuery("""
                            SELECT Team_Name, Games_Played, Wins, Losses, OT, Points,
                            GPG, GAPG, PP_Percent, PK_Percent, Division, Regulation_Wins, ROW,
                            Goals_Scored, Goals_Against, Goal_Diff, Streak FROM teams 
                            WHERE Conference = 'Western'
                            ORDER BY Points DESC
                            """)
        
        table_west_standings.setModel(west_model)
        
        # Set the eastern conference standings table
        east_model = QtSql.QSqlQueryModel()
        east_model.setQuery("""
                            SELECT Team_Name, Games_Played, Wins, Losses, OT, Points,
                            GPG, GAPG, PP_Percent, PK_Percent, Division, Regulation_Wins, ROW,
                            Goals_Scored, Goals_Against, Goal_Diff, Streak 
                            FROM teams WHERE Conference = 'Eastern'
                            ORDER BY Points DESC
                            """)
        table_east_standings.setModel(east_model)
        

    # Sets the database to the player stats table to enable queries to db
    def set_player_stats_table(self, table_player_stats):
        # Set the western conference standings table
        player_model = QtSql.QSqlQueryModel()
        player_model.setQuery("""
                              SELECT Full_Name, Team_Name, Position, Games_Played, 
                              Goals, Assists, Points, Plus_Minus, PIM, PPG, PPP, SHG,
                              SHP, GWG, OTG, S, Shot_Percent, Blk, FO_Percent, Hits FROM players
                              ORDER BY Points DESC
                              """)
        
        table_player_stats.setModel(player_model)
            
    # Set the goalie stats table with the database
    def set_goalie_stats_table(self, table_goalie_stats):
        # Set the eastern conference standings table
        goalie_model = QtSql.QSqlQueryModel()
        goalie_model.setQuery("""
                              SELECT Full_Name, Team_Name, Age, Height, Weight, Country,
                              Number, Position, Games_Played, Games_Started, Wins, Losses,
                              OT, Shutouts, Saves, Save_Percentage, GAA, GA, SA FROM goalies
                              ORDER BY Wins DESC
                              """)
        table_goalie_stats.setModel(goalie_model)
            
    # Creates buttons for each current nhl games for the day
    def create_current_games_buttons(self, layout: QtWidgets.QHBoxLayout):
        # Iterate through each row
        for index, row in self.games.iterrows():
            # Create a button, edit the text to be Away @ Home
            # TODO: reminder to change it to team abbreviations
            self.button = QtWidgets.QPushButton("{} @ {}".format(row['awayID'], row['homeID']))
            self.button.clicked.connect(partial(self.open_boxscore, index))
            layout.addWidget(self.button)
            
    def open_boxscore(self, index):
        boxscore_data = api.get_live_game_feed(self.games.iloc[index]['gameID'])
        dialog = Boxscore_Window(boxscore_data)
        self.dialogs.append(dialog)
        dialog.show()
        
    # Opens the player info dialog window to display more details about a specific player
    def open_player_info(self):
        # Get the player name
        player_name, team = self.get_selected_player()
        
        # Get the player ID from the database
        c = self.conn.cursor()
        
        c.execute(""" SELECT Player_ID FROM players
                  WHERE Full_Name = (?) AND Team_Name = (?)
                  """, (player_name, team))
        id = c.fetchone()
        id = id[0]
        
#        c.execute(""" SELECT Full_Name, Team_Name, Position, Games_Played, 
#                  Goals, Assists, Points, Plus_Minus, PIM, PPG, PPP, SHG,
#                  SHP, GWG, OTG, S, Shot_Percent, Blk, FO_Percent, Hits 
#                  FROM players WHERE Player_ID = (?) """, (id,))
#        
#        player_data = c.fetchone()
#        print(player_data)
        
        player_career_data = api.get_player_career_stats(str(id))
        dialog = Player_Window(id, player_career_data)
#        dialog = Player_Window(player_career_data)
        self.dialogs.append(dialog)
        dialog.show()
    
    def get_selected_player(self):
        rows = self.table_player_stats.selectionModel().selectedRows()
#        print(self.table_player_stats.model().index(rows[0].row(), 0).data())
        return self.table_player_stats.model().index(rows[0].row(), 0).data(), self.table_player_stats.model().index(rows[0].row(), 1).data()
                        
    def closeEvent(self, event):
        super(NHL_MainWindow, self).closeEvent(event)
        self.db.close()
        


# Load team ids on init
teams = {}

PLAYER_STATS_RENAMED = ['Player_ID', 'Full_Name', 'Team_ID', 'Team_Name', 'Age', 'Height',
                        'Weight', 'Country', 'Number', 'Shoots', 'Position', 'Games_Played',
                        'Goals', 'Assists', 'Points', 'Plus_Minus', 'PIM', 'PPG', 'PPP', 'SHG', 'SHP', 
                        'GWG', 'OTG', 'S' , 'Shot_Percent', 'Blk', 'FO_Percent', 'Hits']

GOALIE_STATS_RENAMED = ['Player_ID', 'Full_Name', 'Team_ID', 'Team_Name', 'Age', 'Height',
                        'Weight', 'Country', 'Number', 'Catches', 'Position', 'Games_Played',
                        'Games_Started', 'Wins', 'Losses', 'OT', 'Shutouts', 'Saves', 'Save_Percentage',
                        'GAA', 'GA', 'SA']

def init_program():    
    print(teams)


# Saves all player ids for every team
def get_and_save_player_ids():
    all_player_ids = pd.DataFrame()
    for id in teams.keys():
        # get playerids for each team
        result = api.get_player_ids_from_team(id)
        if result is None:
            return None
        else:
            all_player_ids = all_player_ids.append(result)
    
    # Testing Purposes:
#    result = api.get_player_ids_from_team(11)
#    if result is None:
#        return None
#    else:
#        all_player_ids = all_player_ids.append(result)
    
#    playerIds = pd.DataFrame()

    #iterate through all playerids
        # get the player stats via api & parser

# Makes a request to get all the teams stats and adds it to the database
def get_team_stats():
    conn = db.create_connection('nhl_stats.db')
    # Request team and standing stats
    team_stats = api.get_all_team_stats()
    team_standings = api.get_standings()
    
    # Join the stats and standings table into one
    team_stats = team_stats.merge(team_standings, on=['Team_ID', 'Team_Name'])
        
    # Update the database
    team_stats.to_sql('teams', conn, if_exists='replace', index=False)
    conn.close()
    return team_stats
    
# Takes in a list of player ids and requests their stats from the NHL API and 
# returns their player statistics for the current season in a pandas DataFrame
def get_player_stats():
    conn = db.create_connection('nhl_stats.db')
    # Iterate through all player ids
    with open("resources/player_ids/1_players.csv".format(id), 'r', encoding='utf-8-sig') as player_ids_file:
        reader = csv.DictReader(player_ids_file, delimiter=',')
        goalies = pd.DataFrame()
        players = pd.DataFrame()
        for player_id in reader:
        # Request player stat from NHL API
#            print(player_id['0'])
            result, isGoalie = api.get_player_stats(player_id['0'], '20192020')
            
            # Insert data into players database table
            if (isGoalie):
#                result = result.to_sql('tmp_goalies', con=conn, if_exists='append', index=False)
                goalies = pd.concat([result, goalies], ignore_index=True)
            else:
#                result = result.to_sql('tmp_players', con=conn, if_exists='append', index=False)
                players = pd.concat([result, players], ignore_index=True)
        
        goalies.to_sql('tmp_goalies', con=conn, if_exists='append', index=False)
        players.to_sql('tmp_players', con=conn, if_exists='append', index=False)
        c = conn.cursor()
            
        c.execute("SELECT * FROM tmp_goalies")
        rows = c.fetchall()
        for row in rows:
            conn.execute("""
                         REPLACE INTO goalies({})
                         VALUES (?, ?, ?, ?, ? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,?)
                         """.format(','.join(GOALIE_STATS_RENAMED)),
                         row)
            
        c.execute("SELECT * FROM tmp_players")
        rows = c.fetchall()
        for row in rows:
            conn.execute("""
                         REPLACE INTO players({})
                         VALUES (?, ?, ?, ?, ? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,?, ?, ?, ?, ?)
                         """.format(','.join(PLAYER_STATS_RENAMED)),
                         row)
        conn.close()


def create_teams_dict():
    conn = db.create_connection('nhl_stats.db')
    c = conn.cursor()
    c.execute("SELECT Team_ID, Abbreviation FROM teams")
    rows = c.fetchall()
    for row in rows:
        teams[row[0]] = row[1]
    conn.close()
    
    
if __name__ == "__main__":
    # Create a connection to the database
    conn = db.create_connection('nhl_stats.db')
    
    if conn is not None:
        # Create the team and player tables
        db.create_teams_table(conn)
        db.create_players_table(conn)
        db.create_goalies_table(conn)
    conn.close()
    
#    get_team_stats()
    create_teams_dict()
    
#    c = conn.cursor()

#    get_player_stats(conn)

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = NHL_MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
    