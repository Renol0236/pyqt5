#
import os

from PyQt5.Qt import QIcon
from PyQt5.QtCore import QFile, QTextStream, QSize
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QPushButton, QMessageBox


# Функция для центрирования окна, окно передается в аргумент
def center_window(window):
    screen = QDesktopWidget().screenGeometry()  # Получаем размер окна пользователя
    window_size = window.geometry()  # Получаем размер окна пользователя
    center_x = (screen.width() - window_size.width()) // 2
    center_y = (screen.height() - window_size.height()) // 2
    window.move(center_x, center_y)  # Перемещаем окно в центр.


# Функция для установки шрифта для каждого окна
# Принимает путь к шрифту, и его размер в пикселях, и окно, для вывода ошибок в их случае
def create_font(font_path, px, window):
    try:
        if os.path.isfile(font_path):
            mainfont = QFont() # Создание экземпляра класса шрифта
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1: # Проверка существует ли шрифт
                font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
                mainfont.setFamily(font_family) # Установка именно этого шрифта
                mainfont.setPointSize(px) # Установка размера шрифта
        # Обработка ошибок
            else:
                QMessageBox.critical(window, "Ошибка", "Не удалось загрузить шрифт: " + str(window))
                return QFont("Sans Serif", 16)
        else:
            QMessageBox.critical(window, "Ошибка", "Не найден файл шрифта для: " + str(window))

            return QFont("Sans Serif", 16)

        return mainfont
    except Exception as e:
        print(f'Utils.py: create_font error: {e}')
        return QFont("Sans Serif", 16)

# Фукнция загружает css файл, и возвращает переменную css
def load_css(name):
    css_file = QFile(name)
    css_file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(css_file)
    css = stream.readAll()
    css_file.close()
    return css

# Функция, которая устанавливает иконку
def set_icon(ui, widget_name, path_to_icon, width, height):
    icon = QIcon(path_to_icon)

    button = getattr(ui, widget_name)
    button.setIcon(icon)
    button.setIconSize(QSize(width, height))


# Класс для подсказки
class HintMessageBox(QMessageBox):
    def __init__(self, title, message):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(message)
        self.setIcon(QMessageBox.Information)
        self.addButton(QPushButton('OK'), QMessageBox.AcceptRole)
