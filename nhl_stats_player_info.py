import api
import nhl_parse_const as pc
from PyQt5 import QtCore, QtWidgets, QtSql
from custom_table import CustomTable
from DataFrameModel import DataFrameModel

class Player_Window(QtWidgets.QMainWindow):        
    def __init__(self, player_id, isGoalie):
        super(Player_Window, self).__init__()
        self.player_id = player_id
        self.isGoalie = isGoalie
        self.player_data = api.get_player_data(player_id)
        if (isGoalie):
            self.player_career_data = api.get_goalie_career_stats(player_id)
            self.game_log = api.get_goalie_game_log(player_id, pc.CURRENT_SEASON)
        else:
            self.player_career_data = api.get_player_career_stats(player_id)
            self.game_log = api.get_game_log(player_id, pc.CURRENT_SEASON)
    
        self.setupUi()
        
    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(500, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        
        self.label_career_stats = QtWidgets.QLabel(self.centralwidget)
        #self.label_career_stats.setGeometry(QtCore.QRect(10, 110, 81, 16))
        self.label_career_stats.setObjectName("label_career_stats")
        self.gridLayout.addWidget(self.label_career_stats, 1, 0, 1, 1)
        
        # Create the career stats table and set the model to be able to read a pandas dataframe
        self.table_career_stats = CustomTable(self.centralwidget)
        #self.table_career_stats.setGeometry(QtCore.QRect(10, 130, 571, 201))
        self.table_career_stats.setObjectName("table_career_stats")
        self.player_career_data_model = DataFrameModel(self.player_career_data)
        self.table_career_stats.setModel(self.player_career_data_model)
        self.gridLayout.addWidget(self.table_career_stats, 2, 0, 1, 2)
        
        # Player information
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(410, 0, 160, 110))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSizeConstraint(QtWidgets.QVBoxLayout.SetMaximumSize)
        
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
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 0, 331, 111))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QVBoxLayout.SetMaximumSize)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_player_name = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_player_name.setObjectName("label_player_name")
        self.verticalLayout_2.addWidget(self.label_player_name)
        self.label_player_team = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_player_team.setObjectName("label_player_team")
        self.verticalLayout_2.addWidget(self.label_player_team)
        self.label_player_number = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_player_number.setObjectName("label_player_number")
        self.verticalLayout_2.addWidget(self.label_player_number)
        self.label_player_position = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_player_position.setObjectName("label_player_position")
        self.verticalLayout_2.addWidget(self.label_player_position)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        # Game Log
        self.label_game_log = QtWidgets.QLabel(self.centralwidget)
        #self.label_game_log.setGeometry(QtCore.QRect(10, 340, 51, 16))
        self.label_game_log.setObjectName("label_game_log")
        self.gridLayout.addWidget(self.label_game_log, 3, 0, 1, 1)
        
        self.table_game_log = CustomTable(self.centralwidget)
        #self.table_game_log.setGeometry(QtCore.QRect(10, 360, 571, 201))
        self.table_game_log.setObjectName("table_game_log")
        self.game_log_model = DataFrameModel(self.game_log)
        self.table_game_log.setModel(self.game_log_model)
        self.gridLayout.addWidget(self.table_game_log, 4, 0, 1, 2)

        # Menu bar
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
        
        self.display_player_info()
        
        self.actionExit.setShortcut('Alt+F4')
        self.actionExit.triggered.connect(self.close)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Player Information - {}".format(self.player_data.loc[0, 'Full_Name'])))
        self.label_player_age.setText(_translate("MainWindow", "Age:"))
        self.label_player_height.setText(_translate("MainWindow", "Height:"))
        self.label_player_weight.setText(_translate("MainWindow", "Weight:"))
        self.label_player_shoots.setText(_translate("MainWindow", "Shoots:"))
        self.label_player_birthplace.setText(_translate("MainWindow", "Birth Country:"))
        self.label_career_stats.setText(_translate("MainWindow", "Career Stats"))
        self.label_player_name.setText(_translate("MainWindow", "Player Name"))
        self.label_player_team.setText(_translate("MainWindow", "Team Name"))
        self.label_player_number.setText(_translate("MainWindow", "Player Number"))
        self.label_player_position.setText(_translate("MainWindow", "Position"))
        self.label_game_log.setText(_translate("MainWindow", "Game Log"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionExit.setText(_translate("MainWindow", "Close"))

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
