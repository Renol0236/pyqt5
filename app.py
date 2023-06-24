# Импорт необходимых модулей
import sys
from PyQt5.Qt import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow
from db_scripts import * # БД
from ui_calculator import Ui_Calc # Интерфейс
from ui_currency import Ui_Currency # Интерфейс
from ui_generator import Ui_Generator # Интерфейс
from ui_notify import Ui_Notify # Интерфейс
from ui_main import Ui_Main # Интерфейс
from utils import set_icon, HintMessageBox # Вспомогательные функиии
 # Основной класс главного окна
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Создание экземпляра базы данных
        db = FDataBase(database='database.db')
        # Создание экземпляра класса интерфейса главного окна
        self.ui_main = Ui_Main()
        self.ui_main.setupui(self)
         # Вызов методов этого класса
        self.connect_buttons()
         # Создание экземпляров окон
        self.calculate_window = CalculateWindow()
        self.generator_window = GeneratorWindow()
        self.currency_window = CurrenyWindow()
        self.notify_window = NotifyWindow()
         # Установка иконок для кнопок
        set_icon(self.ui_main, 'currency_button', 'icons/exchange.png', 36, 36)
        set_icon(self.ui_main, 'generator_button', 'icons/padlock.png', 32, 32)
        set_icon(self.ui_main, 'calc_button', 'icons/calculator.png', 32, 32)
        set_icon(self.ui_main, 'notify_button', 'icons/notes.png', 32, 32)
        set_icon(self.ui_main, 'info_button', 'icons/info.png', 32, 32)
     # функция для привязки событий к функциям
    def connect_buttons(self):
        self.ui_main.calc_button.clicked.connect(self.open_calculator) # Кнопка: 'Калькулятор' Функция: open_calculator
        self.ui_main.generator_button.clicked.connect(self.open_generator) # Кнопка: 'Генератор паролей' Функция: open_generator
        self.ui_main.currency_button.clicked.connect(self.open_currency) # Кнопка: 'Конвертор валют' функиця: open_currency
        self.ui_main.notify_button.clicked.connect(self.open_notify)
        self.ui_main.info_button.clicked.connect(self.create_info)
     # Информация
    def create_info(self):
        self.hint = HintMessageBox('Информация', 'Конвертор: \n     Чтобы конвертировать валюту, её нужно указывать в стандарте ISO 4217 Напоминания:\n      Для отображения напоминаний, нужно включить уведомления виндовс.')
        self.hint.exec_()
     # Переключения между окнами
    def open_calculator(self):
        self.calculate_window.show()
    def open_generator(self):
        self.generator_window.show()
    def open_currency(self):
        self.currency_window.show()
    def open_notify(self):
        self.notify_window.show()
 # Класс окна калькулятора
class CalculateWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui_calc = Ui_Calc()
        self.ui_calc.setupui(self)
        self.setWindowIcon(QIcon('icons/calculator.png'))
        self.setCentralWidget(self.ui_calc.main_widget)
 # Класс окна генератора паролей
class GeneratorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui_generator = Ui_Generator()
        self.ui_generator.setupui(self)
        self.setWindowIcon(QIcon('icons/padlock.png'))
        self.setCentralWidget(self.ui_generator.main_widget)
 # Класс окна конвертера валют
class CurrenyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui_currency = Ui_Currency()
        self.ui_currency.setupui(self)
        self.setWindowIcon(QIcon('icons/exchange.png'))
        self.setCentralWidget(self.ui_currency.main_widget)
 # Класс окна уведомлений
class NotifyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui_notify = Ui_Notify()
        self.ui_notify.setupui(self)
        self.setWindowIcon(QIcon('icons/notes.png'))
        self.setCentralWidget(self.ui_notify.main_widget)

 # Запуск приложения
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())