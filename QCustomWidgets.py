# Импорт виджетов, которые будует изменены
# Импорт функций методов необходимых для создания виджетов
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtWidgets import QLabel


# настраиваемый виджет QLabel, который отображает текущее время и обновляется каждую секунду с помощью QTime
class QNowTime(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignTop)  # Выравнивает виджета по верху своего контейнера

        self.timer = QTimer()  # Создание экземпляра класса QTImer
        self.timer.timeout.connect(
            self.update_time)  # Когда проходит одна секунда, таймер выполняет функцию update_time, тем самым обновляя текущее время
        self.timer.start(1000)  # Запуска таймера, который запускает строку выше каждые 1000 миллисекунд (1 секунда)

        self.update_time() # Обновленее текущего времени при запуске

    # Метод, который обновляет текущее время и устанавливает его как текст
    def update_time(self):
        current_time = QTime.currentTime() # Текущее время
        time_text = current_time.toString("hh:mm:ss") # Gреобразует текущее время в строковый формат часов, минут и секунд
        self.setText(f"{time_text}") # Устанавливает время

