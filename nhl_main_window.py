import api
import nhl_stats_db as db
import nhl_stats_app as main
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
                
        # Player stats
        self.label_player_stats = QtWidgets.QLabel(self.centralwidget)
        self.label_player_stats.setGeometry(QtCore.QRect(10, 70, 81, 16))
        self.label_player_stats.setObjectName("label_player_stats")
                        
        self.btn_update_player_stats = QtWidgets.QPushButton(self.centralwidget)
        self.btn_update_player_stats.setGeometry(QtCore.QRect(890, 290, 75, 23))
        self.btn_update_player_stats.setObjectName("btn_update_player_stats")
        
        self.table_player_stats = CustomTable(self.centralwidget)
        self.table_player_stats.setGeometry(QtCore.QRect(10, 90, 871, 221))
        self.table_player_stats.setObjectName("table_player_stats")
                
        self.btn_more_player_info = QtWidgets.QPushButton(self.centralwidget)
        self.btn_more_player_info.setGeometry(QtCore.QRect(890, 260, 75, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_more_player_info.sizePolicy().hasHeightForWidth())
        self.btn_more_player_info.setSizePolicy(sizePolicy)
        self.btn_more_player_info.setObjectName("btn_more_player_info")
                
        # Player Search
        self.line_edit_player_search = QtWidgets.QLineEdit(self.centralwidget)
        self.line_edit_player_search.setGeometry(QtCore.QRect(890, 90, 191, 31))
        self.line_edit_player_search.setObjectName("line_edit_player_search")
        
        self.btn_player_search = QtWidgets.QPushButton(self.centralwidget)
        self.btn_player_search.setGeometry(QtCore.QRect(1090, 90, 81, 31))
        self.btn_player_search.setObjectName("btn_player_search")
        
        self.table_player_search_result = CustomTable(self.centralwidget)
        self.table_player_search_result.setGeometry(QtCore.QRect(890, 130, 291, 121))
        self.table_player_search_result.setObjectName("table_player_search_result")
        
        # Goalie stats
        self.label_goalie_stats = QtWidgets.QLabel(self.centralwidget)
        self.label_goalie_stats.setGeometry(QtCore.QRect(20, 320, 81, 16))
        self.label_goalie_stats.setObjectName("label_goalie_stats")
        
        self.table_goalie_stats = CustomTable(self.centralwidget)
        self.table_goalie_stats.setGeometry(QtCore.QRect(10, 340, 871, 221))
        self.table_goalie_stats.setObjectName("table_goalie_stats")
        
        self.btn_update_goalie_stats = QtWidgets.QPushButton(self.centralwidget)
        self.btn_update_goalie_stats.setGeometry(QtCore.QRect(890, 540, 75, 23))
        self.btn_update_goalie_stats.setObjectName("btn_update_goalie_stats")
        
        self.btn_update_standings = QtWidgets.QPushButton(self.centralwidget)
        self.btn_update_standings.setGeometry(QtCore.QRect(90, 570, 75, 23))
        self.btn_update_standings.setObjectName("btn_update_standings")
                
        self.btn_more_goalie_info = QtWidgets.QPushButton(self.centralwidget)
        self.btn_more_goalie_info.setGeometry(QtCore.QRect(890, 510, 75, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_more_goalie_info.sizePolicy().hasHeightForWidth())
        self.btn_more_goalie_info.setSizePolicy(sizePolicy)
        self.btn_more_goalie_info.setObjectName("btn_more_goalie_info")
        
        # Goalie Search
        self.line_edit_goalie_search = QtWidgets.QLineEdit(self.centralwidget)
        self.line_edit_goalie_search.setGeometry(QtCore.QRect(890, 340, 191, 31))
        self.line_edit_goalie_search.setObjectName("line_edit_goalie_search")
        
        self.btn_goalie_search = QtWidgets.QPushButton(self.centralwidget)
        self.btn_goalie_search.setGeometry(QtCore.QRect(1090, 340, 81, 31))
        self.btn_goalie_search.setObjectName("btn_goalie_search")
        
        self.table_goalie_search_result = CustomTable(self.centralwidget)
        self.table_goalie_search_result.setGeometry(QtCore.QRect(890, 380, 291, 121))
        self.table_goalie_search_result.setObjectName("table_goalie_search_result")
        
        # Standings        
        self.table_pacific_division = CustomTable(self.centralwidget)
        self.table_pacific_division.setGeometry(QtCore.QRect(10, 600, 581, 151))
        self.table_pacific_division.setObjectName("table_pacific_division")
                
        self.table_metro_division = CustomTable(self.centralwidget)
        self.table_metro_division.setGeometry(QtCore.QRect(610, 600, 581, 151))
        self.table_metro_division.setObjectName("table_metro_division")
        
        self.label_standings = QtWidgets.QLabel(self.centralwidget)
        self.label_standings.setGeometry(QtCore.QRect(10, 570, 47, 13))
        self.label_standings.setObjectName("label_standings")
        
        self.label_pacific_division = QtWidgets.QLabel(self.centralwidget)
        self.label_pacific_division.setGeometry(QtCore.QRect(10, 580, 121, 16))
        self.label_pacific_division.setObjectName("label_pacific_division")
        
        self.label_metro_division = QtWidgets.QLabel(self.centralwidget)
        self.label_metro_division.setGeometry(QtCore.QRect(610, 580, 121, 16))
        self.label_metro_division.setObjectName("label_metro_division")
        
        self.table_central_division = CustomTable(self.centralwidget)
        self.table_central_division.setGeometry(QtCore.QRect(10, 770, 581, 151))
        self.table_central_division.setObjectName("table_central_division")
        
        self.table_atlantic_division = CustomTable(self.centralwidget)
        self.table_atlantic_division.setGeometry(QtCore.QRect(610, 770, 581, 151))
        self.table_atlantic_division.setObjectName("table_atlantic_division")
        
        self.label_atlantic_division = QtWidgets.QLabel(self.centralwidget)
        self.label_atlantic_division.setGeometry(QtCore.QRect(610, 750, 121, 16))
        self.label_atlantic_division.setObjectName("label_atlantic_division")

        self.label_central_division = QtWidgets.QLabel(self.centralwidget)
        self.label_central_division.setGeometry(QtCore.QRect(10, 750, 121, 16))
        self.label_central_division.setObjectName("label_central_division")
        
        # Games for the day
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 1181, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.gamesLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.gamesLayout.setContentsMargins(0, 0, 0, 0)
        self.gamesLayout.setObjectName("gamesLayout")
                        
        # Menu bar
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1198, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(self)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
                
        self.set_standings_table()
        self.set_player_stats_table()
        self.set_goalie_stats_table()
               
        self.create_current_games_buttons(self.gamesLayout)              
        
        self.btn_more_player_info.resize(self.btn_more_player_info.sizeHint().width(), self.btn_more_player_info.sizeHint().height())
        self.btn_more_goalie_info.resize(self.btn_more_goalie_info.sizeHint().width(), self.btn_more_goalie_info.sizeHint().height())
        
        # Set up the more player details button
        self.btn_more_player_info.clicked.connect(self.open_player_info)
        self.btn_more_goalie_info.clicked.connect(self.open_goalie_info)
        
        # Set up goalie and player search buttons
        self.btn_goalie_search.clicked.connect(self.search_goalie)
        self.btn_player_search.clicked.connect(self.search_player)
        
        # Set up update buttons
        self.btn_update_player_stats.clicked.connect(self.update_player_stats)
        self.btn_update_goalie_stats.clicked.connect(self.update_goalie_stats)
        self.btn_update_standings.clicked.connect(self.update_standings)
                
        # Set up double clicking search tables
        self.table_player_search_result.doubleClicked.connect(self.open_detailed_search_player)
        self.table_goalie_search_result.doubleClicked.connect(self.open_detailed_search_goalie)
        
        self.actionExit.setShortcut('Alt+F4')
        self.actionExit.triggered.connect(self.close)
        
        self.conn.close()
            
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_standings.setText(_translate("MainWindow", "Standings"))
        self.label_pacific_division.setText(_translate("MainWindow", "Pacific Division"))
        self.label_metro_division.setText(_translate("MainWindow", "Metropolitan Division"))
        self.label_player_stats.setText(_translate("MainWindow", "Player Stats"))
        self.label_goalie_stats.setText(_translate("MainWindow", "Goalies Stats"))
        self.btn_update_player_stats.setText(_translate("MainWindow", "Update"))
        self.btn_update_goalie_stats.setText(_translate("MainWindow", "Update"))
        self.btn_update_standings.setText(_translate("MainWindow", "Update"))
        self.btn_more_player_info.setText(_translate("MainWindow", "More Player Details"))
        self.btn_more_goalie_info.setText(_translate("MainWindow", "More Goalie Details"))
        self.btn_goalie_search.setText(_translate("MainWindow", "Search"))
        self.btn_player_search.setText(_translate("MainWindow", "Search"))
        self.label_atlantic_division.setText(_translate("MainWindow", "Atlantic Division"))
        self.label_central_division.setText(_translate("MainWindow", "Central Division"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
    
    # Creates a connection to the nhl stats database
    def create_connection(self):
        db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("nhl_stats.db")
        if not db.open():
            QtWidgets.QMessageBox.critical(None, "Cannot open database",
                             "Unable to establish a database connection.\n"
                             "Click Cancel to exit.", QtWidgets.QMessageBox.Cancel)
            return False
        
        return db

    # Sets the database to the standings table
    def set_standings_table(self):
        self.db = self.create_connection()
            
        # Set the western conference standings table
        query = QtSql.QSqlQuery(self.db)
        query.prepare("""
                        SELECT Team_Name, Games_Played, Wins, Losses, OT, Points,
                        GPG, GAPG, PP_Percent, PK_Percent, Division, Regulation_Wins, ROW,
                        Goals_Scored, Goals_Against, Goal_Diff, Streak FROM teams 
                        WHERE Division = 'Pacific'
                        ORDER BY Points DESC
                        """)
        query.exec_()
        
        pacific_model = QtSql.QSqlQueryModel()
        pacific_model.setQuery(query)
        
        self.table_pacific_division.setModel(pacific_model)
        
        query.prepare("""
                        SELECT Team_Name, Games_Played, Wins, Losses, OT, Points,
                        GPG, GAPG, PP_Percent, PK_Percent, Division, Regulation_Wins, ROW,
                        Goals_Scored, Goals_Against, Goal_Diff, Streak FROM teams 
                        WHERE Division = 'Central'
                        ORDER BY Points DESC
                        """)
        query.exec_()
        
        central_model = QtSql.QSqlQueryModel()
        central_model.setQuery(query)
        
        self.table_central_division.setModel(central_model)
        
        # Set the eastern conference standings table   
        query.prepare("""
                        SELECT Team_Name, Games_Played, Wins, Losses, OT, Points,
                        GPG, GAPG, PP_Percent, PK_Percent, Division, Regulation_Wins, ROW,
                        Goals_Scored, Goals_Against, Goal_Diff, Streak 
                        FROM teams WHERE Division = 'Metropolitan'
                        ORDER BY Points DESC
                        """)
        query.exec_()
        
        metro_model = QtSql.QSqlQueryModel()
        metro_model.setQuery(query)
        self.table_metro_division.setModel(metro_model)
        
        query.prepare("""
                        SELECT Team_Name, Games_Played, Wins, Losses, OT, Points,
                        GPG, GAPG, PP_Percent, PK_Percent, Division, Regulation_Wins, ROW,
                        Goals_Scored, Goals_Against, Goal_Diff, Streak 
                        FROM teams WHERE Division = 'Atlantic'
                        ORDER BY Points DESC
                        """)
        query.exec_()
        
        atlantic_model = QtSql.QSqlQueryModel()
        atlantic_model.setQuery(query)
        self.table_atlantic_division.setModel(atlantic_model)
        
        self.db.close()

    # Sets the database to the player stats table to enable queries to db
    def set_player_stats_table(self):
        self.db = self.create_connection()
        
        query = QtSql.QSqlQuery(self.db)
        query.prepare("""
                      SELECT Full_Name, Team_Abrv, Position, Games_Played,
                      Goals, Assists, Points, Plus_Minus, PIM, PPG, PPP, SHG, SHP,
                      GWG, S, Shot_Percent, FO_Percent FROM players
                      ORDER BY Points DESC
                      """)
        query.exec_()
        
        # Set the western conference standings table
        player_model = QtSql.QSqlQueryModel()
        player_model.setQuery(query)
        
        while(player_model.canFetchMore()):
            player_model.fetchMore()
            
        self.table_player_stats.setModel(player_model)
        
        self.db.close()
        
    # Set the goalie stats table with the database
    def set_goalie_stats_table(self):
        self.db = self.create_connection()
        
        query = QtSql.QSqlQuery(self.db)
        query.prepare("""
                      SELECT Full_Name, Team_Abrv, Catches, GP, GS, W, L, OTL, SO, SA, Sv,
                      GA, SvPct, GAA, TOI, G, A, P, PIM FROM goalies
                      ORDER BY W DESC
                      """)
        query.exec_()
        
        # Set the eastern conference standings table
        goalie_model = QtSql.QSqlQueryModel()
        goalie_model.setQuery(query)
        self.table_goalie_stats.setModel(goalie_model)
        
        self.db.close()
            
    # Creates buttons for each current nhl games for the day
    def create_current_games_buttons(self, layout: QtWidgets.QHBoxLayout):
        try:
            # Iterate through each row
            for index, row in self.games.iterrows():
                # Create a button, edit the text to be Away @ Home
                try:
                    self.button = QtWidgets.QPushButton("{} @ {}".format(self.teams[row['awayID']], self.teams[row['homeID']]))
                    self.button.clicked.connect(partial(self.open_boxscore, index))
                    layout.addWidget(self.button)
                except KeyError as e:
                    print(e)
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
                
        dialog = Player_Window(id, False)
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
                  WHERE Full_Name = (?) AND Team_Abrv = (?)
                  """, (goalie_name, team))
        id = c.fetchone()
        id = id[0]
        print(id)
                
        dialog = Player_Window(id, True)
        self.dialogs.append(dialog)
        dialog.show()
        self.conn.close()
            
    # Searches for players within the database based on user inputed name
    def search_player(self):
        self.db = self.create_connection()
        self.db.open()
        # Get selection
        name = self.line_edit_player_search.text()

        query = QtSql.QSqlQuery(self.db)
        query.prepare("SELECT * FROM players WHERE Full_Name LIKE (?)")
        query.bindValue(0, "%{}%".format(name))
        query.exec_()

        search_model = QtSql.QSqlQueryModel()
        search_model.setQuery(query)
        
        self.table_player_search_result.setModel(search_model)
        self.table_player_search_result.show()
        
        self.db.close()

        
    # Searches for the goalies within the database based on user inputed name
    def search_goalie(self):
        self.db = self.create_connection()
        self.db.open()
        # Get selection
        name = self.line_edit_goalie_search.text()
        
        query = QtSql.QSqlQuery(self.db)
        query.prepare("SELECT * FROM goalies WHERE Full_Name LIKE (?)")
        query.bindValue(0, "%{}%".format(name))
        query.exec_()
        
        search_model = QtSql.QSqlQueryModel()
        search_model.setQuery(query)
        
        self.table_goalie_search_result.setModel(search_model)
        self.table_goalie_search_result.show()        
        self.db.close()
    
    # Opens the player info window of the double clicked player in the player search result table
    def open_detailed_search_player(self):
        i = self.table_player_search_result.selectionModel().currentIndex()
        id = self.table_player_search_result.model().index(i.row(), 0).data()
        print(id)
        dialog = Player_Window(id, False)
        self.dialogs.append(dialog)
        dialog.show()
        return None
    
    # Opens the player info window of the double clicked goalie in the goalie search result table
    def open_detailed_search_goalie(self):
        i = self.table_goalie_search_result.selectionModel().currentIndex()
        id = self.table_goalie_search_result.model().index(i.row(), 0).data()
        print(id)
        dialog = Player_Window(id, True)
        self.dialogs.append(dialog)
        dialog.show()
        return None
    
    # Gets the player name and the team name from the player stats table
    def get_selected_player(self):
        rows = self.table_player_stats.selectionModel().selectedRows()
        return self.table_player_stats.model().index(rows[0].row(), 0).data(), self.table_player_stats.model().index(rows[0].row(), 1).data()
    
    # Gets the goalie name and team name from the goalie stats table
    def get_selected_goalie(self):
        rows = self.table_goalie_stats.selectionModel().selectedRows()
        return self.table_goalie_stats.model().index(rows[0].row(), 0).data(), self.table_goalie_stats.model().index(rows[0].row(), 1).data()
                        
    # Updates the NHL standings table with new up-to-date data from NHL API
    def update_standings(self):
        main.get_team_stats()
        self.set_standings_table()
        self.table_atlantic_division.show()
        self.table_central_division.show()
        self.table_metro_division.show()
        self.table_pacific_division.show()
        print("Updated Standings")
    
    # Updates the player leaderboards from the NHL API
    def update_player_stats(self):
        main.get_stat_leaders()
        self.set_player_stats_table()
        print("Updated Players")
        self.table_player_stats.show()
    
    # Updates the goalie leaderboards from the NHL API
    def update_goalie_stats(self):
        main.get_goalie_leaders()
        self.set_goalie_stats_table()
        print("Updated Goalies")
        self.table_goalie_stats.show()
    
    def closeEvent(self, event):
        super(NHL_MainWindow, self).closeEvent(event)
        self.db.close()
        self.conn.close()