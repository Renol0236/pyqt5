# Импорт необходимых модулей
import os
import time # Модуль временни, необходимый для работы напоминаний

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QDateTime, QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QDateTimeEdit, QSizePolicy, QApplication
from plyer import notification # Модуль, для создания уведомлений
from db_scripts import * # БД
from insert_history import IDataBase # БД
from utils import * # Вспомогательные функиии
from QCustomWidgets import QNowTime # Виджет с текущем временем
from ui_history import Ui_History # Интерфейс


class Ui_Notify(object):
    def setupui(self, MainWindow):
        # Настройки окна
        MainWindow.setWindowTitle('Notify')
        MainWindow.setGeometry(250, 100, 300, 250)

        # Переменные
        self.MainWindow = MainWindow
        self.Idb = IDataBase('database.db')
        self.css = load_css('css/style_notify.css')
        self.main_font = create_font(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts/font.ttf'), 18, MainWindow)

        # Главный виджет
        self.main_widget = QWidget(MainWindow)

        # Главный лейаут
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setAlignment(Qt.AlignCenter)

        # Текущее врермя
        self.time_label = QNowTime()
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFont(self.main_font)
        self.time_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Виджет для ввода даты и времент
        self.time_edit = QDateTimeEdit()
        self.time_edit.setDateTime(QDateTime.currentDateTime())

        # Создание кнопок через функцию
        self.notify_button = self.create_button('Создать напоминание')
        self.history_button = self.create_button('История напоминаний')

        # Строка для ввода
        self.title_line = QLineEdit()
        self.title_line.setPlaceholderText('Заголовок')

        # Строка для ввода
        self.text_line = QLineEdit()
        self.text_line.setPlaceholderText('Текст')

        # Привязка виджетов к лейауту
        self.main_layout.addWidget(self.time_label)
        self.main_layout.addWidget(self.title_line)
        self.main_layout.addWidget(self.text_line)
        self.main_layout.addWidget(self.time_edit)
        self.main_layout.addWidget(self.notify_button)
        self.main_layout.addWidget(self.history_button)

        # CSS
        self.main_widget.setStyleSheet(
            'background: qlineargradient(spread: pad, x1: 0, y1: 0, x2: 1, y2: 0, stop:'
            ' 0 rgba(39, 65, 196, 1), stop: 0.44 rgba(163, 81, 175, 1), stop:'
            ' 0.64 rgba(190, 43, 210, 1), stop: 0.92 rgba(187, 63, 251, 1));')
        self.time_edit.setStyleSheet(self.css)
        self.title_line.setStyleSheet(self.css)
        self.text_line.setStyleSheet(self.css)

        self.history_button.clicked.connect(self.open_history)
        self.notify_button.clicked.connect(self.create_notify)

        self.ui_history = Ui_History()
        self.history_window = UiNotifyHistory(self.ui_history)

    # Открытие окна с историей
    def open_history(self):
        self.history_window.show()

    # Функция для создания кнопки (шаблон)
    def create_button(self, text):
        button = QPushButton(text)
        button.setFont(self.main_font)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        button.setStyleSheet(self.css)
        return button

    # Фукнция для создания напоминания
    def create_notify(self):
        title = str(self.title_line.text())
        message = str(self.text_line.text())
        timestamp = self.time_edit.dateTime().toSecsSinceEpoch()

        # Запускаем отсчет до отправки уведомления в другом потоке
        countdown_thread = NotificationThread(title, message, timestamp)
        countdown_thread.start()


        self.Idb.notify_history_insert(title, str(self.time_edit.text()), self.ui_history, message) # Запись данных в БД

        self.hint = HintMessageBox(title='Напоминание создано', message='Напоминание создано успешно!')
        self.hint.exec_()

# Класс для создания окна с историей
class UiNotifyHistory(QMainWindow):
    def __init__(self, ui_history):
        super().__init__()
        self.ui_history = ui_history
        self.ui_history.setupui(self, 'notify_history', 'Notify History')
        self.setCentralWidget(self.ui_history.main_widget)

# Класс, для создания мультипоточности
class NotificationThread(QThread): # пункт b?
    finished = pyqtSignal() #Сигнал при завершении

    def __init__(self, title, message, timestamp):
        super().__init__()
        self.title = title
        self.message = message
        self.timestamp = timestamp

    # Отсчёт до уведомления
    def run(self):
        # Вычисляем задержку до указанного времени
        current_time = QDateTime.currentDateTime().toSecsSinceEpoch()
        delay = self.timestamp - current_time

        # Отсчёт до отправки уведомления
        for remaining_time in range(delay, 0, -1):

            time.sleep(1)

        # Отправка уведомления
        notification.notify(title=self.title, message=self.message, timeout=5)
        self.finished.emit()