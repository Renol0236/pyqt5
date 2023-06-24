# Импорт необходимых модулей
import os
import random # Функция choice для генерации пароля
import string # модуль, содержащий все доступные сиволы
import pyperclip # Модуль, для сохранения данных в буфер обмена

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox, QLineEdit, QCheckBox, \
    QSlider
from insert_history import * # БД
from utils import create_font, load_css, HintMessageBox # Вспомогательные функиии
from ui_history import Ui_History # Интерфейс


class Ui_Generator(object):
    def setupui(self, MainWindow):

        # Установка заголовка окна и его размеров
        MainWindow.setWindowTitle('Password Generator')
        MainWindow.setGeometry(300, 700, 400, 350)
        # Объявление переменных

        self.MainWindow = MainWindow
        self.lenght = 0
        self.password = ''

        # Создание БД
        self.Idb = IDataBase('database.db')

        # Загрузка CSS файла
        self.css = load_css('css/style_main.css')

        # Установка шрифта благодоря функции из utils.py
        self.main_font = create_font(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts/font.ttf'), 18, MainWindow)

        # Создание главного виджета
        self.main_widget = QWidget(MainWindow)

        # Создание главного лейаута с контентом
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setAlignment(Qt.AlignCenter)
        # Создание линни с паролем
        self.line = QLineEdit()
        self.line.setFont(self.main_font)
        self.line.setReadOnly(True)
        # Кнопка для генерации
        self.generate_button = QPushButton('Генерировать')
        self.generate_button.setFont(self.main_font)

        # Кнопка для копирования в буфер
        self.copy_button = QPushButton('Копировать')
        self.copy_button.setFont(self.main_font)

        # Текст с длиной пароля

        self.lenght_label = QLabel('Длина: ' + str(self.lenght))
        self.lenght_label.setFont(self.main_font)

        # Ползунок для длины пароля
        self.lenght_slider = QSlider(Qt.Horizontal)


        # Использовать числа
        self.use_number = QCheckBox("Использовать числа")
        self.use_number.setFont(self.main_font)

        # Использовать спец символы
        self.use_specs = QCheckBox('Использовать спец. символы')
        self.use_specs.setFont(self.main_font)

        #  История паролей
        self.history_button = QPushButton('История паролей')
        self.history_button.setFont(self.main_font)

        # Привязка виджетов к лейаутам
        self.main_layout.addWidget(self.line)
        self.main_layout.addWidget(self.copy_button)
        self.main_layout.addWidget(self.lenght_label)
        self.main_layout.addWidget(self.lenght_slider)
        self.main_layout.addWidget(self.generate_button)
        self.main_layout.addWidget(self.use_number)
        self.main_layout.addWidget(self.use_specs)
        self.main_layout.addWidget(self.history_button)


        # CSS
        self.main_widget.setStyleSheet(
            'background: qlineargradient(spread: pad, x1: 0, y1: 0, x2: 1, y2: 0, stop:'
            ' 0 rgba(39, 65, 196, 1), stop: 0.44 rgba(163, 81, 175, 1), stop:'
            ' 0.64 rgba(190, 43, 210, 1), stop: 0.92 rgba(187, 63, 251, 1));')
        self.line.setStyleSheet(self.css)
        self.generate_button.setStyleSheet(self.css)
        self.use_number.setStyleSheet(self.css)
        self.use_specs.setStyleSheet(self.css)
        self.copy_button.setStyleSheet(self.css)
        self.lenght_slider.setStyleSheet(self.css)
        self.history_button.setStyleSheet(self.css)

        # Привязка виджетов к функциям
        self.lenght_slider.valueChanged[int].connect(self.get_lenght)
        self.copy_button.clicked.connect(self.copy)
        self.generate_button.clicked.connect(lambda: self.generate(self.lenght))
        self.history_button.clicked.connect(self.open_history)

        # Создание окна с историей паролей
        self.ui_history = Ui_History()
        self.history_window = UiPassHistory(self.ui_history)
    # Открыть окно с историей действией
    def open_history(self):
        self.history_window.show()
    # Получить длину из ползунка
    def get_lenght(self, value):
        value = value // 3
        self.lenght = value
        self.lenght_label.setText(f'Длина: {str(self.lenght)}')

    # Копирует пароль, если он создан, иначе выводи ошибку.
    def copy(self):
        if self.password != '':
            pyperclip.copy(self.password)

            self.hint = HintMessageBox('Пароль скопировано', 'Пароль успешно скопирован в буфер обмена!')
            self.hint.exec_()
        else:
            QMessageBox.warning(self.MainWindow, 'Ошибка', 'Пароль не сгенерирован!')

    # Генерирует пароль
    def generate(self, lenght):
        chars = string.ascii_letters
        if self.use_number.checkState():
            chars += string.digits
        if self.use_specs.checkState():
            chars += string.punctuation

        password = ''.join(random.choice(chars) for _ in range(lenght))
        self.password = password

        self.Idb.pass_history_insert(password, self.ui_history)

        chars = string.ascii_letters

        self.line.setText(str(password))


# Класс для создания окна с историей
class UiPassHistory(QMainWindow):
    def __init__(self, ui_history):
        super().__init__()
        self.ui_history = ui_history
        self.ui_history.setupui(self, 'pass_history', 'Passwords History')
        self.setCentralWidget(self.ui_history.main_widget)
