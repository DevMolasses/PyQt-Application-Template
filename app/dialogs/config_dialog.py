"""Dialog window for application configuration."""

import os
import sys
from glob import glob

from icecream import ic
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (QComboBox, QDialog, QDialogButtonBox, QFormLayout,
                             QLabel, QSpinBox, QVBoxLayout)

from ui.toggle_switch import QToggleSwitch


class ConfigDialog(QDialog):
    """Dialog window for editing the application preferences (config)."""

    def __init__(self, config_handler):
        super().__init__()
        self._config = config_handler

        self.setWindowTitle("Edit Preferences")

        # Store original window theme and if it has changed
        self._original_theme = self._config.theme_filename
        self.window_theme_changed = False

        # Store user changes before saving
        self._pending_changes = {}

        self._create_widgets()
        self._create_layout()

    def _create_widgets(self):
        """Define all the widgets for the dialog and their functionality."""
        # Restore previous session window
        restore_window_label = QLabel("Restore window size and position:")
        restore_window_label.setToolTip(
            " Sets whether or not to save the current window size and \
                position to use as the initial size and location the next \
                time the app is launched.")
        self.restore_window_field = QToggleSwitch()
        self.restore_window_field.setFixedWidth(
            self.restore_window_field.sizeHint().width())
        self.restore_window_field.setChecked(self._config.window_restore)
        self.restore_window_field.stateChanged.connect(
            self._restore_window_changed)

        # Select window theme
        window_theme_label = QLabel("Window Theme:")
        self.window_theme_field = QComboBox()
        for key, value in self._get_window_themes().items():
            self.window_theme_field.addItem(key, value)
        idx = self.window_theme_field.findData(
            self._config.theme_filename)
        if idx > -1:
            self.window_theme_field.setCurrentIndex(idx)
        self.window_theme_field.currentTextChanged.connect(
            self._window_theme_changed)

        # Number of recent files
        num_recents_label = QLabel("Number of Recent Files to Store/View")
        self.num_recents_field = QSpinBox()
        self.num_recents_field.setMinimum(0)
        self.num_recents_field.setMaximum(30)
        self.num_recents_field.setValue(
            self._config.num_recents_to_show)
        self.num_recents_field.valueChanged.connect(self._num_recents_changed)

        # Collect all the form widgets for easy layout creation
        self.form_widgets = [(restore_window_label, self.restore_window_field),
                             (window_theme_label, self.window_theme_field),
                             (num_recents_label, self.num_recents_field)]

        # Save | Cancel buttons
        btn_box = (QDialogButtonBox.StandardButton.Save |
                   QDialogButtonBox.StandardButton.Cancel)
        self.button_box = QDialogButtonBox(btn_box)
        self.button_box.accepted.connect(self._on_save)
        self.button_box.rejected.connect(self.reject)

    def _create_layout(self):
        """Define the layout of the dialog."""
        central_layout = QVBoxLayout()

        form_layout = QFormLayout()
        for i, (label, field) in enumerate(self.form_widgets):
            form_layout.setWidget(i, QFormLayout.ItemRole.LabelRole, label)
            form_layout.setWidget(i, QFormLayout.ItemRole.FieldRole, field)
        central_layout.addLayout(form_layout)
        central_layout.addWidget(self.button_box)
        self.setLayout(central_layout)

    def _get_window_themes(self) -> dict:
        r"""
        Get the theme names and filenames from .\resources\styles\colors*.qss.

        Note
        ----
        This function is dependant on the following convention:
            - All files have the extension .qss indicating it is a PyQt style
            sheet.
            - A style template is used to define the stylesheet. Keywords are
            used with a leading @ symbol wherever a color, or other thematic
            attribute, is designated.
            - A seperate file is used to define the color pallete for each
            theme.
            - the color pallete file names must be formated as
            'colors_<theme identifier>.qss'.

        Returns
        -------
        dict
            Dictionary of themes formatted as {theme-name: theme-filepath}.

        """
        themes = {}
        for file in glob(".\\resources\\styles\\colors*.qss"):
            with open(file, 'r', encoding='utf-8') as file:
                contents = file.read()
            label = next((line.split("=")[1].strip()
                          for line in contents.split("\n")
                         if line.startswith('@theme-name')), "Unknown")
            themes[label] = os.path.basename(file.name)
        return themes

    @pyqtSlot()
    def _restore_window_changed(self):
        self._pending_changes['window_restore'] = (
            self.restore_window_field.isChecked()
        )

    @pyqtSlot()
    def _window_theme_changed(self):
        new_theme = ic(self.window_theme_field.currentData())
        self._pending_changes['theme_filename'] = new_theme
        self.window_theme_changed = new_theme != self._original_theme
        self.setStyleSheet(self._config.get_stylesheet(new_theme))

    @pyqtSlot(int)
    def _num_recents_changed(self, value):
        self._pending_changes['num_recents_to_show'] = value

    @pyqtSlot()
    def _on_save(self):
        """Apply changes and close dialog."""
        for key, value in self._pending_changes.items():
            setattr(self._config, key, value)

        self.accept()


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
    from core.app_config_handler import ConfigHandler

    class MainWindow(QMainWindow):
        """Main window class for testing purposes."""

        def __init__(self):
            super().__init__()
            self.setGeometry(100, 100, 200, 50)
            self.setWindowTitle("Configuration File Editor")
            button = QPushButton("Launch Editor")
            button.clicked.connect(self._launch_editor)
            self.setCentralWidget(button)

            self._config = ConfigHandler(".\\resources\\app_config.yaml")

        def _launch_editor(self):
            config_dialog = ConfigDialog(self._config, parent=self)

            if config_dialog.exec():
                print("Success")
                print(self._config)
            else:
                print("Cancelled")

        def set_style(self):
            """
            Update the application stylesheet.

            Returns
            -------
            None.

            """
            print(f"set_style logic here for theme_filename \
                  {self._config.theme_filename}")

    app = QApplication(sys.argv)

    default_font = QFont()
    default_font.setPointSize(12)
    app.setFont(default_font)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
