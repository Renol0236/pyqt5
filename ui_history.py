# Импорт необходимый модулей
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem
from db_scripts import * # БД
from utils import create_font, load_css # Вспомогательные функиии


class Ui_History(object):
    def setupui(self, MainWindow, table_db, title):
        # Размеры окна и навание окна
        MainWindow.setWindowTitle(title)
        MainWindow.setGeometry(200, 200, 575, 400)

        # Создание базы данных
        self.db = FDataBase('database.db')
        self.table_db = table_db
        # Загрузка шрифта
        self.main_font = create_font(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts/font.ttf'), 18, MainWindow)
        # Загрузка css файла
        self.css = load_css('css/style_calc.css')
        # Создание главного виджета
        self.main_widget = QWidget()

         # Создание главного лейаута с контентом
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setAlignment(Qt.AlignCenter)

         # Создание таблицы с историей
        self.table_history = QTableWidget()
        self.table_history.setFont(self.main_font)

         # Кнопка для очисти БД
        self.button_clear = QPushButton('Очистить')
        self.button_clear.setFont(self.main_font)
        self.button_clear.clicked.connect(lambda: self.clear_history_ui(self.table_db))
         # Привязка виджетов к лейаутам
        self.main_layout.addWidget(self.table_history)
        self.main_layout.addWidget(self.button_clear)
         # Заполнение таблицы Qt данными из базы данных
        self.add_table_data(self.table_db)


    # Заполнение таблицы по её названию
    def add_table_data(self, table_name):
        try:
            self.table_history.clearContents()
            rows = self.db.get_all_history(table_name)
            self.table_history.setRowCount(len(rows))
            self.table_history.setColumnCount(len(rows[0]))
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.table_history.setItem(i, j, item)

            print('addded', +str(table_name))
        except:
            pass

    # Удаление строк из таблицы по названию
    def clear_history_ui(self, table_name):
        try:
            self.db.clear_history(table_name)
            self.table_history.clearContents()
            self.table_history.setRowCount(0)  # Установка количества строк таблицы в 0
            self.table_history.setColumnCount(0)  # Установка количества столбцов таблицы в 0
            self.table_history.update()  # Обновление таблицы после очистки
        except sqlite3.Error as e:
            print("Ошибка в методе очистки истории калькулятора БД: " + str(e))
