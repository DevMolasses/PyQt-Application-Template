r"""src\config_handler.py."""
__author__ = "Trever Stewart"
__version__ = 1.0

import copy
import getpass
import os

import yaml
# from icecream import ic
from PyQt6.QtCore import QPoint, QSize


class ConfigHandler:
    """Handle all configuration file needs."""

    # Declare parameters
    _username = None
    _style_template_path = ".\\resources\\styles\\style_template.qss"
    _down_arrow_template_path = ".\\resources\\icons\\down-arrow-template.svg"
    _button_add_icon_path = ".\\resources\\icons\\plus-symbol-template.svg"
    _button_delete_icon_path = ".\\resources\\icons\\minus-symbol-template.svg"

    STARTER_CONFIG = {"theme_filename": "colors_light.qss",
                      "window_restore": False,
                      "window_x": 100,
                      "window_y": 100,
                      "window_width": 1600,
                      "window_height": 1200,
                      "recent_files": {},
                      "num_recents_to_show": 10}

    def __init__(self, config_filepath):
        try:
            self._username = getpass.getuser()
        except Exception:
            self._username = "DEFAULT"

        self.config_filepath = config_filepath
        self.temp_dir = ".\\resources\\temp\\"
        os.makedirs(self.temp_dir, exist_ok=True)

        try:
            with open(self.config_filepath, 'r') as file:
                self.config = yaml.safe_load(file)
        except FileNotFoundError:
            self.config = {"DEFAULT": copy.deepcopy(self.STARTER_CONFIG)}
            self.save_config()

        if self.username not in self.config:
            self.config[self.username] = self.STARTER_CONFIG
            self.save_config()

    def get_stylesheet(self, theme_filename: str = None) -> str:
        """Retrieve and format stylesheet string based on theme in config file.

        This function is dependent on having a style_template.qss with keywords
        for the various colors and other modification. The format of the
        keywords is @key-words-here. The mapping of the keywords to their
        associated colors happens in a theme qss file with the format
        @key-word-here = #ffffff.

        Returns
        -------
        str
            Complete stylesheet string that can be passed to an
            app.setStyleSheet() method.

        """
        if theme_filename is None:
            theme_filename = self.theme_filename
        with open(self._style_template_path, 'r') as file:
            style = file.read()

        # with open(self._down_arrow_template_path, 'r') as file:
        #     svg = file.read()

        with open(f".\\resources\\styles\\{theme_filename}", 'r') as file:
            colors = file.read()

        color_list = [tuple(line.replace(" = ", "=").split("="))
                      for line in colors.split("\n")]

        svg_templates = {
            "@button-plus-icon": self._button_add_icon_path,
            "@button-minus-icon": self._button_delete_icon_path,
            "@combobox-down-arrow": self._down_arrow_template_path
            }

        processed_svgs = {}

        for lbl, clr in color_list:
            if lbl in svg_templates:
                with open(svg_templates[lbl], 'r') as svg_file:
                    svg_content = svg_file.read()
                svg_content = svg_content.replace(lbl, clr)
                svg_path = f"{self.temp_dir}{lbl[1:]}-in-use.svg"
                with open(svg_path, "w") as temp_file:
                    temp_file.write(svg_content)
                url = "url(" + svg_path.replace("\\", "/") + ")"
                processed_svgs[lbl] = url

        for lbl, clr in color_list:
            if lbl in processed_svgs:
                style = style.replace(lbl, processed_svgs[lbl])
            else:
                style = style.replace(lbl, clr)

        return style

    def get_window_position_size(self, screen_size):
        """Retreive main window size and position."""
        if self.window_restore:
            x, y = self.window_position
            width, height = self.window_size
        else:
            x, y = (20, 20)
            width = int(min(screen_size.width() * .5, 1600))
            height = int(min(screen_size.height() * .8, 1200))
        return (QPoint(x, y), QSize(width, height))

    def add_recent_file(self, filepath: str):
        """Add a filepath to the recent_files list in the configuration file.

        Parameters
        ----------
        filepath : str
            The absolute filepath to the recently opened file.

        """
        # Split the filename from the path
        _, filename = os.path.split(filepath)

        try:
            # Look for the filepath in the list of recent files
            # Will throw exception if filepath is not in the list
            file_list = list(self.get_config_field("recent_files").values())
            idx = file_list.index(filepath)

            # Create a temp list to rearrange the order
            temp_list = list(self.get_config_field("recent_files").items())

            # Move the filepath from it's current location to index 0
            temp_list.insert(0, temp_list.pop(temp_list.index(temp_list[idx])))

            # Update list in configuration
            self.recent_files = dict(temp_list)
        except ValueError:
            # Enters when the filepath is not alread in the recent files list

            # Create a dict of the new filepath for easier reference later
            new_file = {filename: filepath}

            # Place the new file at the top of the recent files list
            self.recent_files = {**new_file, **self.recent_files}

            # Truncate recent_files if needed
            while len(self.recent_files) > self.num_recents_to_show:
                self.recent_files.popitem()

    def save_config(self):
        """
        Save the current configuration to file.

        Returns
        -------
        None.

        """
        if self.username != "DEFAULT":
            with open(self.config_filepath, 'w') as file:
                yaml.dump(self.config, file, sort_keys=False)

    def get_config_field(self, field: str):
        """Get the value associated with the provided field.

        Parameters
        ----------
        field : str
            Name of the field to retrieve value for.

        Returns
        -------
        obj
            The value associated with the given field. Value type will match
            what is stored in the dictionary.

        """
        try:
            return self.config[self.username][field]
        except KeyError:
            # Key isn't in config file, so add it
            value = self.STARTER_CONFIG[field]
            self.set_config_field(field, value)
            return value

    def set_config_field(self, field: str, value):
        """Set the value associated with the provided field.

        Parameters
        ----------
        field : str
            Name of the field to set the value for.
        value : obj
            Value to store in the field. Can be any value type that can be
            stored in a dictionary.

        Returns
        -------
        None.

        """
        self.config[self.username][field] = value

    def set_config_fields(self, fields, values):
        """Set the value accociated with multiple fields.

        Parameters
        ----------
        fields : Iterable
            Iterable of field names to set the value for.
        values : Iterable
            Iterable of values to be stored in their respective fields.

        Note
        ----
        The size and order of the fields and values must be the same to
        ensure accuracy of the stored information.

        Returns
        -------
        None.

        """
        for field, value in zip(fields, values):
            self.set_config_field(field, value)

    def __repr__(self) -> str:
        """Redefine what is displayed if ConfigHandler is printed.

        Build a string that prints a 'pretty', nested dictionary without the
        curly braces.
        """
        msg = ""
        for a in self.config:
            if msg != "":
                msg += "\n"
            msg += f"{a}:\n    "
            msg += str(self.config[a]).replace(", ", "\n    ")
        return msg.replace("{", "").replace("}", "")

