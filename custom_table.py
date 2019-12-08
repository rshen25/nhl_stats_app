from PyQt5 import QtCore, QtGui, QtWidgets, QtSql

# Overrides TableView class, sets the table columns to fit to content, and allows for user resizing
class CustomTable(QtWidgets.QTableView):
    def __init__(self,  *args, **kwargs):
        super(CustomTable, self).__init__(*args, **kwargs)
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
    
    def resizeEvent(self, event):
        super(QtWidgets.QTableView, self).resizeEvent(event)
        header = self.horizontalHeader()
        for column in range(header.count()):
            header.setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)
            width = header.sectionSize(column)
            header.setSectionResizeMode(column, QtWidgets.QHeaderView.Interactive)
            header.resizeSection(column, width)
