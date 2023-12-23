import sys
from decimal import Decimal, ROUND_HALF_UP

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QInputDialog, QMessageBox, QLabel, \
    QVBoxLayout, QDialog

from generated_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    """
    Главное окно приложения.
    """
    def __init__(self):
        """
        Инициализация интерфейса с подключением сгенерированного ui из QtDesigner
        """
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.tableWidget.horizontalHeader().setSectionsClickable(True)
        self.ui.tableWidget.verticalHeader().setSectionsClickable(True)
        self.ui.tableWidget.horizontalHeader().setSectionsMovable(False)
        self.ui.tableWidget.verticalHeader().setSectionsMovable(False)
        self.ui.tableWidget.horizontalHeader().sectionDoubleClicked.connect(self.edit_header)
        self.ui.tableWidget.verticalHeader().sectionDoubleClicked.connect(self.edit_header)

        self.setWindowTitle("Мастер анализа иерархий")
        self.ui.result_button.clicked.connect(self.result)
        self.ui.clear_button.clicked.connect(self.nulify_cells)

        action = QAction("Помогите!", self)
        self.ui.menuHelp.addAction(action)
        self.ui.menuHelp.triggered.connect(self.show_help)

        self.ui.criteriaAmount.valueChanged.connect(self.change_amount)
        self.amount = self.ui.criteriaAmount.value()

    def edit_header(self, logicalIndex):
        """
        Редактирует название критериев в таблице

        :param logicalIndex: индекс столбца/строки
        :return: None
        """
        n = self.ui.tableWidget.rowCount()
        if logicalIndex == n - 1:  # Строку и столбец с суммой нельзя редактировать
            return
        oldHeaders = [self.ui.tableWidget.verticalHeaderItem(i).text() for i in range(n)]
        oldHeaders2 = [self.ui.tableWidget.horizontalHeaderItem(i).text() for i in range(n)]
        newHeader, ok = QInputDialog.getText(self, 'Изменение данных', 'Название критерия:')
        if ok:
            # Сохраняет предыдущие названия, с новым измененным столбцом/строкой
            oldHeaders[logicalIndex] = newHeader
            oldHeaders2[logicalIndex] = newHeader
            self.ui.tableWidget.setVerticalHeaderLabels(oldHeaders)
            self.ui.tableWidget.setHorizontalHeaderLabels(oldHeaders2)

    def show_help(self):
        """
        Shows help picture widget

        :return: None
        """
        # Создаем дополнительное окно (QDialog)
        image_window = QDialog(self)
        image_window.setWindowTitle("Помощь")
        image_window.setGeometry(200, 200, 400, 400)
        label = QLabel(image_window)
        pixmap = QPixmap("src/help.png")
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(label)
        image_window.setLayout(layout)
        image_window.exec()

    def result(self):
        """
        Fill table with results

        :return: None (if error or success)
        """
        n = self.ui.tableWidget.rowCount()
        # Проходимся по всем критериям (кроме столбцов сумм)
        for i in range(n - 1):
            # Задаем единичную диагональ
            new_item = QTableWidgetItem("1")
            self.ui.tableWidget.setItem(i, i, new_item)

            # Берем значения из правого треугольника и вносим значения в минус первой степени в левую часть
            for j in range(0, i):
                item_in = self.ui.tableWidget.item(j, i)
                if item_in:
                    a_i = item_in.text()
                else:
                    a_i = "no data"
                b = -1
                try:
                    # Важная особенность питона заключается в том, что float не точное число
                    # Поэтому используется следующий подход
                    b = decimize(str(1 / Decimal(a_i)))
                except Exception:
                    message_box = QMessageBox()
                    message_box.setWindowTitle("Ошибка!")
                    message_box.setText(f"В данных есть ошибка (или значение одной из ячеек ноль)! "
                                        f"Пожалуйста исправьте значение ({j + 1}, {i + 1})!")
                    message_box.exec()
                    return
                item_out = QTableWidgetItem(str(b))
                self.ui.tableWidget.setItem(i, j, item_out)

        # Перейдем от таблицы к списку значений:
        summs = []  # Суммы построчно
        s = Decimal(0)  # Сумма всех значений критериев
        for i in range(n - 1):
            row_summ = 0
            for j in range(n - 1):
                item = self.ui.tableWidget.item(i, j)
                if item:
                    a = decimize(item.text())
                    s += a
                    row_summ += a
            summs.append(row_summ)
            print(f"Строка {i}. Сумма = {row_summ}")  # TODO: check readme
        result = Decimal(0)  # Итоговая сумма
        for i in range(n - 1):  # Сумма значений критериев
            row_summ = decimize(str(summs[i] / s))
            item = QTableWidgetItem(str(row_summ))
            self.ui.tableWidget.setItem(i, n - 1, item)
            result += row_summ
        item = QTableWidgetItem(str(decimize(str(result))))
        self.ui.tableWidget.setItem(n - 1, n - 1, item)

    def nulify_cells(self):
        """
        Обнуляет значения ячеек

        :return: None
        """
        for row in range(self.ui.tableWidget.rowCount()):
            for col in range(self.ui.tableWidget.columnCount()):
                item = self.ui.tableWidget.item(row, col)
                if item is not None:
                    item.setText("")

    def change_headers(self):
        """
        Автоматически изменяет названия критериев, а также столбец и строку с суммой

        :return: None
        """
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

    def change_amount(self):
        """
        Добавляет или убавляет строчку/строку

        :return: None
        """
        n = self.ui.criteriaAmount.value()
        if self.amount < n:  # Добавление нового критерия
            self.ui.tableWidget.insertRow(n)
            self.ui.tableWidget.insertColumn(n)

            row_header_item = QTableWidgetItem("Критерий " + str(n))
            self.ui.tableWidget.setVerticalHeaderItem(n, row_header_item)
            col_header_item = QTableWidgetItem("Критерий " + str(n))
            self.ui.tableWidget.setHorizontalHeaderItem(n, col_header_item)

            self.ui.tableWidget.setColumnCount(n + 1)
            self.ui.tableWidget.setRowCount(n + 1)
        else:  # Удаление нового критерия
            self.ui.tableWidget.removeRow(n)
            self.ui.tableWidget.removeColumn(n)
            self.ui.tableWidget.setColumnCount(n + 1)
            self.ui.tableWidget.setRowCount(n + 1)
        self.nulify_cells()  # Обнуляем сетку значений
        self.amount = self.ui.criteriaAmount.value()
        self.change_headers()  # Обновляем заголовки критериев


def decimize(n):
    return Decimal(n).quantize(Decimal(".01"), rounding=ROUND_HALF_UP)


if __name__ == "__main__":
    # выполняется в случае, когда файл является entry point и запускается как самостоятельное приложение.
    app = QApplication(sys.argv)  # экземпляр QApplication, который управляет приложением PyQt.
    window = MainWindow()  # экземпляр главного окна, отображаемого в приложении.

    window.show()  # отображаем главное окно.
    sys.exit(app.exec())  # цикл событий приложения, ожидающий события и взаимодействие пользователя
