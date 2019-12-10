from PyQt5 import QtCore, QtGui, QtWidgets, QtSql

# Overrides TableView class, sets the table columns to fit to content, and allows for user resizing
class CustomTable(QtWidgets.QTableView):
    def __init__(self,  *args, **kwargs):
        super(CustomTable, self).__init__(*args, **kwargs)
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.change_table_style()
    
    def resizeEvent(self, event):
        super(QtWidgets.QTableView, self).resizeEvent(event)
        header = self.horizontalHeader()
        for column in range(header.count()):
            header.setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)
            width = header.sectionSize(column)
            header.setSectionResizeMode(column, QtWidgets.QHeaderView.Interactive)
            header.resizeSection(column, width)
            
    def change_table_style(self):
        self.setAlternatingRowColors(True)
        header = self.horizontalHeader()
        header.setStyleSheet("""::section{background-color: rgb(56,56,56);
                                        color: white;}""")
        vertical = self.verticalHeader()
        vertical.setStyleSheet("""::section{background-color: rgb(56,56,56);
                                        color: white;}""")
        self.setStyleSheet("background-color:rgb(212, 213, 214);alternate-background-color:rgb(165, 171, 181);")
