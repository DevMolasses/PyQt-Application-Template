r"""src\config_handler.py."""
__license__ = """
Enter license here.
"""
__author__ = "Author Name"
__version__ = 0.0

import os
import getpass
import yaml
import copy


class ConfigHandler:
    """Handle all configuration file needs."""

    # Declare parameters
    _username = None

    STARTER_CONFIG = {"theme_filename": "colors_light.qss",
                      "window_restore": False,
                      "window_x": 100,
                      "window_y": 100,
                      "window_width": 1600,
                      "window_height": 1200,
                      "recent_files": {},
                      "num_recents_to_show": 10}

    def __init__(self, test=False):
        try:
            self._username = getpass.getuser()
        except Exception:
            self._username = "DEFAULT"

        if test:
            self.config_filepath = ".\\testing\\test_config.yaml"
        else:
            self.config_filepath = ".\\resources\\app_config.yaml"
        try:
            with open(self.config_filepath, 'r') as file:
                self.config = yaml.safe_load(file)
        except FileNotFoundError:
            self.config = {"DEFAULT": copy.deepcopy(self.STARTER_CONFIG)}
            self.save_config()

        if self.username not in self.config:
            self.config[self.username] = self.STARTER_CONFIG
            self.save_config()

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
            idx = list(self.get_config_field("recent_files").values()).index(filepath)

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
            try:
                value = self.STARTER_CONFIG[field]
                self.set_config_field(field, value)
                return value
            except KeyError:
                raise

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
