"""
Unit tests that require access to the IOM go here.

To run these tests, you will need a copy of the plugin installed and running on the active server. Create an action item
that calls the hidden `my_tests` action using an embedded script like the following:

    plugin_id = "com.drjason.temp-adapter"
    plugin = indigo.server.getPlugin(plugin_id)

    try:
        if indigo.PluginInfo.isRunning(plugin):
            plugin.executeAction("my_tests")
        else:
            indigo.server.log("Plugin not enabled.")
    except Exception as err:
        indigo.server.log(f"{err}")

Tests should be added to this file when appropriate.
"""
from unittest import TestCase
# from unittest.mock import MagicMock
import dotenv
import logging
import indigo  # noqa
import os


import simpleeval  # noqa
# import sensor_adapter  # noqa
import pyrescaler  # noqa

LOGGER = logging.getLogger('Plugin')
dotenv.load_dotenv()

DEVICE_CUSTOM_FORMULA_GENERIC = indigo.devices[int(os.getenv('DEVICE_CUSTOM_FORMULA_GENERIC'))]
DEV_TEMP_CONV = indigo.devices[int(os.getenv('DEVICE_TEMPERATURE_CONVERSION'))]


class TestPlugin(TestCase):
    """ """
    def __init__(self):
        super().__init__()

    @staticmethod
    def test_plugin(plugin):
        """ """
        try:
            test_case = TestCase()

            # ===================================== validate_prefs_config_ui() =====================================
            values_dict = {'showDebugLevel': '20'}  # value as string
            test_case.assertTrue(plugin.validate_prefs_config_ui(values_dict), "Method should return True.")
            values_dict['showDebugLevel'] = 20  # value as int
            test_case.assertTrue(plugin.validate_prefs_config_ui(values_dict), "Method should return True.")

            # ===================================== show_formula_result() =====================================
            value = DEV_TEMP_CONV.states['temperature']  # value as real
            values_dict = {'address': f"{DEV_TEMP_CONV.id}.temperature", 'format': "{0:.2f} ºF", 'multiplier': "", 'offset': "", 'formula': "x / 2"}
            result = plugin.show_formula_result(values_dict, "", 0)
            test_case.assertIsInstance(result, dict, "Method should return a dict object.")
            test_case.assertIsInstance(result['formula_test'], str, "Method should return a string object.")
            test_case.assertEqual(result['formula_test'], f'{value / 2:0.2f} ºF', "Method didn't return a properly formatted value.")

            # ===================================== get_scales() =====================================
            values_dict = {}
            scale_list = {'power': [('W', 'Watts'), ('kW', 'Kilowatts'), ('hp', 'Horsepower')],
                          'temperature': [('F', 'Fahrenheit'), ('C', 'Celsius')],
                          'length': [('in', 'Inches'), ('ft', 'Feet'), ('yd', 'Yards'), ('mi', 'Miles'), ('cm', 'Centimeters'), ('m', 'Meters'), ('km', 'Kilometers'), ('nmi', 'Nautical Miles'), ('fm', 'Fathoms'), ('cbt', 'Cubits'), ('h', 'Hands')],
                          '': [],
                          }
            result = plugin.get_scales("", values_dict, "", 0)
            test_case.assertIsInstance(result, list, "Method should return a list object.")
            for scale_type in ['power', 'temperature', 'length', '']:
                values_dict = {'scaleType': scale_type}
                result = plugin.get_scales("", values_dict, "", 0)
                test_case.assertIsInstance(result, list, "Method should return a list object.")
                test_case.assertEqual(result, scale_list[scale_type], "Method didn't return a valid list.")

            # ===================================== get_eligible_sensors() =====================================
            # We can't test if get_eligible_sensors() returns an accurate list because the result can vary.
            result = plugin.get_eligible_sensors("", None, "", 0)
            test_case.assertIsInstance(result, list, "Method should return a list object.")
            test_case.assertTrue(all(isinstance(item, tuple) for item in result), "List should contain only tuples.")

            return True, None
        except Exception as error:
            LOGGER.critical(f"{error}")
            return False, error


# ===================================== simpleeval.py =====================================
class TestSimpleEval(TestCase):
    def __init__(self):
        super().__init__()

    @staticmethod
    def test_simple_eval(plugin):
        test_case = TestCase()
        # ===================================== random_int() =====================================
        test_case.assertTrue(simpleeval.random_int(10) <= 10, "Method return should be less than input")
        test_case.assertTrue(simpleeval.random_int(100) <= 100, "Method return should be less than input")

        # ===================================== safe_power() =====================================
        test_case.assertEqual(simpleeval.safe_power(2, 4), 16, "Method didn't return the expected value.")

        # ===================================== safe_multi() =====================================
        test_case.assertEqual(simpleeval.safe_mult(10, "*"), "**********", "Method didn't return the expected value.")
        test_case.assertEqual(simpleeval.safe_mult(10, 2), 20, "Method didn't return the expected value.")

        # ===================================== safe_add() =====================================
        test_case.assertEqual(simpleeval.safe_add("**", "**"), "****", "Method didn't return the expected value.")
        test_case.assertEqual(simpleeval.safe_add(1, 1), 2, "Method didn't return the expected value.")

        # ===================================== simple_eval() =====================================
        test_case.assertEqual(simpleeval.simple_eval('x', None, None, {'x': 50}), 50, "Method didn't return the expected value.")
        test_case.assertEqual(simpleeval.simple_eval('x + 2', None, None, {'x': 50}), 52, "Method didn't return the expected value.")
        test_case.assertEqual(simpleeval.simple_eval('x - 2', None, None, {'x': 50}), 48, "Method didn't return the expected value.")
        test_case.assertEqual(simpleeval.simple_eval('x * 2', None, None, {'x': 50}), 100, "Method didn't return the expected value.")
        test_case.assertEqual(simpleeval.simple_eval('x / 2', None, None, {'x': 50}), 25, "Method didn't return the expected value.")
        test_case.assertEqual(simpleeval.simple_eval('x + 20 - (10 * 7)', None, None, {'x': 50}), 0, "Method didn't return the expected value.")
        test_case.assertEqual(simpleeval.simple_eval('x ** 2', None, None, {'x': 5}), 25, "Method didn't return the expected value.")
        test_case.assertEqual(simpleeval.simple_eval('1 if x == 2 else -1 if x == 3 else 0', None, None, {'x': 2}), 1, "Method didn't return the expected value.")
        test_case.assertEqual(simpleeval.simple_eval('1 if x == 2 else -1 if x == 3 else 0', None, None, {'x': 3}), -1, "Method didn't return the expected value.")
        test_case.assertEqual(simpleeval.simple_eval('1 if x == 2 else -1 if x == 3 else 0', None, None, {'x': 4}), 0, "Method didn't return the expected value.")
        return True, None


# ===================================== sensor_adapter.py =====================================
# There are no sensor_adapter tests at this time. They should be added as need cases arise.
