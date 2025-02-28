"""main_window.py."""
import ctypes
import platform
from functools import partial

# from icecream import ic
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtWidgets import (QApplication, QFileDialog, QLabel, QMainWindow,
                             QPushButton, QVBoxLayout, QWidget)


class MainWindow(QMainWindow):
    """Main window."""

    def __init__(self, main_controller):
        super().__init__()

        if 'windows' in platform.system().lower():
            self.windows_specific_function()

        # Define attributes
        self.open_recent_menu = None

        self.main_controller = main_controller
        self.main_controller.window_theme_changed.connect(
            self._set_stylesheet)
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle('Application Title')

        self.app = QApplication.instance()

        self._set_stylesheet()

        self.status_bar = self.statusBar()
        # self.status_bar.setSizeGripEnabled(False)
        self.status_bar.setVisible(False)  # Remove this to use status bar

        self._create_menu()

        self._setup_ui()

        position, size = self.main_controller.get_window_position_size(
            self.app.primaryScreen().availableGeometry())
        self.move(position)
        self.resize(size)

        self.setWindowIcon(QIcon(".\\resources\\icons\\application_icon.svg"))

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        layout.addWidget(QLabel("Add widgets to the application!."))
        layout.addWidget(QPushButton("Needs Functionality"))

        # layout.addStretch()

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

        # Edit - Separator Bar
        edit_menu.addSeparator()

        # Edit - Preferences
        edit_preferences_action = QAction("&Preferences", self)
        edit_preferences_action.setShortcut(
            QKeySequence.StandardKey.Preferences)
        edit_preferences_action.triggered.connect(
            self.main_controller.on_edit_preferences)
        edit_menu.addAction(edit_preferences_action)

        # Help Menu
        help_menu = menu.addMenu("&Help")

        # Help - About
        help_about_action = QAction("&About...", self)
        help_about_action.triggered.connect(self.main_controller.on_about)
        help_menu.addAction(help_about_action)

    def _set_stylesheet(self):
        self.app.setStyleSheet(self.main_controller.get_stylesheet())

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
            len(self.main_controller.config_handler.recent_files) > 0)

    @pyqtSlot()
    def _quit_app(self):
        self.close()

###############################################################################
#                                Catch Events                                 #
###############################################################################
    def closeEvent(self, event):  # pylint: disable=invalid-name
        """Handle close event to clean up application."""
        self.main_controller.save_window_position_and_size(self)

        self.main_controller.delete_temp_files()

        event.accept()

###############################################################################
#                       System/Platform specific functions                    #
###############################################################################

    def windows_specific_function(self):
        """Run this function if the OS is Windows."""
        # Tell Windows to display the WindowIcon on the taskbar
        myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
