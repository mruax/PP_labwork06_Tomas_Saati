import sys
from pathlib import Path

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget, QInputDialog, QLineEdit

from generated_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.tableWidget.horizontalHeader().setSectionsClickable(True)
        self.ui.tableWidget.verticalHeader().setSectionsClickable(True)

        self.ui.tableWidget.horizontalHeader().setSectionsMovable(False)
        self.ui.tableWidget.verticalHeader().setSectionsMovable(False)

        self.ui.tableWidget.horizontalHeader().sectionDoubleClicked.connect(self.editColumnHeader)
        self.ui.tableWidget.verticalHeader().sectionDoubleClicked.connect(self.editRowHeader)

        self.setWindowTitle("Tomas Saati")
        self.ui.result_button.clicked.connect(self.result)

        self.ui.criteriaAmount.valueChanged.connect(self.changeAmount)

    def editColumnHeader(self, logicalIndex):
        item = self.ui.tableWidget.horizontalHeaderItem(logicalIndex)
        n = self.ui.tableWidget.columnCount()
        if logicalIndex == n - 1:
            return
        if item:
            oldHeaders = [self.ui.tableWidget.horizontalHeaderItem(i).text() for i in range(n)]
            newHeader, ok = QInputDialog.getText(self, 'Изменение данных', 'Название критерия:')
            if ok:
                oldHeaders[logicalIndex] = newHeader
                self.ui.tableWidget.setHorizontalHeaderLabels(oldHeaders)

    def editRowHeader(self, logicalIndex):
        item = self.ui.tableWidget.verticalHeaderItem(logicalIndex)
        n = self.ui.tableWidget.rowCount()
        if logicalIndex == n - 1:
            return
        if item:
            oldHeaders = [self.ui.tableWidget.verticalHeaderItem(i).text() for i in
                          range(n)]
            newHeader, ok = QInputDialog.getText(self, 'Изменение данных', 'Название критерия:')
            if ok:
                oldHeaders[logicalIndex] = newHeader
                self.ui.tableWidget.setVerticalHeaderLabels(oldHeaders)

    def result(self):
        print("Нажал кнопку!")

    def nulify_cells(self):
        for row in range(self.ui.tableWidget.rowCount()):
            for col in range(self.ui.tableWidget.columnCount()):
                item = self.ui.tableWidget.item(row, col)
                if item is not None:
                    item.setText("")

    def changeAmount(self):
        # self.ui.tableWidget.setColumnCount(self.ui.tableWidget.columnCount() + 1)
        # self.ui.tableWidget.setRowCount(self.ui.tableWidget.rowCount() + 1)
        # row_position = self.ui.tableWidget.rowCount() - 1
        # column_position = self.ui.tableWidget.columnCount() - 1
        # self.ui.tableWidget.insertRow(row_position)
        # self.ui.tableWidget.insertColumn(column_position)
        n = self.ui.criteriaAmount.value()
        self.ui.tableWidget.setRowCount(n + 1)
        self.ui.tableWidget.setColumnCount(n + 1)
        self.nulify_cells()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec())