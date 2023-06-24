import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, QMessageBox, \
    QGridLayout, QLineEdit
from db_scripts import FDataBase
from insert_history import IDataBase
from ui_history import Ui_History
from utils import create_font, load_css


class Ui_Calc(object):
    def setupui(self, MainWindow):
        # Установка названия окна

        MainWindow.setWindowTitle('Calculator')
        # Объявления переменных
        self.db = FDataBase(database='database.db')
        self.Idb = IDataBase(database='database.db')
        self.result = ''

        self.buttons = [
                        '7', '8', '9', '*',
                        '4', '5', '6', '+',
                        '1', '2', '3', '-',
                        '0', '.', '/', '=',
                        'C']

        # Загрузка шрифта
        self.main_font = create_font(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts/font.ttf'), 18, MainWindow)

        # Загрузка css файла
        self.css = load_css('css/style_calc.css')

        # Создание главного виджета
        self.main_widget = QWidget(MainWindow)

        # Создание главного лейаута с контентом
        self.main_layout = QVBoxLayout(self.main_widget)

        # Создание лейатуа для строки
        self.line_layout = QHBoxLayout()
        # Создание сетки с кнопками для калькулятора
        self.grid_layout = QGridLayout()
        # Создание лейаута для кнопки снизу
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setAlignment(Qt.AlignCenter)

        # Привязка лейаутов друг к другу
        self.main_layout.addLayout(self.line_layout)
        self.main_layout.addLayout(self.grid_layout)
        self.main_layout.addLayout(self.bottom_layout)
        
        # Создание строки для ввода чисел
        self.string_calc = QLineEdit()
        self.string_calc.setReadOnly(True)

        #Кнопка с историей
        self.history_button = QPushButton('История действий')
        self.history_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # Привязка виджетов к лейаутоам
        self.line_layout.addWidget(self.string_calc)
        self.bottom_layout.addWidget(self.history_button)
        #CSS
        self.main_widget.setStyleSheet('background: qlineargradient(spread: pad, x1: 0, y1: 0, x2: 1, y2: 0, stop: '
                                       '0 rgba(39, 65, 196, 1), stop: 0.44 rgba(163, 81, 175, 1), stop: 0.64 rgba(190, 43, 210, 1), '
                                       'stop: 0.92 rgba(187, 63, 251, 1));')
        self.string_calc.setStyleSheet(self.css)
        self.history_button.setStyleSheet(self.css)
        # Создание кнопкок для калькулятора, благодаря циклу
        positions = [(i, j) for i in range(5) for j in range(4)]
        for position, button in zip(positions, self.buttons):
            btn = self.create_button(button)
            self.grid_layout.addWidget(btn, *position)

        # Создание экземпляра класса окна с результатами
        self.ui_history = Ui_History()
        self.history_window = CalcHistoryWindow(self.ui_history)

        # Привязка кнопок к функциям
        self.history_button.clicked.connect(self.open_history)

    # Открыть окно с историей действией
    def open_history(self):
        self.history_window.show()

    # Шаблон для создания кнопки
    def create_button(self, text):
        button = QPushButton(text)
        button.setFont(self.main_font)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        button.clicked.connect(lambda: self.button_clicked(text))
        button.setStyleSheet(self.css)
        return button

    # Функция, которая срабатывает при каждом клике на кнопку из сетки (калькулятора)
    def button_clicked(self, button_text):
        try:
            if button_text in self.buttons:
                if button_text != '=' and button_text != 'C':
                    self.result += str(button_text)
                    self.string_calc.setText(str(self.result))
                if button_text == 'C':
                    self.result = ''
                    self.string_calc.setText('')
                if button_text == '=':
                    self.string_calc.setText(self.calculate())

        except ZeroDivisionError:
            QMessageBox.warning(self.main_widget, 'Ошибка', 'Деление на ноль невозможно')
            self.result = ''
            self.string_calc.setText('')

    # Функция для рассчёта суммы
    def calculate(self):
        try:
            result = round(eval(self.result), 3)
            self.Idb.calc_history_insert(result, self.result, self.ui_history) # из файла insert_history, запись данных в БД
            self.result = str(result)
            return str(result)
        except:
            QMessageBox.warning(self.main_widget, 'Ошибка', 'Некорректный ввод')
            self.result = ''
            self.string_calc.setText('')
# Класс для создания окна с историей
class CalcHistoryWindow(QMainWindow):
    def __init__(self, ui_history):
        super().__init__()
        self.ui_history = ui_history
        self.ui_history.setupui(self, 'calc_history', 'Calculator History')
        self.setCentralWidget(self.ui_history.main_widget)