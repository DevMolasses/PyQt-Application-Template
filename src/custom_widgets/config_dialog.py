"""Dialog window for application configuration."""

import sys
import os

# Change the working directory to the main app directory if running this module
# directly.
if __name__ == "__main__":
    os.chdir("..\\..\\")

from PyQt6.QtWidgets import (QDialog, QDialogButtonBox, QVBoxLayout,
                             QFormLayout, QLabel, QComboBox, QSpinBox)
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QFont
from src.custom_widgets.toggle_switch import QToggleSwitch

from glob import glob


class ConfigDialog(QDialog):
    """Dialog window for editing the application preferences (config)."""

    def __init__(self, config, parent=None):
        super().__init__()
        self._config = config
        self._parent = parent

        self.setWindowTitle("Edit Preferences")

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
        self.restore_window_field.setChecked(
            self._config.get_config_field('window_restore'))
        self.restore_window_field.stateChanged.connect(
            self._restore_window_changed)

        # Select window theme
        window_theme_label = QLabel("Window Theme:")
        self.window_theme_field = QComboBox()
        # self.window_theme_field.addItems(self._get_window_themes())
        for key, value in self._get_window_themes().items():
            self.window_theme_field.addItem(key, value)
        idx = self.window_theme_field.findData(
            self._config.get_config_field('theme_filename'))
        if idx > -1:
            self.window_theme_field.setCurrentIndex(idx)
        self.window_theme_field.currentTextChanged.connect(
            self._window_theme_changed)

        # Number of recent files
        num_recents_label = QLabel("Number of Recent Files to Store/View")
        self.num_recents_field = QSpinBox()
        self.num_recents_field.setMinimum(0)
        self.num_recents_field.setMaximum(30)
        self.num_recents_field.setValue(self._config.num_recents_to_show)
        self.num_recents_field.valueChanged.connect(self._num_recents_changed)


        # Collect all the form widgets for easy layout creation
        self.form_widgets = [(restore_window_label, self.restore_window_field),
                             (window_theme_label, self.window_theme_field),
                             (num_recents_label, self.num_recents_field)]

        # SAve | Cancel buttons
        btn_box = (QDialogButtonBox.StandardButton.Save |
                   QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox = QDialogButtonBox(btn_box)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def _create_layout(self):
        """Define the layout of the dialog."""
        central_layout = QVBoxLayout()

        form_layout = QFormLayout()
        for i, (label, field) in enumerate(self.form_widgets):
            form_layout.setWidget(i, QFormLayout.ItemRole.LabelRole, label)
            form_layout.setWidget(i, QFormLayout.ItemRole.FieldRole, field)
        central_layout.addLayout(form_layout)
        central_layout.addWidget(self.buttonBox)
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
        files = glob(".\\resources\\styles\\colors*.qss")
        themes = {}
        for file in files:
            with open(file, 'r') as file:
                contents = file.read()
            content_list = [tuple(line.replace(" = ", "=").split("="))
                            for line in contents.split("\n")]
            label_idx = [item[0] for item in content_list].index('@theme-name')
            label = content_list[label_idx][1]
            themes[label] = os.path.split(file.name)[1]
        return themes

    @pyqtSlot()
    def _restore_window_changed(self):
        self._config.window_restore = self.restore_window_field.isChecked()

    @pyqtSlot(str)
    def _window_theme_changed(self, key):
        self._config.theme_filename = self.window_theme_field.currentData()
        self._parent._set_style()

    @pyqtSlot(int)
    def _num_recents_changed(self, value):
        self._config.num_recents_to_show = value

    @property
    def config(self):
        """
        Property to access stored configuration dictionary.

        Returns
        -------
        dict
            The full contents of the configuration file.

        """
        return self._config


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
    from src.config_handler import ConfigHandler

    class MainWindow(QMainWindow):
        """Main window class for testing purposes."""

        def __init__(self):
            super().__init__()
            self.setGeometry(100, 100, 200, 50)
            self.setWindowTitle("Configuration File Editor")
            button = QPushButton("Launch Editor")
            button.clicked.connect(self._launch_editor)
            self.setCentralWidget(button)

            self._config = ConfigHandler()

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
