"""
    Qt main window
"""
from enum import Enum
from dataclasses import dataclass

from PyQt6.QtCore import Qt
from PyQt6.QtGui import (
    QAction,
    QActionGroup
)
from PyQt6.QtWidgets import (
    QMainWindow,
    QToolBar,
    QSplitter,
)

from werbanc.ui.qt.script_panel import ScriptPanel
from werbanc.ui.qt.chat_panel import ChatPanel

@dataclass
class ToolBarMixin:
    title: str
    shortcut: str

class ToolBar(ToolBarMixin, Enum):
    OVERVIEW = "Overview", "Ctrl+1"
    SCRIPT = "Script", "Ctrl+2"
    CHAT = "Chat", "Ctrl+3"
    WORKSPACE = "Workspace", "Ctrl+4"
    PROJECT = "Project", "Ctrl+5"

class MainWindow(QMainWindow):
    _title = "WerbanC"
    _default_size = (1100, 700)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self._title)
        self.resize(*self._default_size)
        self._setup_tool_bar()
        self._setup_overview_window()


    def _on_navigation(self, action: QAction) -> None:
        section = action.data()

        if section == ToolBar.OVERVIEW:
            self.script_panel.show()
            self.chat_panel.show()
        elif section == ToolBar.SCRIPT:
            self.script_panel.show()
            self.chat_panel.hide()
            self.script_panel.editor.setFocus()
        elif section == ToolBar.CHAT:
            self.chat_panel.show()
            self.script_panel.hide()
            self.chat_panel.message_input.setFocus()

    def _setup_tool_bar(self) -> None:
        toolbar = QToolBar("Navigation")
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        self.navigation_group = QActionGroup(self)
        self.navigation_group.setExclusive(True)

        for i, value in enumerate(ToolBar):
            action = QAction(value.title, self)
            action.setCheckable(True)
            action.setShortcut(value.shortcut)
            action.setToolTip(f"{value.title} {value.shortcut}")
            action.setData(value)

            self.navigation_group.addAction(action)
            toolbar.addAction(action)

            if value in (ToolBar.WORKSPACE, ToolBar.PROJECT):
                action.setEnabled(False)

            if i == 0:
                action.setChecked(True)

            self.navigation_group.triggered.connect(self._on_navigation)

    def _setup_overview_window(self) -> None:
        """
            Setup overview window with Script and chat panel
        """
        splitter = QSplitter(Qt.Orientation.Horizontal, self)
        self.script_panel = ScriptPanel(splitter)
        self.chat_panel = ChatPanel(splitter)

        splitter.addWidget(self.script_panel)
        splitter.addWidget(self.chat_panel)

        self.setCentralWidget(splitter)