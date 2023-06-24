import inspect
import sqlite3


def get_frame():
    frame = inspect.currentframe()
    outer_frame = inspect.getouterframes(frame)[1]
    filename = outer_frame.filename
    method_name = outer_frame.function
    return filename, method_name

class FDataBase:
    def __init__(self, database):
        self.conn, self.cursor = self.create_connection(database)
        self.check_table_existence('pass_history')
        self.check_table_existence('calc_history')
        self.check_table_existence('currency_history')
        self.check_table_existence('notify_history')


# Создание подключения
    def create_connection(self, database):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        return conn, cursor

# Чтение sql файла
    def read_sql_file(self, filename):
        with open(filename, 'r') as file:
            sql_statements = file.read()
        return sql_statements

# Создание таблиц в sql файле
    def create_tables(self, filename):
        try:
            sql_statements = self.read_sql_file(filename)
            queries = sql_statements.split(";")
            print(queries)
            for query in queries:
                query = query.strip()
                print(query)
                if query:
                    self.cursor.execute(query)

            self.conn.commit()

        except sqlite3.Error as e:
            filename, method_name = get_frame()
            print(f'\n\nОшибка в {filename}, метод: {method_name}\nError: {e}')

    # Проверить наличие таблиы
    def check_table_existence(self, table_name):
        try:
            self.cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name=?', (table_name,))
            result = self.cursor.fetchone()
            if result is not None:
                return True
            else:
                self.create_tables('sql.sql')
        except sqlite3.Error as e:
            filename, method_name = get_frame()
            print(f'\n\nОшибка в {filename}, метод: {method_name}\nError: {e}')
    #
    # def create_table_if_not_exists(self, table_name):
    #     try:
    #         if not self.check_table_existence(table_name):
    #             self.cursor.execute(f"CREATE TABLE {table_name} (id INTEGER PRIMARY KEY, result INTEGER NOT NULL, line VARCHAR NOT NULL, tm VARCHAR NOT NULL)")
    #             self.conn.commit()
    #     except sqlite3.Error as e:
    #         filename, method_name = get_frame()
    #         print(f'\n\nОшибка в {filename}, метод: {method_name}\nError: {e}')

    # def get_all_history(self, table_name):
    #     try:
    #         if table_name == 'calc_history':
    #             self.cursor.execute(f'SELECT result, line, tm FROM {table_name}')
    #             result = self.cursor.fetchall()
    #             if result:
    #                 return result
    #         if table_name == 'pass_history':
    #             self.cursor.execute(f'SELECT pass, tm FROM {table_name}')
    #             result = self.cursor.fetchall()
    #             if result:
    #                 return result
    #         if table_name == 'currency_history':
    #             self.cursor.execute(f'SELECT result, "from", "to", tm FROM {table_name}')
    #             result = self.cursor.fetchall()
    #             if result:
    #                 return result
    #         if table_name == 'notify_history':
    #             self.cursor.execute(f'SELECT title, text, tm FROM {table_name}')
    #             result = self.cursor.fetchall()
    #             if result:
    #                 return result
    #     except sqlite3.Error as e:
    #         filename, method_name = get_frame()
    #         print(f'\n\nОшибка в {filename}, метод: {method_name}\nError: {e}')

    # Получить все строки из таблицы по имени
    def get_all_history(self, table_name):
        if table_name not in ['calc_history', 'pass_history', 'currency_history', 'notify_history']:
            raise ValueError('Неправильное имя таблицы')
        try:
            self.cursor.execute(f'SELECT * FROM {table_name}')
            result = self.cursor.fetchall()
            return result
        except sqlite3.Error as e:
            filename, method_name = get_frame()
            print(f'\n\nОшибка в {filename}, метод: {method_name}\nError: {e}')
            return []

    # Очистить строки таблицы по имени таблицы
    def clear_history(self, table_name):
        try:
            self.cursor.execute(f'DELETE FROM {table_name}')
            self.conn.commit()
        except sqlite3.Error as e:
            filename, method_name = get_frame()
            print(f'\n\nОшибка в {filename}, метод: {method_name}\nError: {e}')
