"""main.py"""
import sys

from icecream import ic
from PyQt6.QtWidgets import QApplication

from app.main_window import MainWindow
from core.main_controller import MainController

ic.configureOutput(includeContext=True)
ic.enable()


def main():
    """Entry point of application."""
    # Initialize the application
    app = QApplication(sys.argv)

    # Instantiate the main components
    main_controller = MainController()
    main_window = MainWindow(main_controller)

    # Show the main window
    main_window.show()

    # Execute the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
