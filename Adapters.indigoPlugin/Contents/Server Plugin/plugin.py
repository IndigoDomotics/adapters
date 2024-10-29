#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
This plugin for the Indigo home automation sever allows you to add thin "adapters" on top of your devices to perform
all kinds of mathematical or formatting transformations.

For example, suppose you have devices that report temperatures in Fahrenheit and you prefer Celsius, or the other way
around. This plugin can generate "device adapters" that "wrap" around your native device and convert the temperature to
the scale you prefer.

It supports all kinds of things:
- temperature, distance, and power conversions
- arbitrary linear translations of numeric sensors (i.e. multiplier and an offset factor)
- custom expressions and formats to transmogrify (single) sensor outputs in almost any way you can think of

Originally authored by forum user `dustysparkle`.
Contributions by: DaveL17
"""

import logging  # NOTE: logging must be imported after pyrescaler
import simpleeval
from sensor_adapter import SensorAdapter
from pyrescaler.pyrescaler import get_scale_options

try:
    import indigo  # noqa
    # import pydevd  # noqa
except ImportError:
    pass

__author__    = "dustysparkle, DaveL17"
__copyright__ = "Not used."
__license__   = "Apache 2.0"
__build__     = "Not used."
__title__     = 'Adapters Plugin for Indigo'
__version__   = '2024.1.0'


# ==============================================================================
def _is_number(val) -> bool:
    """
    Convenience method to determine whether passed value is a number. This method will also return True if the passed
    value is a string, as long as it will float.

    :param val: The value to check
    """
    try:
        float(val)
        return True
    except ValueError:
        return False


# ==============================================================================
class Plugin(indigo.PluginBase):
    """
    Docstring placeholder
    """

    # ==============================================================================
    def __init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs):
        """
        Docstring placeholder
        """
        # indigo.PluginBase.__init__(
        #     self, plugin_id, plugin_display_name, plugin_version, plugin_prefs
        # )
        super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs)

        self.active_adapters     = []
        self.adapters_for_device = {}
        self.debug_level         = int(self.pluginPrefs.get('showDebugLevel', "30"))
        self.sensor_logger       = None
        self.pyrescaler_logger   = None

        # =============================== Debug Logging ================================
        self.debug_logging()

        # "Subscribe to Changes" from all indigo devices, so we can update our 'converted' values
        # any time the native value changes.
        indigo.devices.subscribeToChanges()

    # ==============================================================================
    def address_changed(self, values_dict: indigo.Dict = None, type_id: str = "", target_id: int = 0) -> None:
        """
        Docstring placeholder

        :param indigo.Dict values_dict:
        :param str type_id:
        :param int target_id:
        """
        self.logger.debug("address_changed")

    # ==============================================================================
    def device_updated(self, orig_dev: indigo.Dict, new_dev: indigo.Dict) -> None:
        """
        Docstring placeholder

        :param indigo.Device orig_dev:
        :param indigo.Device new_dev:
        """
        indigo.PluginBase.device_updated(self, orig_dev, new_dev)
        if new_dev.id in self.adapters_for_device:
            for adapter in self.adapters_for_device[new_dev.id]:
                adapter.go()

    # ==============================================================================
    def debug_logging(self) -> None:
        """
        The Adapters Plugin logging is minimal due to the fact that the plugin is a shim on top of other objects. For
        example, a sensor changes (which would typically be logged by Indigo or another plugin) so an additional log
        message from this plugin would be overkill.
        """
        log_format = '%(asctime)s.%(msecs)03d\t%(levelname)-10s\t%(name)s.%(funcName)-28s %(msg)s'
        self.plugin_file_handler.setFormatter(logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S'))

        self.indigo_log_handler.setLevel(self.debug_level)

        self.sensor_logger = logging.getLogger("sensor_adapter")  # sensor_adapter.py logger
        self.sensor_logger.addHandler(self.indigo_log_handler)
        self.sensor_logger.setLevel(self.debug_level)

        self.pyrescaler_logger = logging.getLogger("pyrescaler")  # pyrescaler.py logger
        self.pyrescaler_logger.addHandler(self.indigo_log_handler)
        self.pyrescaler_logger.setLevel(self.debug_level)

    # ==============================================================================
    def device_start_comm(self, dev: indigo.Device) -> None:
        """
        Docstring placeholder

        :param indigo.Device dev:
        """
        self.logger.debug(f"device_start_comm: {dev.pluginProps['address']}")

        # in case any states added/removed after plugin upgrade
        dev.stateListOrDisplayStateIdChanged()

        new_device = SensorAdapter(dev)
        self.active_adapters.append(new_device)

        if new_device.native_device_id not in self.adapters_for_device:
            self.adapters_for_device[new_device.native_device_id] = []

        self.adapters_for_device[new_device.native_device_id].append(new_device)

        self.logger.debug(f"added adapter: {new_device.name()}")

    # ==============================================================================
    def device_stop_comm(self, dev: indigo.Device) -> None:
        """
        Docstring placeholder

        :param indigo.Device dev:
        """
        self.active_adapters = [
            adapter for adapter in self.active_adapters
            if adapter.address != dev.pluginProps["address"]
        ]

    # ==============================================================================
    @staticmethod
    def get_device_config_ui_values(
            values_dict: indigo.Dict = None, user_cancelled: bool = False, type_id: str = "", dev_id: int = 0
    ) -> indigo.Dict:
        """
        Docstring placeholder

        :param indigo.Dict values_dict:
        :param bool user_cancelled:
        :param str type_id:
        :param int dev_id:
        """
        # Remove any prior test results so UI opens clean next time
        values_dict['formula_test'] = "Press the Show Result button to see the result."
        return values_dict

    # ==============================================================================
    def get_eligible_sensors(
            self, _filter: str = "", values_dict: indigo.Dict = None, type_id: str = "", target_id: int = 0
    ) -> list:
        """
        Return a list of device/states with numeric values

        :param str _filter:
        :param indigo.Dict values_dict:
        :param str type_id:
        :param int target_id:
        """
        eligible_sensors = []
        for dev in indigo.devices:
            # don't include instances of this plugin/device in the list
            if (not dev.pluginId) or (dev.pluginId != self.pluginId):
                for (state_key, state_value) in dev.states.items():
                    # only return devices/states that have a numeric value
                    if _is_number(state_value):
                        eligible_sensors.append(
                            (f"{dev.id:d}.{state_key}",
                             f"{dev.name} ({state_key}): {f'{float(state_value):.1f}'}"
                             )
                        )

        return eligible_sensors

    # ==============================================================================
    def get_scales(self, _filter: str = "", values_dict: indigo.Dict = None, type_id: str = "", target_id: int = 0) -> list:
        """
        Docstring placeholder

        :param str _filter:
        :param indigo.Dict values_dict:
        :param str type_id:
        :param int target_id:
        """
        self.logger.debug("get_scales")
        if "scaleType" not in values_dict:
            return []
        self.logger.debug(f"getting scale options for scale type: {values_dict['scaleType']}")
        opts = get_scale_options(scale_type=values_dict["scaleType"])
        self.logger.debug(f"scale options: {opts}")
        return opts

    # ==============================================================================
    def open_browser_to_python_format_help(self, values_dict: indigo.Dict = None, type_id: str = "", target_id: int = 0) -> None:
        """
        Docstring placeholder

        :param indigo.Dict values_dict:
        :param str type_id:
        :param int target_id:
        """
        self.browserOpen("https://pyformat.info")

    # ==============================================================================
    def scale_type_changed(self, values_dict=None, type_id="", target_id=0) -> None:
        """
        Called by Devices.xml when a Predefined Scale Adapter scale type is changed.
        """
        self.logger.debug("scale_type_changed")

    # ==============================================================================
    def show_formula_result(self, values_dict: indigo.Dict = None, type_id: str = "", target_id: int = 0):
        """
        Test adapter device conversion settings

        :param indigo.Dict values_dict:
        :param str type_id:
        :param int target_id:
        """
        address        = values_dict['address']
        error_msg_dict = indigo.Dict()
        formatter      = values_dict['format']
        multiplier     = values_dict.get('multiplier', "")
        offset         = values_dict.get('offset', "")

        # Source value
        try:
            source    = address.split('.')  # ['12345678', 'temperature']
            val_value = indigo.devices[int(source[0])].states[source[1]]
        except ValueError:
            # Source device has not yet been selected
            return values_dict

        # Get the formula expression
        if type_id == "customConvertedSensor":
            val_formula = f"({val_value} * {multiplier}) + {offset}"
        else:
            val_formula = values_dict['formula']

        # Evaluate the formula expression
        try:
            result = simpleeval.simple_eval(val_formula, names={"x": val_value})
        except Exception as err:
            error_msg_dict['formula'] = f"Invalid Formula Expression: {err}"
            self.logger.debug(f"Invalid Formula: {val_formula}")
            return values_dict, error_msg_dict

        # Evaluate the format expression
        try:
            result = formatter.format(result)
            if len(result) == 0:
                raise Exception
        except Exception as err:
            error_msg_dict['format'] = f"Invalid Format Expression: {err}"
            self.logger.debug(f"Invalid Format Specifier: {formatter}")
            return values_dict, error_msg_dict

        values_dict['formula_test'] = result
        return values_dict

    # ==============================================================================
    def validate_prefs_config_ui(self, values_dict: indigo.Dict) -> tuple:
        """
        Docstring placeholder

        :param indigo.Dict values_dict:
        """
        error_msg_dict = indigo.Dict()
        try:
            self.debug_level = int(values_dict['showDebugLevel'])
            self.indigo_log_handler.setLevel(self.debug_level)
            self.sensor_logger.setLevel(self.debug_level)
            self.pyrescaler_logger.setLevel(self.debug_level)
            return True, values_dict
        except TypeError as error:
            error_msg_dict['showDebugLevel'] = "The debug level is invalid"
            return False, values_dict, error_msg_dict

    # ==============================================================================
    def my_tests(self, action=None):
        from Tests import test_plugin
        plugin_tests = test_plugin.TestPlugin()
        simple_eval_tests = test_plugin.TestSimpleEval()
        # sensor_adapter_tests = test_plugin.TestSensorAdapter()

        def process_test_result(result, name):
            if result[0] is True:
                self.logger.warning(f"{name} tests passed.")
            else:
                self.logger.warning(f"{result[1]}")

        test = plugin_tests.test_plugin(self)
        process_test_result(test, "Plugin")
        test = simple_eval_tests.test_simple_eval(self)
        process_test_result(test, "Simple Eval")
        # test = sensor_adapter_tests.test_sensor_adapter(self)  # There are no sensor adapter tests at this time.
        # process_test_result(test, "Sensor Adapter")
        self.logger.warning("There are no Sensor Adapter tests yet.")
        self.logger.warning("There are no pyrescaler tests yet.")
