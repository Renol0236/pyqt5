# Импорт необходимых модулей
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QLineEdit
from currency_converter import CurrencyConverter # Библиотека, с конвертором валют
from insert_history import * # БД
from utils import create_font, load_css # Вспомогательные функиии
from ui_history import Ui_History # Интерфейс

class Ui_Currency(object):
    def setupui(self, MainWindow):

        # Установка заголовка окна и его размеров
        MainWindow.setWindowTitle('Currency Convertor')
        MainWindow.setGeometry(600, 500, 400, 350)

        # Главное окно
        self.MainWindow = MainWindow

        # Создание БД
        self.Idb = IDataBase('database.db')

        # Загрузка CSS файла
        self.css = load_css('css/style_currency.css')

        # Установка шрифта благодоря функции из utils.py
        self.main_font = create_font(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts/font.ttf'), 18,
                                     MainWindow)

        # Создание главного виджетa
        self.main_widget = QWidget(MainWindow)

        # Основной лейаута
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setAlignment(Qt.AlignCenter)

        # Входная валюта

        self.input_currency = QLineEdit()
        self.input_currency.setPlaceholderText('С валюты: ')
        self.input_currency.setFont(self.main_font)

        # Входное число денег

        self.input_amount = QLineEdit()
        self.input_amount.setPlaceholderText('Я отдам: ')
        self.input_amount.setFont(self.main_font)

        # Выходная валюта

        self.output_currency = QLineEdit()
        self.output_currency.setPlaceholderText('В валюту: ')
        self.output_currency.setFont(self.main_font)

        # Выходное число денег

        self.output_amount = QLineEdit()
        self.output_amount.setReadOnly(True)
        self.output_amount.setPlaceholderText('Я получу:')
        self.output_amount.setFont(self.main_font)

        # Кнопка конвертации
        self.convert_button = QPushButton('Конвертировать')
        self.convert_button.setFont(self.main_font)

        # Кнопка истории дейтсвий

        self.history_button = QPushButton('История конвертаций')
        self.history_button.setFont(self.main_font)

        # Привязка виджетов к лейаутам

        self.main_layout.addWidget(self.input_currency)
        self.main_layout.addWidget(self.input_amount)
        self.main_layout.addWidget(self.output_currency)
        self.main_layout.addWidget(self.output_amount)
        self.main_layout.addWidget(self.convert_button)
        self.main_layout.addWidget(self.history_button)

        # CSS
        self.main_widget.setStyleSheet(
            'background: qlineargradient(spread: pad, x1: 0, y1: 0, x2: 1, y2: 0, stop:'
            ' 0 rgba(39, 65, 196, 1), stop: 0.44 rgba(163, 81, 175, 1), stop:'
            ' 0.64 rgba(190, 43, 210, 1), stop: 0.92 rgba(187, 63, 251, 1));')
        self.output_currency.setStyleSheet(self.css)
        self.input_currency.setStyleSheet(self.css)
        self.output_amount.setStyleSheet(self.css)
        self.input_amount.setStyleSheet(self.css)
        self.convert_button.setStyleSheet(self.css)
        self.history_button.setStyleSheet(self.css)

        # Привязка кнопки к функции
        self.convert_button.clicked.connect(self.convert)
        self.history_button.clicked.connect(self.open_history)
        # Создание окна с историей паролей
        self.ui_history = Ui_History()
        self.history_window = UiCurrencyHistory(self.ui_history)

    # Открыть окно с историей действией
    def open_history(self):
        self.history_window.show()

    # функция конвертации валюты
    def convert(self):
        try:
            c = CurrencyConverter('eurofxref.csv')

            input_currency = self.input_currency.text().upper()
            output_currency = self.output_currency.text().upper()
            try:
                input_amount = float(self.input_amount.text())
            except:
                raise Exception('Неверный ввод суммы')

            try:
                self.output_amountINT = round(c.convert(input_amount, input_currency, output_currency), 2)
                self.output_amount.setText(str(self.output_amountINT))
                try:
                    self.Idb.currency_history_insert(self.output_amountINT, input_currency, output_currency,
                                                     self.ui_history)
                except:
                    raise Exception('Ошибка добавелния в БД')
            except ValueError:
                raise Exception("Неверный ввод валюты")

        except Exception as e:
            QMessageBox.critical(self.MainWindow, 'Ошибка', str(e))

# Класс для создания окна с историей
class UiCurrencyHistory(QMainWindow):
    def __init__(self, ui_history):
        super().__init__()
        self.ui_history = ui_history
        self.ui_history.setupui(self, 'currency_history', 'Currency History')
        self.setCentralWidget(self.ui_history.main_widget)
