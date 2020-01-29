from PyQt5 import QtCore, QtWidgets
from custom_table import CustomTable
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
        
        # Home Player Stats
        self.table_home_stats = CustomTable(self.centralwidget)
        self.table_home_stats.setGeometry(QtCore.QRect(0, 60, 661, 321))
        self.table_home_stats.setObjectName("table_home_stats")
        home_model = DataFrameModel(self.boxscore_data.home_player_stats)
        self.table_home_stats.setModel(home_model)        
        
        # Away Player Stats
        self.table_away_stats = CustomTable(self.centralwidget)
        self.table_away_stats.setGeometry(QtCore.QRect(10, 440, 651, 261))
        self.table_away_stats.setObjectName("table_away_stats")
        away_model = DataFrameModel(self.boxscore_data.away_player_stats)
        self.table_away_stats.setModel(away_model)
                        
        # Goals Display        
        self.label_goals = QtWidgets.QLabel(self.centralwidget)
        self.label_goals.setGeometry(QtCore.QRect(740, 10, 47, 13))
        self.label_goals.setObjectName("label_goals")  
        
        self.scrollArea_goals = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_goals.setGeometry(QtCore.QRect(670, 30, 191, 671))
        self.scrollArea_goals.setWidgetResizable(True)
        self.scrollArea_goals.setObjectName("scrollArea_goals")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 189, 669))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layout_goals_display = QtWidgets.QVBoxLayout()
        self.layout_goals_display.setObjectName("layout_goals_display")
        self.verticalLayout.addLayout(self.layout_goals_display)
        self.scrollArea_goals.setWidget(self.scrollAreaWidgetContents_2)
        
        # Home Score         
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(10, 0, 151, 61))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_home = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_home.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_home.setObjectName("horizontalLayout_home")
        self.label_home_team_name = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        self.label_home_team_name.setObjectName("label_home_team_name")
        self.horizontalLayout_home.addWidget(self.label_home_team_name)
        self.label_home_score = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        self.label_home_score.setObjectName("label_home_score")
        self.horizontalLayout_home.addWidget(self.label_home_score)
               
        # Away Score        
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 380, 171, 61))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_away = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_away.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_away.setObjectName("horizontalLayout_away")
        self.label_away_team_name = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_away_team_name.setObjectName("label_away_team_name")
        self.horizontalLayout_away.addWidget(self.label_away_team_name)
        self.label_away_score = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_away_score.setObjectName("label_away_score")
        self.horizontalLayout_away.addWidget(self.label_away_score)
        
        # Home Team Stats        
        self.scrollArea_home_team_stats = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_home_team_stats.setGeometry(QtCore.QRect(160, 0, 501, 61))
        self.scrollArea_home_team_stats.setWidgetResizable(True)
        self.scrollArea_home_team_stats.setObjectName("scrollArea_home_team_stats")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 499, 59))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.layout_home_team_stats = QtWidgets.QHBoxLayout()
        self.layout_home_team_stats.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.layout_home_team_stats.setObjectName("layout_home_team_stats")
        self.horizontalLayout.addLayout(self.layout_home_team_stats)
        self.scrollArea_home_team_stats.setWidget(self.scrollAreaWidgetContents)
        
        # Away Team Stats      
        self.scrollArea_away_team_stats = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_away_team_stats.setGeometry(QtCore.QRect(180, 380, 481, 61))
        self.scrollArea_away_team_stats.setWidgetResizable(True)
        self.scrollArea_away_team_stats.setObjectName("scrollArea_away_team_stats")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 479, 59))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.layout_away_team_stats = QtWidgets.QHBoxLayout()
        self.layout_away_team_stats.setObjectName("layout_away_team_stats")
        self.horizontalLayout_2.addLayout(self.layout_away_team_stats)
        self.scrollArea_away_team_stats.setWidget(self.scrollAreaWidgetContents_3)
        
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
        
        self.actionExit.setShortcut('Alt+F4')
        self.actionExit.triggered.connect(self.close)
        
        QtCore.QMetaObject.connectSlotsByName(self)        
        
        self.retranslateUi(self)
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
            label = QtWidgets.QLabel()
            label.setText(stats + "  " + str(self.boxscore_data.away_team_stats[stats]))
            label.setScaledContents(True)
            label.setWordWrap(True)
            self.layout_away_team_stats.addWidget(label)
        
        for stats in self.boxscore_data.home_team_stats:
            label = QtWidgets.QLabel()
            label.setScaledContents(True)
            label.setWordWrap(True)
            label.setText(stats + "  " + str(self.boxscore_data.home_team_stats[stats]))
            self.layout_home_team_stats.addWidget(label)
            
        # Create the goals Labels
        goals_scored = self.boxscore_data.get_goals()
        for goals in goals_scored:
            label = QtWidgets.QLabel()
            label.setScaledContents(True)
            label.setWordWrap(True)
            label.setText(goals)
            self.layout_goals_display.addWidget(label)
       
class Stat_List(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Stat_List, self).__init__(parent)
        self.initWidget()

    def initWidget(self):
        listBox = QtWidgets.QVBoxLayout(self)
        self.setLayout(listBox)
    
        scroll = QtWidgets.QScrollArea(self)
        listBox.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QtWidgets.QWidget(scroll)
    
        scrollLayout = QtWidgets.QVBoxLayout(scrollContent)
        scrollContent.setLayout(scrollLayout)
        scroll.setWidget(scrollContent)
        