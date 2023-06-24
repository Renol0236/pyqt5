import inspect
import sqlite3
from datetime import datetime


# Функция, чтобы получить имя файла и метода в котором она вызвана, для отчета об ошибке
def get_frame():
    frame = inspect.currentframe()
    outer_frame = inspect.getouterframes(frame)[1]
    filename = outer_frame.filename
    method_name = outer_frame.function
    return filename, method_name

# Класс, для записи данных в БД
class IDataBase:
    def __init__(self, database):
        self.conn, self.cursor = self.create_connection(database)

    # Создание соеденения
    def create_connection(self, database):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        return conn, cursor

    # Запись истории калькулятора в БД
    def calc_history_insert(self, result, line, ui):
        try:
            time = datetime.now()
            time = time.strftime("%H:%M")

            self.cursor.execute('INSERT INTO calc_history VALUES(NULL, ?,?,?)', (result, line, time))
            self.conn.commit()

            # Вызов метода add_table_data
            ui.add_table_data('calc_history')
        except sqlite3.Error as e:
            filename, method_name = get_frame()
            print(f'\n\nОшибка в {filename}, метод: {method_name}\nError: {e}')

    # Запись истории паролей в БД
    def pass_history_insert(self, password, ui):
        try:
            time = datetime.now()
            time = time.strftime("%H:%M")

            self.cursor.execute('INSERT INTO pass_history VALUES(NULL, ?, ?)', (password, time))
            self.conn.commit()

            # Вызов метода add_table_data
            ui.add_table_data('pass_history')

        except sqlite3.Error as e:
            filename, method_name = get_frame()
            print(f'\n\nОшибка в {filename}, метод: {method_name}\nError: {e}')

    # Запись истроии конвертора в БД
    def currency_history_insert(self, result, froM, to, ui):
        try:
            time = datetime.now()
            time = time.strftime("%H:%M")

            self.cursor.execute('INSERT INTO currency_history VALUES(NULL, ?, ?, ?, ?)', (result, froM, to, time))
            self.conn.commit()

            # Вызов метода add_table_data
            ui.add_table_data('currency_history')

        except sqlite3.Error as e:
            filename, method_name = get_frame()
            print(f'\n\nОшибка в {filename}, метод: {method_name}\nError: {e}')

    # Запись истроии напоминаний в БД
    def notify_history_insert(self, title, expired, ui, text=None):
        try:

            time = datetime.now()
            time = time.strftime("%H:%M")

            if text is not None:
                self.cursor.execute('INSERT INTO notify_history VALUES(NULL, ?, ?, ?, ?)', (title, text, expired, time))
            else:
                self.cursor.execute('INSERT INTO notify_history VALUES(NULL, ?, NULL, ?, ?)', (title, expired, time))

            self.conn.commit()

            # Вызов метода add_table_data
            ui.add_table_data('notify_history')
        except sqlite3.Error as e:
            filename, method_name = get_frame()
            print(f'\n\nОшибка в {filename}, метод: {method_name}\nError: {e}')