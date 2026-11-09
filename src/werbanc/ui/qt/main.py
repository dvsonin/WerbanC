"""
    Qt ui main
"""
import sys

from PyQt6.QtWidgets import QApplication

from werbanc.ui.qt.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(app.style().standardPalette())

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())