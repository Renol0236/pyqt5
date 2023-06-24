import os

from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, QSpacerItem
from QCustomWidgets import QNowTime
from utils import center_window, create_font, load_css


class Ui_Main(object):
    def setupui(self, MainWindow):
        # Функция для создания кнопки (шаблон)
        def CreateButton(text):
            button = QPushButton(text)
            button.setFont(self.mainfont)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            return button

        # Установка заголовка окна и его размеров
        MainWindow.setWindowTitle('Buisness Helper')
        MainWindow.setGeometry(0, 0, 400, 350)

        # Центрирование окна на экране
        center_window(MainWindow)

        # Загрузка CSS файла
        css = load_css('css/style_main.css')

        # Создание главного виджета и его установка в центральную область окна
        self.main_widget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.main_widget)

        # Создание вертикального лейаута для главного виджета и его выравнивание
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setAlignment(Qt.AlignTop)

        # Создание горизонтального лейаута для заголовка и его настройка
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(QMargins(0, 5, 0, 0))

        # Создание вертикального лейаута для левой части основного контента и его выравнивание
        self.left_layout = QVBoxLayout()
        self.left_layout.setAlignment(Qt.AlignVCenter)
        self.left_layout.setContentsMargins(QMargins(10,0,0,35))

        # Создание вертикального лейаута для правой части основного контента и его выравнивание
        self.right_layout = QVBoxLayout()
        self.right_layout.setAlignment(Qt.AlignVCenter)
        self.right_layout.setContentsMargins(QMargins(10, 0, 0, 35))

        # Создание горизонтального лейаута для основного контента и его выравнивание
        self.main_content_layout = QHBoxLayout()
        self.main_content_layout.setAlignment(Qt.AlignCenter)

        # Установка шрифта благодоря функции из utils.py
        self.mainfont = create_font(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts/font.ttf'), 18, MainWindow)

        # Создание виджета для отображения текущего времени и его настройка
        self.time_label = QNowTime()
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFont(self.mainfont)
        self.time_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Создание кнопки для отображения информации и ее настройка
        self.info_button = CreateButton('Информация')
        self.info_button.setFixedSize(200, 55)

        # Создание кнопки для отображения курса валют и ее настройка
        self.currency_button = CreateButton('Конвертор валют')
        self.left_layout.addSpacing(65)

        # Создание кнопки для отображения заметок и ее настройка
        self.notify_button = CreateButton('Напоминания')
        self.right_layout.addSpacing(65)

        # Создание кнопки для отображения истории и ее настройка
        self.generator_button = CreateButton('Генераторй паролей')

        # Создание кнопки для отображения калькулятора и ее настройка
        self.calc_button = CreateButton('Калькулятор')

        # Добавление лейаутов в главный лейаут
        self.header_layout.addWidget(self.time_label)
        self.header_layout.addWidget(self.info_button)

        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addLayout(self.main_content_layout)

        self.main_content_layout.addLayout(self.left_layout)

        self.spacer_left_right = QSpacerItem(0, 100, QSizePolicy.Expanding, QSizePolicy.Minimum) # Создание пустого пространства между левой и правой частью

        self.main_content_layout.addItem(self.spacer_left_right)
        self.main_content_layout.addLayout(self.right_layout)
        # Применения CSS к элементам
        self.main_widget.setStyleSheet('background: qlineargradient(spread: pad, x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 rgba(39, 65, 196, 1), stop: 0.44 rgba(163, 81, 175, 1), stop: 0.64 rgba(190, 43, 210, 1), stop: 0.92 rgba(187, 63, 251, 1));')
        self.time_label.setStyleSheet('background: none; color: white;')
        self.info_button.setStyleSheet(css)
        self.currency_button.setStyleSheet(css)
        self.notify_button.setStyleSheet(css)
        self.generator_button.setStyleSheet(css)
        self.calc_button.setStyleSheet(css)
        # Добавление виджетов к лейаутат

        # Лейаут с двумя кнопками слева
        self.left_layout.addWidget(self.currency_button)
        self.left_layout.addItem(self.spacer_left_right) # Создание пустого пространства между кнопками
        self.left_layout.addWidget(self.generator_button)


        # Лейаут с двумя кнопками справа
        self.right_layout.addWidget(self.calc_button)
        self.right_layout.addItem(self.spacer_left_right) # Создание пустого пространства между кнопками
        self.right_layout.addWidget(self.notify_button)
