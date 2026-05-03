### v2025.2.1
- Fixes `device_stop_comm` not cleaning up `adapters_for_device`, causing stopped adapters to continue receiving updates.
- Fixes `validate_prefs_config_ui` only catching `TypeError` when `ValueError` is also possible for invalid debug level input.
- Fixes incorrect `indigo.Dict` type annotations on `device_updated` parameters (should be `indigo.Device`).
- Fixes `show_formula_result` building an invalid formula string when multiplier or offset is empty.
- Fixes bare `raise Exception` in format validation producing an empty error message.
- Fixes duplicate `indigo.Device` append in `device_start_comm`.
- Fixes `_is_number` not catching `TypeError` for `None` and non-numeric state values.

### v2025.2.0
- Removes Actions.xml and MenuItems.xml server plugin files.
- Updates simpleeval for Python 3 compatibility.
- Code cleanup and bug fixes.
- Standardized project `.gitignore` file.
- Removes unused variables from `tests/.env` file.

### v2025.1.0
- Stability and performance enhancements.
- Code cleanup.

### v2024.1.0
- Removes unneeded PyCharm debugging code.
- Cleans up .gitignore file.
- More code typing.
- Unit tests.

### v2023.2.0
- Code refinements.
- Basic wiki pages.
- Fixes `plugin does not define method scale_type_changed` error.

### v2023.1.0
- Code refinements.

### v2022.1.8
- Adds trap to `sensor_adaptor.go()` method to avoid infrequent tracebacks when devices not available at startup.
- Released to the Plugin Store

### v2022.0.7
- Improves formula test tool UI error reporting (error_msg_dict).

### v2022.0.6
- Adds trap for formula test tool when device first created.
- Code refinements.

### v2022.0.5
- Adds a tool to test expressions before saving them to the Adapters device.

### v2022.0.4
- Removes Rankine and Kelvin from temperature conversions (can be reactivated if needed.)

### v2022.0.3
- Adds icons to devices lacking them; improves state value alignment in the Indigo UI.

### v2022.0.2
- Refactors logging.

### v2022.0.1
- Initial port to Indigo 2022.1 and Python 3.
