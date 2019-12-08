from PyQt5 import QtCore, QtGui, QtWidgets
from custom_table import CustomTable
import pandas as pd
from DataFrameModel import DataFrameModel


class Boxscore_Window(QtWidgets.QMainWindow):
    def __init__(self, data):
        super(Boxscore_Window, self).__init__()
        self.boxscore_data = data
        self.setupUi()
        
    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(867, 748)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.table_home_stats = CustomTable(self.centralwidget)
        self.table_home_stats.setGeometry(QtCore.QRect(0, 60, 661, 321))
        self.table_home_stats.setObjectName("table_home_stats")
        home_model = DataFrameModel(self.boxscore_data.home_player_stats)
        self.table_home_stats.setModel(home_model)
        self.change_table_style(self.table_home_stats)
        
        self.table_away_stats = CustomTable(self.centralwidget)
        self.table_away_stats.setGeometry(QtCore.QRect(10, 440, 651, 261))
        self.table_away_stats.setObjectName("table_away_stats")
        away_model = DataFrameModel(self.boxscore_data.away_player_stats)
        self.table_away_stats.setModel(away_model)
        self.change_table_style(self.table_away_stats)
        
        self.label_away_team_name = QtWidgets.QLabel(self.centralwidget)
        self.label_away_team_name.setGeometry(QtCore.QRect(10, 395, 101, 31))
        self.label_away_team_name.setObjectName("label_away_team_name")
        self.label_home_team_name = QtWidgets.QLabel(self.centralwidget)
        self.label_home_team_name.setGeometry(QtCore.QRect(10, 9, 91, 41))
        self.label_home_team_name.setObjectName("label_home_team_name")
        self.label_goals = QtWidgets.QLabel(self.centralwidget)
        self.label_goals.setGeometry(QtCore.QRect(740, 10, 47, 13))
        self.label_goals.setObjectName("label_goals")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(680, 30, 171, 671))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.layout_goals_display = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.layout_goals_display.setContentsMargins(0, 0, 0, 0)
        self.layout_goals_display.setObjectName("layout_goals_display")
        self.label_home_score = QtWidgets.QLabel(self.centralwidget)
        self.label_home_score.setGeometry(QtCore.QRect(110, 15, 61, 31))
        self.label_home_score.setObjectName("label_home_score")
        self.label_away_score = QtWidgets.QLabel(self.centralwidget)
        self.label_away_score.setGeometry(QtCore.QRect(120, 400, 61, 16))
        self.label_away_score.setObjectName("label_away_score")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(180, 390, 481, 51))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.grid_away_team_stats = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.grid_away_team_stats.setContentsMargins(0, 0, 0, 0)
        self.grid_away_team_stats.setObjectName("gridLayout_2")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(180, 0, 481, 51))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.grid_home_team_stats = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.grid_home_team_stats.setContentsMargins(0, 0, 0, 0)
        self.grid_home_team_stats.setObjectName("gridLayout_3")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 867, 21))
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
        
        self.setup_boxscoreUi()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_away_team_name.setText(_translate("MainWindow", "Away Team:"))
        self.label_home_team_name.setText(_translate("MainWindow", "Home Team:"))
        self.label_goals.setText(_translate("MainWindow", "Goals"))
        self.label_home_score.setText(_translate("MainWindow", "Home Score"))
        self.label_away_score.setText(_translate("MainWindow", "Away Score"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
    
    # Set up the UI based on the information of the current boxscore data
    def setup_boxscoreUi(self):
        # Set the team names
        self.label_away_team_name.setText(self.boxscore_data.away_team)
        self.label_home_team_name.setText(self.boxscore_data.home_team)
        
        # Set the team score
        self.label_away_score.setText(str(self.boxscore_data.get_away_score()))
        self.label_home_score.setText(str(self.boxscore_data.get_home_score()))
        
        # Create the team stats
        for stats in self.boxscore_data.away_team_stats:
            print("Away Team Stats: " + stats)
            label = QtWidgets.QLabel()
            label.setText(str(stats))
            self.grid_away_team_stats.addWidget(label)
        
        for stats in self.boxscore_data.home_team_stats:
            print("Home Team Stats:" + stats)
            label = QtWidgets.QLabel()
            label.setText(str(stats))
            self.grid_home_team_stats.addWidget(label)
            
        # Create the goals Labels
        goals_scored = self.boxscore_data.get_goals()
        for goals in goals_scored:
            label = QtWidgets.QLabel()
            label.setText(goals)
            self.layout_goals_display.addWidget(label)

    def change_table_style(self, table):
        header = table.horizontalHeader()
        header.setStyleSheet("""::section{background-color: rgb(56,56,56);
                                        color: white;}""")
        vertical = table.verticalHeader()
        vertical.setStyleSheet("""::section{background-color: rgb(56,56,56);
                                        color: white;}""")
        table.setStyleSheet("background-color:rgb(212, 213, 214);alternate-background-color:rgb(165, 171, 181);")
        
       
