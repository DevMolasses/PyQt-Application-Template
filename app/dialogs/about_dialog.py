"""Dialog Window to display the "About" information for the application.

The "About Dialog" pulls basic information from the calling class, and a
README.md file in the top-level directory. The information required in the
calling class is: __author__, __version__, __license__. If any of these
attributes are missing, either "Unkown" or None will be displayed in its place.

The README.md file is located in the top-level application directory and
contains the necessary documentation for the application. The markdown will be
rendered exaclty as written in the README file. If markdown syntax is not used
in the README file, the file will be displayed as if it was in markdown.
"""

import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import (QDialog, QDialogButtonBox, QHBoxLayout, QLabel,
                             QTabWidget, QTextBrowser, QVBoxLayout)


from app.metadata import __app_name__, __version__, __author__, __license__


class AboutDialog(QDialog):
    """Dialog for viewing application information."""

    def __init__(self, parent=None):
        super().__init__()
        self._parent = parent

        self.resize(QSize(650, 450))

        self._create_widgets()
        self._create_layout()

    def _create_widgets(self):
        """Define all the widgets for the dialog and their functionality."""
        # Label widgets (Title and logo)
        self._title = QLabel(__app_name__)
        _font = QFont()
        _font.setBold(True)
        _font.setPointSize(18)
        self._title.setFont(_font)
        self._title.setStyleSheet("font-size:32px;")
        self._title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._logo = QLabel()
        self._logo.setPixmap(
            QPixmap(".\\resources\\icons\\application_icon.svg"))
        self._logo.setMaximumSize(QSize(100, 100))
        self._logo.setScaledContents(True)

        # Tabs
        self._tabs = QTabWidget()

        # Overview Tab Widget
        self._overview = QTextBrowser()
        self._overview.setHtml(self._get_overview())
        self._overview.setStyleSheet("border: 0px;")
        self._tabs.addTab(self._overview, "Overview")

        # Readme Tab Widget
        readme = self._get_readme()
        if readme is not None:
            self._readme = QTextBrowser()
            self._readme.setMarkdown(readme)
            self._readme.setStyleSheet("border: 0px;")
            self._tabs.addTab(self._readme, "Readme")

        # License Tab Widget
        if self._get_license() is not None:
            self._license = QTextBrowser()
            # self._license.setMarkdown(self._get_license())
            self._license.setMarkdown(__license__)
            self._license.setStyleSheet("border: 0px;")
            self._tabs.addTab(self._license, "License")

        # Button Box
        self._button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self._button_box.accepted.connect(self.accept)

    def _create_layout(self):
        """Define the layout of the dialog."""
        central_layout = QVBoxLayout()

        logo_layout = QHBoxLayout()
        logo_layout.addWidget(self._logo)

        label_layout = QVBoxLayout()
        label_layout.addStretch()
        label_layout.addWidget(self._title)
        label_layout.addLayout(logo_layout)
        label_layout.addStretch()

        content_layout = QHBoxLayout()
        content_layout.addLayout(label_layout)
        content_layout.addWidget(self._tabs)

        central_layout.addLayout(content_layout)
        central_layout.addWidget(self._button_box)

        self.setLayout(central_layout)

    def _get_caller_module(self):
        """Get the module of the calling class."""
        return sys.modules[self._parent.__module__]

    def _get_license(self):
        """Retrieve the __license__ attribute of the calling class.

        Returns
        -------
        str
            Contents of the __license__ attribute of the calling class. If the
            attribute doesn't exist, default is None.

        """
        try:
            return self._get_caller_module().__license__
        except AttributeError:
            return None

    def _get_overview(self) -> str:
        """Construct the text that will be displayed in the "overview" tab.

        This method pulls the author and version attributes of the calling
        class to include in the overview text.

        Returns
        -------
        txt : str
            HTML String with the overview information.

        """
        txt = (
            "<div style='display: flex; flex-direction: column; "
            "justify-content: center; align-items: center; height: 100vh; "
            "text-align: center;'>"
            f"<p><strong>Author:</strong> {__author__}</p>"
            f"<p><strong>Version:</strong> {__version__}</p>"
            "</div>"
        )
        return txt

    def _get_readme(self) -> str:
        """Retrieve the contents of the README.md file if it exists.

        Returns
        -------
        str
            Full contents of the README.md file. Returns None if the file does
            not exist.
        """
        try:
            with open("README.md", "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return None


if __name__ == "__main__":
    # pylint: disable=ungrouped-imports
    from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

    class MainWindow(QMainWindow):
        """Main window class for testing purposes."""

        def __init__(self):
            super().__init__()
            self.setGeometry(100, 100, 200, 50)
            self.setWindowTitle("Dialog Launcher")
            button = QPushButton("Launch Dialog")
            button.clicked.connect(self._launch_editor)
            self.setCentralWidget(button)

        def _launch_editor(self):
            AboutDialog(parent=self).exec()

    app = QApplication(sys.argv)

    default_font = QFont()
    default_font.setPointSize(12)
    app.setFont(default_font)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
