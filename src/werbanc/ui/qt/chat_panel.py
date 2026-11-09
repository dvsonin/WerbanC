"""
    Qt chat panel
"""
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextBrowser,
    QPlainTextEdit,
    QPushButton
)

class ChatPanel(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.history = QTextBrowser(self)

        self.message_input = QPlainTextEdit(self)
        self.message_input.setPlaceholderText("Уточнение к ответу модели…")

        self.send_button = QPushButton("Отправить", self)
        self.send_button.setEnabled(False)  # Включим после подключения обработки.

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.history, stretch=3)
        layout.addWidget(self.message_input, stretch=1)
        layout.addWidget(self.send_button)