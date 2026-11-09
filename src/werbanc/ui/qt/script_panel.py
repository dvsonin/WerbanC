"""
    Qt script panel
"""
from PyQt6.Qsci import QsciScintilla
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout
)

class ScriptPanel(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.editor = QsciScintilla(self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.editor)