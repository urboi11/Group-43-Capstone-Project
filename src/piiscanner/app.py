"""
Group 43 Senior Capstone Project
"""
import importlib.metadata
import sys
from .pyqt.piiscannerapp import MainWindow
from PySide6 import QtWidgets


def main():

    # Find the name of the module that was used to start the app
    app_module = sys.modules["__main__"].__package__
    # Retrieve the app's metadata
    metadata = importlib.metadata.metadata(app_module)

    QtWidgets.QApplication.setApplicationName(metadata["Formal-Name"])

    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
