#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Docstring placeholder
"""

import indigo  # noqa
from sensor_adapter import SensorAdapter
from pyrescaler.pyrescaler import *
import logging

__author__    = "dustysparkle, DaveL17"
__copyright__ = "Not used."
__license__   = "Apache 2.0"  # FIXME
__build__     = "Not used."
__title__     = 'Adapters Plugin for Indigo'
__version__   = '2022.0.5'


# ==============================================================================
def _is_number(val):
    """
    Docstring placeholder
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
        indigo.PluginBase.__init__(
            self, plugin_id, plugin_display_name, plugin_version, plugin_prefs
        )

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
    def debug_logging(self):

        # The Adapters Plugin logging is minimal due to the fact that the plugin is a shim on top
        # of other objects. For example, a sensor changes (which would typically be logged by
        # Indigo or another plugin) so an additional log message from this plugin would be overkill.
        log_format = '%(asctime)s.%(msecs)03d\t%(levelname)-10s\t%(name)s.%(funcName)-28s %(msg)s'
        self.plugin_file_handler.setFormatter(
            logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')
        )

        self.indigo_log_handler.setLevel(self.debug_level)

        self.sensor_logger = logging.getLogger("sensor_adapter")  # sensor_adapter.py logger
        self.sensor_logger.addHandler(self.indigo_log_handler)
        self.sensor_logger.setLevel(self.debug_level)

        self.pyrescaler_logger = logging.getLogger("pyrescaler")  # pyrescaler.py logger
        self.pyrescaler_logger.addHandler(self.indigo_log_handler)
        self.pyrescaler_logger.setLevel(self.debug_level)

    # ==============================================================================
    def __del__(self):
        """
        Docstring placeholder
        """
        indigo.PluginBase.__del__(self)

    # ==============================================================================
    def get_eligible_sensors(self, _filter="", values_dict=None, type_id="", target_id=0):
        """
        Docstring placeholder
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
    @staticmethod
    def get_device_config_ui_values(values_dict=None, user_cancelled=False, type_id="", dev_id=0):
        """
        Docstring placeholder
        """
        # Remove any test results so UI opens clean next time
        values_dict['formula_test'] = "Press the Show Result button to see the result."
        return values_dict

    # ==============================================================================
    # @staticmethod
    # def validate_device_config_ui(values_dict=None, user_cancelled=False, type_id="", dev_id=0):
    #     """
    #     Docstring placeholder
    #     """
    #     # Remove any test results so UI opens clean next time
    #     values_dict['formula_test'] = "Press the Show Result button to see the result."
    #     return True, values_dict

    # ==============================================================================
    def validate_prefs_config_ui(self, values_dict):
        """
        Docstring placeholder
        """
        self.debug_level = int(values_dict['showDebugLevel'])
        self.indigo_log_handler.setLevel(self.debug_level)
        self.sensor_logger.setLevel(self.debug_level)
        self.pyrescaler_logger.setLevel(self.debug_level)
        return True

    # ==============================================================================
    def startup(self):
        """
        Docstring placeholder
        """
        self.logger.debug("startup called")

    # ==============================================================================
    def shutdown(self):
        """
        Docstring placeholder
        """
        self.logger.debug("shutdown called")

    # ==============================================================================
    def open_browser_to_python_format_help(self, values_dict=None, type_id="", target_id=0):
        """
        Docstring placeholder
        """
        self.browserOpen("https://pyformat.info")

    # ==============================================================================
    def address_changed(self, values_dict=None, type_id="", target_id=0):
        """
        Docstring placeholder
        """
        self.logger.debug("address_changed")

    # ==============================================================================
    def show_formula_result(self, values_dict=None, type_id="", target_id=0):
        """
        Test adapter device conversion settings
        """
        import simpleeval
        addr        = values_dict['address']   # i.e., 12345678.temperature
        multiplier  = values_dict.get('multiplier', "")
        offset      = values_dict.get('offset', "")
        source      = addr.split('.')        # ['12345678', 'temperature']
        val_format  = values_dict['format']
        val_value   = indigo.devices[int(source[0])].states[source[1]]

        # Get the formula
        if type_id == "customConvertedSensor":
            val_formula = f"({val_value} * {multiplier}) + {offset}"
        else:
            val_formula = values_dict['formula']

        # Evaluate the formula expression
        try:
            result = simpleeval.simple_eval(val_formula, names={"x": val_value})
        except (SyntaxError, TypeError, ValueError) as err:
            result = f"Invalid Formula Expression: {err}"

        # Evaluate the format expression
        try:
            result = val_format.format(result)
        except (IndexError, TypeError, ValueError) as err:
            result = f"Invalid Format Expression: {err}"

        values_dict['formula_test'] = result
        return values_dict

    # ==============================================================================
    def scale_type_changed(self, values_dict=None, type_id="", target_id=0):
        """
        Docstring placeholder
        """
        self.logger.debug("scale_type_changed")

    # ==============================================================================
    def get_scales(self, _filter="", values_dict=None, type_id="", target_id=0):
        """
        Docstring placeholder
        """
        self.logger.debug("get_scales")
        if "scaleType" not in values_dict:
            return []
        self.logger.debug(f"getting scale options for scale type: {values_dict['scaleType']}")
        opts = get_scale_options(scale_type=values_dict["scaleType"])
        self.logger.debug(f"scale options: {opts}")
        return opts

    # ==============================================================================
    def device_start_comm(self, dev):
        """
        Docstring placeholder
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
    def device_stop_comm(self, dev):
        """
        Docstring placeholder
        """
        self.active_adapters = [
            adapter for adapter in self.active_adapters
            if adapter.address != dev.pluginProps["address"]
        ]

    # ==============================================================================
    def device_updated(self, orig_dev, new_dev):
        """
        Docstring placeholder
        """
        indigo.PluginBase.device_updated(self, orig_dev, new_dev)
        if new_dev.id in self.adapters_for_device:
            for adapter in self.adapters_for_device[new_dev.id]:
                adapter.go()

    # ==============================================================================
    # def run_concurrent_thread(self):
    #     """
    #     Docstring placeholder
    #     """
    #     try:
    #
    #         while True:
    #             self.sleep(5)
    #
    #     except self.StopThread:
    #         pass  # Optionally catch the StopThread exception and do any needed cleanup.
