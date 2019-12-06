from PyQt5 import QtCore, QtGui, QtWidgets


class Boxscore_Window(QtWidgets.QMainWindow):
    def __init__(self, boxscore_data):
        super(Boxscore_Window, self).__init__()
        self.boxscore_data = boxscore_data
        self.setupUi()
        print("window created")
        
    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(867, 748)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.table_home_stats = QtWidgets.QTableView(self.centralwidget)
        self.table_home_stats.setGeometry(QtCore.QRect(10, 30, 651, 321))
        self.table_home_stats.setObjectName("table_home_stats")
        self.table_away_stats = QtWidgets.QTableView(self.centralwidget)
        self.table_away_stats.setGeometry(QtCore.QRect(10, 380, 651, 321))
        self.table_away_stats.setObjectName("table_away_stats")
        self.label_away_team_name = QtWidgets.QLabel(self.centralwidget)
        self.label_away_team_name.setGeometry(QtCore.QRect(10, 360, 61, 16))
        self.label_away_team_name.setObjectName("label_away_team_name")
        self.label_home_team_name = QtWidgets.QLabel(self.centralwidget)
        self.label_home_team_name.setGeometry(QtCore.QRect(10, 10, 61, 16))
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
        self.label_home_score.setGeometry(QtCore.QRect(80, 10, 61, 16))
        self.label_home_score.setObjectName("label_home_score")
        self.label_away_score = QtWidgets.QLabel(self.centralwidget)
        self.label_away_score.setGeometry(QtCore.QRect(80, 360, 61, 16))
        self.label_away_score.setObjectName("label_away_score")
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

#if __name__ == "__main__":
#    import sys
#    app = QtWidgets.QApplication(sys.argv)
#    MainWindow = QtWidgets.QMainWindow()
#    ui = Boxscore_Window()
#    ui.setupUi(MainWindow)
#    MainWindow.show()
#    sys.exit(app.exec_())