###############################################################################
#                     Define property setters and getters                     #
###############################################################################

    @property
    def num_recents_to_show(self):
        """How many recent files should be visible in the menu."""
        return self.get_config_field("num_recents_to_show")

    @num_recents_to_show.setter
    def num_recents_to_show(self, value: int):
        self.set_config_field("num_recents_to_show", value)

    @property
    def recent_files(self):
        """List of recently opened files."""
        return self.get_config_field('recent_files')

    @recent_files.setter
    def recent_files(self, files: dict):
        self.set_config_field("recent_files", files)

    @property
    def theme_filename(self):
        """File name of the theme currently in use."""
        return self.get_config_field('theme_filename')

    @theme_filename.setter
    def theme_filename(self, filename):
        self.set_config_field('theme_filename', filename)

    @property
    def username(self):
        """Computer user name of the currently logged-in user."""
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def window_position(self):
        """Lasted saved window position to use with window restore function."""
        return (self.get_config_field('window_x'),
                self.get_config_field('window_y'))

    @window_position.setter
    def window_position(self, position: tuple | list):
        self.set_config_fields(['window_x', 'window_y'], position)

    @property
    def window_restore(self):
        """Indicator of app launch with last used window position and size."""
        return self.get_config_field('window_restore')

    @window_restore.setter
    def window_restore(self, restore: bool):
        self.set_config_field('window_restore', restore)

    @property
    def window_size(self):
        """Lasted saved window size to use with window restore function."""
        return (self.get_config_field('window_width'),
                self.get_config_field('window_height'))

    @window_size.setter
    def window_size(self, size: tuple | list):
        self.set_config_fields(['window_width', 'window_height'], size)
