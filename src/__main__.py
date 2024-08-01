"""Main function to build and show the application."""

__license__ = """
Enter license here.
"""
__author__ = "Author Name"
__version__ = 0.0


import sys
import os

# Change the working directory to the main app directory if running this module
# directly.
if __name__ == "__main__":
    os.chdir("..\\")

import ctypes
from functools import partial
from PyQt6.QtWidgets import (QApplication, QFileDialog, QMainWindow)
from PyQt6.QtGui import QAction, QFont, QIcon, QKeySequence
from PyQt6.QtCore import pyqtSlot, QPoint, QSize, Qt, QThreadPool
from src.custom_widgets.toggle_switch import QToggleSwitch
from src.config_handler import ConfigHandler
from src.custom_widgets.config_dialog import ConfigDialog
from src.custom_widgets.about_dialog import AboutDialog


class MainWindow(QMainWindow):
    """Main class for the application."""

    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("My Application")

        self.config_handler = ConfigHandler()

        self.app = QApplication.instance()

        self._set_style()

        if self.config_handler.window_restore:
            x, y, = self.config_handler.window_position
            width, height = self.config_handler.window_size
            self.move(QPoint(x, y))
            self.resize(QSize(width, height))
        else:
            screen_gm = self.app.primaryScreen().availableGeometry()
            width = int(min(screen_gm.width() * .5, 1600))
            height = int(min(screen_gm.height() * .8, 1200))
            self.resize(QSize(width, height))
            frame_gm = self.frameGeometry()
            center_point = screen_gm.center()
            frame_gm.moveCenter(center_point)
            self.move(frame_gm.topLeft())

        self.setWindowIcon(QIcon(".\\resources\\application_icon.svg"))

        # Build the GUI
        self._create_menu()
        self._create_widgets()
        self._create_layout()

    def _create_menu(self):
        menu = self.menuBar()

        # File Menu
        file_menu = menu.addMenu("&File")
        file_menu.aboutToShow.connect(self._show_hide_recents)

        # File - Open
        file_open_action = QAction("&Open...", self)
        file_open_action.setShortcut(QKeySequence.StandardKey.Open)
        file_open_action.triggered.connect(self._open_file)
        file_menu.addAction(file_open_action)

        # File - Open Recent Menu
        self.open_recent_menu = file_menu.addMenu("Open &Recent")
        self.open_recent_menu.aboutToShow.connect(
            self._populate_open_recent_menu)
        self.open_recent_menu.setToolTipsVisible(True)

        # File - Close
        file_close_action = QAction("&Close", self)
        file_close_action.setShortcut(QKeySequence.StandardKey.Close)
        file_close_action.triggered.connect(self._close_file)
        file_menu.addAction(file_close_action)

        # File - Seperator Bar
        file_menu.addSeparator()

        # File - Quit
        file_quit_action = QAction("&Quit", self)
        file_quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        file_quit_action.triggered.connect(self._quit_app)
        file_menu.addAction(file_quit_action)

        # Edit Menu
        edit_menu = menu.addMenu("&Edit")

        # Edit - Preferences
        edit_preferences_action = QAction("&Preferences", self)
        edit_preferences_action.setShortcut(
            QKeySequence.StandardKey.Preferences)
        edit_preferences_action.triggered.connect(self._edit_preferences)
        edit_menu.addAction(edit_preferences_action)

        # Help Menu
        help_menu = menu.addMenu("&Help")

        # Help - About
        help_about_action = QAction("&About...", self)
        help_about_action.triggered.connect(self._about)
        help_menu.addAction(help_about_action)

    def _create_widgets(self):
        pass

    def _create_layout(self):
        pass

    def _set_style(self):
        with open(".\\resources\\styles\\style_template.qss", "r") as file:
            style = file.read()

        theme = self.config_handler.theme_filename
        with open(f".\\resources\\styles\\{theme}", "r") as file:
            colors = file.read()

        color_list = [tuple(line.replace(" = ", "=").split("="))
                      for line in colors.split("\n")]

        for lbl, clr in color_list:
            style = style.replace(lbl, clr)

        self.app.setStyleSheet(style)

###############################################################################
#                                Widget Slots                                 #
###############################################################################

###############################################################################
#                                Action Slots                                 #
###############################################################################
    @pyqtSlot()
    def _open_file(self, filepath=None):
        """Handle activating the open file action."""
        # Launch a file dialog to select the file to open.
        if filepath is None:
            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
            file_dialog.setMimeTypeFilters(["image/jpeg",
                                            "image/png",
                                            "image/svg+xml",
                                            "application/octet-stream"])
            # file_dialog.setNameFilter("Qt Style Sheets (*.qss)")

            if file_dialog.exec():
                for file in file_dialog.selectedFiles():
                    print(file)
                    self.config_handler.add_recent_file(file)
        else:
            self.config_handler.add_recent_file(filepath)
            print("Open", filepath)

    @pyqtSlot()
    def _close_file(self):
        print("Perform close action here...")

    @pyqtSlot()
    def _populate_open_recent_menu(self):
        """Generate entries for "Open Recent" menu with their actions."""
        # Step 1: Clear the menu of the old entries
        self.open_recent_menu.clear()

        # Step 2: Create the actions
        actions = []
        for filename, filepath in self.config_handler.recent_files.items():
            action = QAction(filename, self)
            action.triggered.connect(partial(self._open_file, filepath))
            action.setToolTip(filepath)
            actions.append(action)

        # Step 3: Add actions to the menu
        self.open_recent_menu.addActions(actions)

        # Step 4: Add clear recents action
        self.open_recent_menu.addSeparator()
        clear_recents_action = QAction("Clear List...", self)
        clear_recents_action.triggered.connect(self._clear_recent_files)
        self.open_recent_menu.addAction(clear_recents_action)

    @pyqtSlot()
    def _clear_recent_files(self):
        self.config_handler.recent_files = {}

    @pyqtSlot()
    def _show_hide_recents(self):
        self.open_recent_menu.menuAction().setVisible(
            len(self.config_handler.recent_files) > 0)

    @pyqtSlot()
    def _edit_preferences(self):
        config_dialog = ConfigDialog(self.config_handler, parent=self)
        config_dialog.exec()

    @pyqtSlot()
    def _about(self):
        AboutDialog(parent=self).exec()

    @pyqtSlot()
    def _quit_app(self):
        self.close()

###############################################################################
#                                Catch Events                                 #
###############################################################################
    def closeEvent(self, event):
        """Event handler for an Application Close Event.

        Capture the closeEvent to save the current window position and size
        before the window closes and that information is lost.
        """
        self.config_handler.window_position = (self.x(), self.y())
        self.config_handler.window_size = (self.width(), self.height())
        self.config_handler.save_config()
        event.accept()


def main():
    """Entry point to the application."""
    # Assign an application ID that will be uniquely identified by the taskbar
    appid = u"Organization.Application"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

    # Create the application object
    app = QApplication(sys.argv)

    # Set the default font properties
    default_font = QFont()
    default_font.setPointSize(12)
    app.setFont(default_font)

    # Create and show the main window object
    main_window = MainWindow()
    main_window.show()

    # Execute the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
