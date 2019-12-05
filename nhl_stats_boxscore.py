# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\git_local_repo\nhl_stats_app\nhl_stats_boxscore.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(867, 748)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
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
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 867, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
