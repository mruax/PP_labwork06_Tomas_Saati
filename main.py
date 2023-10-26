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

        self.ui.tableWidget.horizontalHeader().sectionDoubleClicked.connect(self.editHeader)
        self.ui.tableWidget.verticalHeader().sectionDoubleClicked.connect(self.editHeader)

        self.setWindowTitle("Tomas Saati")
        self.ui.result_button.clicked.connect(self.result)

        self.ui.criteriaAmount.valueChanged.connect(self.changeAmount)
        self.amount = self.ui.criteriaAmount.value()

    def editHeader(self, logicalIndex):
        n = self.ui.tableWidget.rowCount()
        if logicalIndex == n - 1:
            return
        oldHeaders = [self.ui.tableWidget.verticalHeaderItem(i).text() for i in range(n)]
        oldHeaders2 = [self.ui.tableWidget.horizontalHeaderItem(i).text() for i in range(n)]
        newHeader, ok = QInputDialog.getText(self, 'Изменение данных', 'Название критерия:')
        if ok:
            oldHeaders[logicalIndex] = newHeader
            oldHeaders2[logicalIndex] = newHeader
            self.ui.tableWidget.setVerticalHeaderLabels(oldHeaders)
            self.ui.tableWidget.setHorizontalHeaderLabels(oldHeaders2)

    def result(self):
        print("Нажал кнопку!")

    def nulify_cells(self):
        for row in range(self.ui.tableWidget.rowCount()):
            for col in range(self.ui.tableWidget.columnCount()):
                item = self.ui.tableWidget.item(row, col)
                if item is not None:
                    item.setText("")

    def change_headers(self):
        n = self.ui.tableWidget.columnCount()
        headers = [self.ui.tableWidget.verticalHeaderItem(i).text() for i in range(n)]
        headers[n - 2] = f"Критерий {n - 1}"
        headers[n - 1] = "Сумма"
        n = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.setVerticalHeaderLabels(headers)
        headers = [self.ui.tableWidget.horizontalHeaderItem(i).text() for i in range(n)]
        headers[n - 2] = f"Критерий {n - 1}"
        headers[n - 1] = "Сумма"
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)

    def changeAmount(self):
        n = self.ui.criteriaAmount.value()
        if self.amount < n:
            self.ui.tableWidget.insertRow(n)
            self.ui.tableWidget.insertColumn(n)

            row_header_item = QTableWidgetItem("Критерий " + str(n))
            self.ui.tableWidget.setVerticalHeaderItem(n, row_header_item)
            col_header_item = QTableWidgetItem("Критерий " + str(n))
            self.ui.tableWidget.setHorizontalHeaderItem(n, col_header_item)

            self.ui.tableWidget.setColumnCount(n + 1)
            self.ui.tableWidget.setRowCount(n + 1)
        else:
            self.ui.tableWidget.removeRow(n)
            self.ui.tableWidget.removeColumn(n)
            self.ui.tableWidget.setColumnCount(n + 1)
            self.ui.tableWidget.setRowCount(n + 1)
        self.nulify_cells()
        self.amount = self.ui.criteriaAmount.value()
        self.change_headers()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec())