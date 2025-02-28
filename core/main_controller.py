"""core\\main_controller.py."""

import os
from glob import glob

# from icecream import ic
from PyQt6.QtCore import QObject, pyqtSignal

from app.dialogs.config_dialog import ConfigDialog
from app.dialogs.about_dialog import AboutDialog
from core.app_config_handler import ConfigHandler


class MainController(QObject):
    """Main controller logic layer for application."""

    window_theme_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.config_handler = ConfigHandler(".\\resources\\app_config.yaml")

        # Launch sub-controllers and conncect their signals
        # TODO Add any needed subcontrollers here

    def delete_temp_files(self):
        """Delete all files in the temporary resources directory."""
        files = glob(".\\resources\\temp\\*")
        for file in files:
            os.remove(file)

    def get_stylesheet(self):
        """Retrieve stylesheet."""
        return self.config_handler.get_stylesheet()

    def get_window_position_size(self, screen_size):
        """Retreive main window size and position."""
        return self.config_handler.get_window_position_size(screen_size)

    def save_window_position_and_size(self, window):
        """Save the current window position and size to the app config file."""
        self.config_handler.window_position = (window.x(), window.y())
        self.config_handler.window_size = (
            window.width(), window.height())
        self.config_handler.save_config()

    def on_edit_preferences(self):
        """Handle Edit Preferences menu action."""
        config_dialog = ConfigDialog(
            self.config_handler)
        if config_dialog.exec():
            if config_dialog.window_theme_changed:
                self.window_theme_changed.emit()

    def on_about(self):
        """Handle Help About menu action."""
        AboutDialog().exec()
