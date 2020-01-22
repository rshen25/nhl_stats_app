from PyQt5 import QtCore, QtWidgets, QtSql
from custom_table import CustomTable
from DataFrameModel import DataFrameModel

class Player_Window(QtWidgets.QMainWindow):        
    def __init__(self, player_id, player_data, player_career_data, isGoalie):
        super(Player_Window, self).__init__()
        self.player_id = player_id
        self.isGoalie = isGoalie
        self.player_data = player_data
        self.player_career_data = player_career_data
        self.setupUi()
        
    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(988, 606)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
#        self.table_season_stats = CustomTable(self.centralwidget)
#        self.table_season_stats.setGeometry(QtCore.QRect(20, 150, 951, 71))
#        self.table_season_stats.setObjectName("table_season_stats")
        
        # Create the career stats table and set the model to be able to read a pandas dataframe
        self.table_career_stats = CustomTable(self.centralwidget)
        self.table_career_stats.setGeometry(QtCore.QRect(20, 150, 951, 301))
        self.table_career_stats.setObjectName("table_career_stats")
        self.model = DataFrameModel(self.player_career_data)
        self.table_career_stats.setModel(self.model)
        
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(410, 0, 160, 110))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSizeConstraint(QtWidgets.QVBoxLayout.SetMaximumSize)
        self.verticalLayoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget2.setGeometry(QtCore.QRect(10, 0, 160, 110))
        self.verticalLayoutWidget2.setObjectName("verticalLayoutWidget")
        self.verticalLayout2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget2)
        self.verticalLayout2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout2.setObjectName("verticalLayout")
        self.verticalLayout2.setSizeConstraint(QtWidgets.QVBoxLayout.SetMaximumSize)

        self.label_player_age = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_player_age.setObjectName("label_player_age")
        self.verticalLayout.addWidget(self.label_player_age)
        self.label_player_height = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_player_height.setObjectName("label_player_height")
        self.verticalLayout.addWidget(self.label_player_height)
        self.label_player_weight = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_player_weight.setObjectName("label_player_weight")
        self.verticalLayout.addWidget(self.label_player_weight)
        self.label_player_shoots = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_player_shoots.setObjectName("label_player_shoots")
        self.verticalLayout.addWidget(self.label_player_shoots)
        self.label_player_birthplace = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_player_birthplace.setObjectName("label_player_birthplace")
        self.verticalLayout.addWidget(self.label_player_birthplace)
        self.label_player_name = QtWidgets.QLabel(self.centralwidget)
        self.label_player_name.setGeometry(QtCore.QRect(20, 10, 111, 41))
        self.label_player_name.setObjectName("label_player_name")
        self.verticalLayout2.addWidget(self.label_player_name)
        self.label_player_team = QtWidgets.QLabel(self.centralwidget)
        self.label_player_team.setGeometry(QtCore.QRect(120, 70, 111, 31))
        self.label_player_team.setObjectName("label_player_team")
        self.verticalLayout2.addWidget(self.label_player_team)
        self.label_player_number = QtWidgets.QLabel(self.centralwidget)
        self.label_player_number.setGeometry(QtCore.QRect(120, 20, 81, 16))
        self.label_player_number.setObjectName("label_player_number")
        self.verticalLayout2.addWidget(self.label_player_number)
        self.label_player_position = QtWidgets.QLabel(self.centralwidget)
        self.label_player_position.setGeometry(QtCore.QRect(30, 80, 47, 13))
        self.label_player_position.setObjectName("label_player_position")
        self.verticalLayout2.addWidget(self.label_player_position)
#        self.label_11 = QtWidgets.QLabel(self.centralwidget)
#        self.label_11.setGeometry(QtCore.QRect(20, 130, 81, 21))
#        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(20, 240, 81, 16))
        self.label_12.setObjectName("label_12")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 988, 21))
        self.menubar.setObjectName("menubar")
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
        self.db = self.create_connection()
        
#        self.set_current_season_table(self.player_id)
        
        self.display_player_info()
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_player_age.setText(_translate("MainWindow", "Age:"))
        self.label_player_height.setText(_translate("MainWindow", "Height:"))
        self.label_player_weight.setText(_translate("MainWindow", "Weight:"))
        self.label_player_shoots.setText(_translate("MainWindow", "Shoots:"))
        self.label_player_birthplace.setText(_translate("MainWindow", "Birth Country:"))
        self.label_player_name.setText(_translate("MainWindow", "Player Name"))
        self.label_player_team.setText(_translate("MainWindow", "Team Name"))
        self.label_player_number.setText(_translate("MainWindow", "Player Number"))
        self.label_player_position.setText(_translate("MainWindow", "Position"))
#        self.label_11.setText(_translate("MainWindow", "Current Season"))
        self.label_12.setText(_translate("MainWindow", "Career Stats"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionExit.setText(_translate("MainWindow", "Close"))

    # queries the database and populates the current season stats table
#    def set_current_season_table(self, player_id):
#        model = QtSql.QSqlQueryModel()
#        if self.isGoalie:
#            model.setQuery("""
#                           SELECT Games_Played, Games_Started, Wins, Losses,
#                              OT, Shutouts, Saves, Save_Percentage, GAA, GA, SA FROM goalies
#                           WHERE Player_ID = {}
#                           """.format(player_id))
#        else:
#            model.setQuery("""
#                           SELECT Games_Played, Goals, Assists, Points, Plus_Minus, PIM, PPG, PPP, SHG,
#                           SHP, GWG, OTG, S, Shot_Percent, Blk, FO_Percent, Hits FROM players
#                           WHERE Player_ID = {}
#                           """.format(player_id))
#        self.table_season_stats.setModel(model)

    # Create a connection to the database
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
    
    # Populates and displays the player information such as name, age, team, etc.
    def display_player_info(self):
        
        # Set label names
        self.label_player_name.setText(self.player_data.loc[0, 'Full_Name'])
        self.label_player_name.setScaledContents(True)
        self.label_player_team.setText(str(self.player_data.loc[0, 'Team_Name']))
        self.label_player_team.setScaledContents(True)        
        self.label_player_age.setText("Age: " + str(self.player_data.loc[0, 'Age']))
        self.label_player_age.setScaledContents(True)
        self.label_player_height.setText("Height: " + str(self.player_data.loc[0, 'Height']))
        self.label_player_height.setScaledContents(True)
        self.label_player_weight.setText("Weight: " + str(self.player_data.loc[0, 'Weight']))
        self.label_player_weight.setScaledContents(True)
        self.label_player_birthplace.setText("Country: " + str(self.player_data.loc[0, 'Country']))
        self.label_player_birthplace.setScaledContents(True)
        self.label_player_number.setText("Number: " + str(self.player_data.loc[0, 'Number']))
        self.label_player_number.setScaledContents(True)
        self.label_player_shoots.setText("Handed: " + str(self.player_data.loc[0, 'Shoots']))
        self.label_player_shoots.setScaledContents(True)
        self.label_player_position.setText("Position: " + str(self.player_data.loc[0, 'Position']))
        self.label_player_position.setScaledContents(True)
            
    # Close event to close the database connection when window is closed
    def closeEvent(self, event):
        super(Player_Window, self).closeEvent(event)
        self.db.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Player_Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
