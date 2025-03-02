# PyQt Application Template

A robust template for building PyQt6 desktop applications with a layered architecture. This repository provides a modular foundation for creating cross-platform GUI applications in Python, featuring a separation of UI components, application logic, and core utilities, all implemented programmatically without Qt Designer or `.ui` files.

## Features
- **Layered Architecture**:
  - `app/`: Application-specific logic, including dialogs and the main window.
  - `core/`: Utilities for control, configuration, and logging.
  - `ui/`: Custom, reusable widgets (e.g. toggle switch).
- **Core Functionality**:
  - Menu-driven interface with File (Open, Recent, Close, Quit), Edit (Preferences), and Help (About) options.
  - Supports opening files with recent file tracking.
  - Dynamic theming via QSS stylesheets.
  - User profile tracking for unique configuration settings for each user.
- **Python-Driven UI**: Full control through Python code.
- **Resource Support**: SVG icons and modular QSS stylesheets for customization.
- **Extensible**: Placeholder UI ready for additional widgets and logic.
- **Cross-Platform**: Runs on Windows, macOS, and Linux.

## Repository Structure
```text
PyQt-Application-Template/
├── app/                    # Application-specific logic
│   ├── dialogs/           # Dialog implementations
│   │   ├── init.py    # Package initializer
│   │   ├── about_dialog.py  # About dialog logic
│   │   └── config_dialog.py # Configuration dialog logic
│   ├── init.py        # Package initializer
│   ├── main_window.py     # Main application window with menu and UI
│   └── metadata.py        # Application metadata
├── core/                  # Core utilities
│   ├── init.py        # Package initializer
│   ├── app_config_handler.py # Configuration management
│   ├── logger.py          # Logging utility
│   ├── main_controller.py # Main application controller
├── resources/             # Static assets
│   ├── icons/             # SVG icons for UI
│   │   ├── application_icon.svg # App icon
│   │   ├── down-arrow-template.svg
│   │   ├── minus-symbol-template.svg
│   │   ├── pause-circle.svg
│   │   ├── play-circle.svg
│   │   ├── plus-symbol-template.svg
│   │   └── warning-triangle.svg
│   ├── styles/            # QSS stylesheets for theming
│   │   ├── colors_dark.qss       # Dark theme colors
│   │   ├── colors_dark_orange.qss # Dark orange theme colors
│   │   ├── colors_light.qss      # Light theme colors
│   │   └── style_template.qss    # Base stylesheet template
│   ├── init.py        # Package initializer
│   └── app_config.yaml    # Configuration file
├── tests/                 # Test suite
│   ├── init.py        # Package initializer
│   └── test_metadata.py   # Metadata tests
├── ui/                    # Custom UI widgets
│   ├── init.py        # Package initializer
│   └── toggle_switch.py   # Custom toggle switch widget
├── .gitignore             # Ignores Python artifacts (e.g., pycache)
├── LICENSE                # MIT License
├── main.py                # Application entry point
├── pyproject.toml         # Project configuration
├── README.md              # This documentation
├── requirements.txt       # Project dependencies
```
## Installation
1. **Create a New Repository from this Template**:
   Use the "Use this template" button on GitHub to start a new project with this structure. This is the recommended way to begin building your application.

2. **Clone or Fork (Optional)**:
   To test or contribute to the template:
   <CODEBLOCK>
   git clone https://github.com/DevMolasses/PyQt-Application-Template.git
   cd PyQt-Application-Template
   </CODEBLOCK>
   Or fork the repository via GitHub for development purposes.

3. **Set Up a Virtual Environment** (recommended):
   <CODEBLOCK>
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   </CODEBLOCK>

4. **Install Dependencies**:
   <CODEBLOCK>
   pip install -r requirements.txt
   </CODEBLOCK>
   Contents of `requirements.txt`:
   <CODEBLOCK>
   pyqt6
   pyyaml
   icecream
   pytest
   </CODEBLOCK>
   Note: `icecream` and `pytest` are optional based on your workflow; core functionality requires only `pyqt6` and `pyyaml`.

5. **Run the Application**:
   <CODEBLOCK>
   python main.py
   </CODEBLOCK>
   Launches a window with a menu bar, placeholder label, and button.

## Usage
- **Extend the UI**: Add widgets to `app/main_window.py`’s `layout` in `_setup_ui()`.
- **Enhance Logic**: Implement file handling in `core/main_controller.py` for `_open_file()` and `_close_file()`.
- **Add Dialogs**: Expand `app/dialogs/` with additional functionality.
- **Testing**: Write tests in `tests/` beyond `test_metadata.py`.

### Customizing Stylesheets
This template uses a non-standard QSS approach for theming. Styles are split into:
- **Color Files**: `colors_dark.qss`, `colors_dark_orange.qss`, `colors_light.qss` to define color variables (e.g., `widget-background`, `widget-alternate-background`).
- **Template File**: `style_template.qss` provides the base widget styles, referencing color variables.
To customize:
1. Modify or add color variables in a `colors_*.qss` file.
2. Update `style_template.qss` to apply styles to widgets, using variables from the color file.
    ```
    QPushButton{
        background-color: @widget-alternate-background;
        color: @text;
        border: 1px solid @major-accent;
        border-radius: 4px;
        padding: 6px 12px;
    }
    ```
3. Load your chosen stylesheet via `core/main_controller.py`’s `get_stylesheet()` method.

## Contributing
Contributions welcome! Fork, branch, commit, push, and submit a pull request.

## License
[MIT License](LICENSE).

## Acknowledgments
- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/).
- Created by [DevMolasses](https://github.com/DevMolasses).

<!-- ## Branch Options
This is the `main` branch for a multi-layered app. For a simpler version, check out the `simple` branch (`git checkout simple`). -->