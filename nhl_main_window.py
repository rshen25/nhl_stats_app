import api
import nhl_stats_db as db
from PyQt5 import QtCore, QtWidgets, QtSql
from nhl_stats_boxscore import Boxscore_Window
from functools import partial
from nhl_stats_player_info import Player_Window
from custom_table import CustomTable

class NHL_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, teams, *args, **kwargs):
        super(NHL_MainWindow, self).__init__(*args, **kwargs)
        self.dialogs = list()
        self.conn = db.create_connection('nhl_stats.db')
        self.games = api.get_current_games()
        self.teams = teams
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
        
        self.btn_goalie_details = QtWidgets.QPushButton(self.centralwidget)
        self.btn_goalie_details.setGeometry(QtCore.QRect(1030, 330, 75, 23))
        self.btn_goalie_details.setObjectName("pushButton_5")
        
        self.table_west_standings = CustomTable(self.centralwidget)
        self.table_west_standings.setGeometry(QtCore.QRect(10, 610, 581, 311))
        self.table_west_standings.setObjectName("table_west_standings")
        
        self.table_player_stats = CustomTable(self.centralwidget)
        self.table_player_stats.setGeometry(QtCore.QRect(10, 110, 1181, 221))
        self.table_player_stats.setObjectName("table_player_stats")
        
        self.table_goalie_stats = CustomTable(self.centralwidget)
        self.table_goalie_stats.setGeometry(QtCore.QRect(10, 360, 1181, 221))
        self.table_goalie_stats.setObjectName("table_goalie_stats")
        
        self.table_east_standings = CustomTable(self.centralwidget)
        self.table_east_standings.setGeometry(QtCore.QRect(610, 610, 581, 311))
        self.table_east_standings.setObjectName("table_east_standings")
        
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
        self.btn_goalie_details.clicked.connect(self.open_goalie_info)
        
        self.db.close()
        self.conn.close()

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
        self.btn_goalie_details.setText(_translate("MainWindow", "More Goalie Details"))
    
    # Creates a connection to the nhl stats database
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
                              SELECT Full_Name, Team_Abrv, Position, Games_Played,
                              Goals, Assists, Points, Plus_Minus, PIM, PPG, PPP, SHG, SHP, 
                              GWG, S, Shot_Percent, FO_Percent FROM players
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
        try:
            # Iterate through each row
            for index, row in self.games.iterrows():
                # Create a button, edit the text to be Away @ Home
                self.button = QtWidgets.QPushButton("{} @ {}".format(self.teams[row['awayID']], self.teams[row['homeID']]))
                self.button.clicked.connect(partial(self.open_boxscore, index))
                layout.addWidget(self.button)
        except AttributeError as e:
            print(e)
            
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
        self.conn = db.create_connection('nhl_stats.db')
        c = self.conn.cursor()
        
        c.execute(""" SELECT Player_ID FROM players
                  WHERE Full_Name = (?) AND Team_Abrv = (?)
                  """, (player_name, team))
        id = c.fetchone()
        id = id[0]
                
        player_career_data = api.get_player_career_stats(str(id))
        dialog = Player_Window(id, player_career_data, False)
        self.dialogs.append(dialog)
        dialog.show()
        self.conn.close()
        
    # Opens the goalie info dialog window to display more details about the goalie
    def open_goalie_info(self):
        # Get the player name
        goalie_name, team = self.get_selected_goalie()
        print(goalie_name)
        print(team)
        
        # Get the player ID from the database
        self.conn = db.create_connection('nhl_stats.db')
        c = self.conn.cursor()
        
        c.execute(""" SELECT Player_ID FROM goalies
                  WHERE Full_Name = (?) AND Team_Name = (?)
                  """, (goalie_name, team))
        id = c.fetchone()
        id = id[0]
        print(id)
                
        goalie_career_data = api.get_goalie_career_stats(str(id))
        dialog = Player_Window(id, goalie_career_data, True)
        self.dialogs.append(dialog)
        dialog.show()
        self.conn.close()
    
    # Gets the player name and the team name from the player stats table
    def get_selected_player(self):
        rows = self.table_player_stats.selectionModel().selectedRows()
        return self.table_player_stats.model().index(rows[0].row(), 0).data(), self.table_player_stats.model().index(rows[0].row(), 1).data()
    
    # Gets the goalie name and team name from the goalie stats table
    def get_selected_goalie(self):
        rows = self.table_goalie_stats.selectionModel().selectedRows()
        return self.table_goalie_stats.model().index(rows[0].row(), 0).data(), self.table_goalie_stats.model().index(rows[0].row(), 1).data()
                        
    def closeEvent(self, event):
        super(NHL_MainWindow, self).closeEvent(event)
        self.db.close()
        self.conn.close()