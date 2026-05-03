"""
Tests for plugin.py, simpleeval.py, pyrescaler, and sensor_adapter.py.

Tests that require the Indigo IOM (e.g. TestPlugin) run scripts via the
indigo-host subprocess. All other tests run in-process and have no Indigo
dependency.

Note: the plugin does not have any Actions or Triggers at this time.
"""
import dotenv
import logging
import os
from tests.shared import APIBase # noqa
import simpleeval  # noqa
from tests.shared.utils import run_host_script
import textwrap
from unittest.mock import MagicMock, patch
from pyrescaler.pyrescaler import (get_converter, get_scale_options,
                                   AffineScaledMeasurement,
                                   ArbitraryFormulaScaledMeasurement)

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))


# ===================================== plugin.py =====================================
class TestPlugin(APIBase):
    """Integration tests for plugin.py that run against a live Indigo host via indigo-host scripts."""

    @classmethod
    def setUpClass(cls):
        pass

    # Create a test device of type Predefined Scale Adapter (`tempConvertedSensor`)
    def test_device_creation(self):
        """Verify that a tempConvertedSensor device can be created and deleted via the Indigo API.

        Note that `SupportsSensorValue` is required for programmatic device creation in order to create the
        `sensorValue` state.
        """
        plugin_id = os.getenv("PLUGIN_ID")
        my_name = "'adapters_unit_test_create_device'"
        my_props = {'SupportsSensorValue': True,
                    'address': os.getenv('DEVICE_CREATE_ID'),
                    'scaleType': 'length',
                    'nativeScale': 'mi',
                    'desiredScale': 'km',
                    'precision': 1}
        host_script = textwrap.dedent(f"""\
            try:
                import time
                indigo.device.create(protocol=indigo.kProtocol.Plugin,
                    address='8',
                    name={my_name},
                    description='Description Here',
                    pluginId={plugin_id},
                    deviceTypeId='tempConvertedSensor',
                    props={my_props},
                    folder=1476713640
                )
                time.sleep(1)
                return True
            except:
                return False
        """)
        run_host_script(host_script)
        self.assertTrue(host_script, "Device creation successful.")

        # Confirm the device was created
        host_script = textwrap.dedent(f"""\
            if {my_name} in [dev.name for dev in indigo.devices.iter({plugin_id})]:
                return True
            else:
                return False
        """)
        self.assertTrue(host_script, "Could not confirm the device was created.")

        # Delete the test device
        host_script = textwrap.dedent(f"""\
            try:
                indigo.device.delete({my_name})
                return True
            except:
                return False
        """)
        run_host_script(host_script)
        self.assertTrue(host_script, "Device deletion failed.")

# ===================================== simpleeval.py =====================================
class TestSimpleEval(APIBase):
    """Tests for the plugin's use of simpleeval helper functions (no Indigo dependency)."""

    @classmethod
    def setUpClass(cls):
        pass

    def test_simple_eval(self):
        """ Test simple evaluation """
        # ===================================== random_int() =====================================
        self.assertTrue(simpleeval.random_int(10) <= 10, "Method return should be less than input")
        self.assertTrue(simpleeval.random_int(100) <= 100, "Method return should be less than input")

        # ===================================== safe_power() =====================================
        self.assertEqual(simpleeval.safe_power(2, 4), 16, "Method didn't return the expected value.")

        # ===================================== safe_multi() =====================================
        self.assertEqual(simpleeval.safe_mult(10, "*"), "**********", "Method didn't return the expected value.")
        self.assertEqual(simpleeval.safe_mult(10, 2), 20, "Method didn't return the expected value.")

        # ===================================== safe_add() =====================================
        self.assertEqual(simpleeval.safe_add("**", "**"), "****", "Method didn't return the expected value.")
        self.assertEqual(simpleeval.safe_add(1, 1), 2, "Method didn't return the expected value.")

        # ===================================== simple_eval() =====================================
        self.assertEqual(simpleeval.simple_eval('x', None, None, {'x': 50}), 50, "Method didn't return the expected value.")
        self.assertEqual(simpleeval.simple_eval('x + 2', None, None, {'x': 50}), 52, "Method didn't return the expected value.")
        self.assertEqual(simpleeval.simple_eval('x - 2', None, None, {'x': 50}), 48, "Method didn't return the expected value.")
        self.assertEqual(simpleeval.simple_eval('x * 2', None, None, {'x': 50}), 100, "Method didn't return the expected value.")
        self.assertEqual(simpleeval.simple_eval('x / 2', None, None, {'x': 50}), 25, "Method didn't return the expected value.")
        self.assertEqual(simpleeval.simple_eval('x + 20 - (10 * 7)', None, None, {'x': 50}), 0, "Method didn't return the expected value.")
        self.assertEqual(simpleeval.simple_eval('x ** 2', None, None, {'x': 5}), 25, "Method didn't return the expected value.")
        self.assertEqual(simpleeval.simple_eval('1 if x == 2 else -1 if x == 3 else 0', None, None, {'x': 2}), 1, "Method didn't return the expected value.")
        self.assertEqual(simpleeval.simple_eval('1 if x == 2 else -1 if x == 3 else 0', None, None, {'x': 3}), -1, "Method didn't return the expected value.")
        self.assertEqual(simpleeval.simple_eval('1 if x == 2 else -1 if x == 3 else 0', None, None, {'x': 4}), 0, "Method didn't return the expected value.")


class TestPyRescaler(APIBase):
    """Tests for the plugin's use of pyrescaler — get_scale_options(), get_converter(),
    AffineScaledMeasurement, and ArbitraryFormulaScaledMeasurement (no Indigo dependency)."""

    @classmethod
    def setUpClass(cls):
        pass

    # ===================================== get_scale_options() =====================================
    def test_get_scale_options(self):
        """Test get_scale_options() returns valid dropdown data for each scale type used by the plugin."""
        # temperature
        options = get_scale_options(scale_type='temperature')
        self.assertIsInstance(options, list, "get_scale_options should return a list.")
        self.assertTrue(len(options) > 0, "Temperature options list should not be empty.")
        self.assertTrue(all(len(t) == 2 for t in options), "Each option should be a 2-tuple.")
        keys = [t[0] for t in options]
        self.assertIn('F', keys, "Temperature options should include Fahrenheit key 'F'.")
        self.assertIn('C', keys, "Temperature options should include Celsius key 'C'.")

        # length
        options = get_scale_options(scale_type='length')
        self.assertTrue(len(options) > 0, "Length options list should not be empty.")
        keys = [t[0] for t in options]
        self.assertIn('mi', keys, "Length options should include miles key 'mi'.")
        self.assertIn('km', keys, "Length options should include kilometers key 'km'.")

        # power
        options = get_scale_options(scale_type='power')
        self.assertTrue(len(options) > 0, "Power options list should not be empty.")
        keys = [t[0] for t in options]
        self.assertIn('W',  keys, "Power options should include watts key 'W'.")
        self.assertIn('kW', keys, "Power options should include kilowatts key 'kW'.")

    # ===================================== get_converter() — temperature =====================================
    def test_get_converter_temperature(self):
        """Test get_converter() for temperature, matching _PredefinedDelegate usage."""
        # F -> C
        converter = get_converter('temperature', 'F', 'C', precision=1)
        self.assertAlmostEqual(converter.convert(32),  0.0,   1, "32°F should convert to 0°C.")
        self.assertAlmostEqual(converter.convert(212), 100.0, 1, "212°F should convert to 100°C.")

        # C -> F
        converter = get_converter('temperature', 'C', 'F', precision=1)
        self.assertAlmostEqual(converter.convert(0),   32.0,  1, "0°C should convert to 32°F.")
        self.assertAlmostEqual(converter.convert(100), 212.0, 1, "100°C should convert to 212°F.")

        # suffix() / suffix_native() — used in _PredefinedDelegate.name()
        converter = get_converter('temperature', 'F', 'C', precision=1)
        self.assertIn('C', converter.suffix(),        "Desired scale suffix should contain 'C'.")
        self.assertIn('F', converter.suffix_native(), "Native scale suffix should contain 'F'.")

        # format() — used in SensorAdapter.go()
        result = converter.format(32)
        self.assertIsInstance(result, str, "format() should return a string.")
        self.assertIn('0', result, "Formatted 32°F->°C should contain '0'.")

    # ===================================== get_converter() — length =====================================
    def test_get_converter_length(self):
        """Test get_converter() for length, matching _PredefinedDelegate usage."""
        converter = get_converter('length', 'mi', 'km', precision=3)
        self.assertAlmostEqual(converter.convert(1), 1.609, 2, "1 mile should convert to ~1.609 km.")

        converter = get_converter('length', 'ft', 'm', precision=2)
        self.assertAlmostEqual(converter.convert(1), 0.3048, 3, "1 ft should convert to 0.3048 m.")

    # ===================================== get_converter() — power =====================================
    def test_get_converter_power(self):
        """Test get_converter() for power, matching _PredefinedDelegate usage."""
        converter = get_converter('power', 'W', 'kW', precision=3)
        self.assertAlmostEqual(converter.convert(1000), 1.0, 3, "1000 W should convert to 1 kW.")

        converter = get_converter('power', 'kW', 'W', precision=0)
        self.assertAlmostEqual(converter.convert(1), 1000.0, 0, "1 kW should convert to 1000 W.")

    # ===================================== AffineScaledMeasurement =====================================
    def test_affine_scaled_measurement(self):
        """Test AffineScaledMeasurement with the constructor args _AffineTransformDelegate passes."""
        # identity
        m = AffineScaledMeasurement(multiplier=1.0, offset=0.0, format_string="{0:.1f}")
        self.assertAlmostEqual(m.convert(42), 42.0, 5, "Identity transform should return input unchanged.")

        # scale only
        m = AffineScaledMeasurement(multiplier=2.0, offset=0.0, format_string="{0:.1f}")
        self.assertAlmostEqual(m.convert(5), 10.0, 5, "multiplier=2 should double the input.")

        # offset only
        m = AffineScaledMeasurement(multiplier=1.0, offset=10.0, format_string="{0:.1f}")
        self.assertAlmostEqual(m.convert(5), 15.0, 5, "offset=10 should add 10 to the input.")

        # string props from pluginProps (plugin passes raw strings from device config)
        m = AffineScaledMeasurement(multiplier='1.8', offset='32', format_string="{0:.1f} °F")
        self.assertAlmostEqual(m.convert(0), 32.0, 5, "String multiplier/offset should be coerced to float.")

        # format() applies the format_string from pluginProps
        m = AffineScaledMeasurement(multiplier=2.0, offset=0.0, format_string="{0:.2f} units")
        self.assertEqual(m.format(5), "10.00 units", "format() should apply the configured format_string.")

    # ===================================== ArbitraryFormulaScaledMeasurement =====================================
    def test_arbitrary_formula_scaled_measurement(self):
        """Test ArbitraryFormulaScaledMeasurement with formulas matching Devices.xml examples."""
        # default formula shown in Devices.xml
        m = ArbitraryFormulaScaledMeasurement(formula="(9/5 * x) + 32", format_string="{0:.1f}")
        self.assertAlmostEqual(m.convert(0),   32.0,  5, "C->F formula: 0°C should yield 32°F.")
        self.assertAlmostEqual(m.convert(100), 212.0, 5, "C->F formula: 100°C should yield 212°F.")

        # polynomial example from Devices.xml
        m = ArbitraryFormulaScaledMeasurement(formula="x ** 2 + 3 * x + 4", format_string="{0:.1f}")
        self.assertAlmostEqual(m.convert(2), 14.0, 5, "Polynomial formula: f(2) should equal 14.")

        # conditional example from Devices.xml
        m = ArbitraryFormulaScaledMeasurement(formula="1 if x == 2 else -1", format_string="{0:.1f}")
        self.assertEqual(m.convert(2),  1.0,  "Conditional formula should return 1 when x == 2.")
        self.assertEqual(m.convert(99), -1.0, "Conditional formula should return -1 when x != 2.")

        # format() applies the format_string from pluginProps
        m = ArbitraryFormulaScaledMeasurement(formula="x * 2", format_string="{0:.2f} result")
        self.assertEqual(m.format(5), "10.00 result", "format() should apply the configured format_string.")


class TestSensorAdapter(APIBase):
    """Tests for sensor_adapter.py delegate classes and SensorAdapter.go().

    The indigo module is injected into sys.modules as a MagicMock in setUpClass
    so that sensor_adapter can be imported without the Indigo runtime.
    """

    @classmethod
    def setUpClass(cls):
        import sys
        sys.modules['indigo'] = MagicMock()

    def _make_dev(self, device_type_id: str, props: dict) -> MagicMock:
        """Return a mock Indigo device with the given deviceTypeId and pluginProps."""
        dev              = MagicMock()
        dev.deviceTypeId = device_type_id
        dev.pluginProps  = props
        return dev

    def _make_adapter(self) -> MagicMock:
        """Return a minimal mock adapter with a real precision attribute."""
        adapter           = MagicMock()
        adapter.precision = 1
        return adapter

    # ===================================== _PredefinedDelegate =====================================
    def test_predefined_delegate_sets_converter_temperature(self):
        """_PredefinedDelegate reads scaleType/nativeScale/desiredScale/precision from pluginProps
        and stores a working converter on adapter.desired_scale."""
        dev     = self._make_dev('tempConvertedSensor', {
            'scaleType':    'temperature',
            'nativeScale':  'F',
            'desiredScale': 'C',
            'precision':    '1',
        })
        adapter = self._make_adapter()

        with patch('sensor_adapter.indigo'):
            from sensor_adapter import _PredefinedDelegate
            _PredefinedDelegate(dev, adapter)

        self.assertAlmostEqual(adapter.desired_scale.convert(32),  0.0,   1, "32°F should convert to 0°C.")
        self.assertAlmostEqual(adapter.desired_scale.convert(212), 100.0, 1, "212°F should convert to 100°C.")

    def test_predefined_delegate_sets_precision(self):
        """_PredefinedDelegate writes the precision from pluginProps back onto the adapter."""
        dev     = self._make_dev('tempConvertedSensor', {
            'scaleType':    'temperature',
            'nativeScale':  'F',
            'desiredScale': 'C',
            'precision':    '2',
        })
        adapter = self._make_adapter()

        with patch('sensor_adapter.indigo'):
            from sensor_adapter import _PredefinedDelegate
            _PredefinedDelegate(dev, adapter)

        self.assertEqual(adapter.precision, 2,
                         "Delegate should write int(pluginProps['precision']) to adapter.precision.")

    def test_predefined_delegate_name(self):
        """_PredefinedDelegate.name() should embed native device name, state name, and unit suffixes."""
        dev     = self._make_dev('tempConvertedSensor', {
            'scaleType':    'temperature',
            'nativeScale':  'F',
            'desiredScale': 'C',
            'precision':    '1',
        })
        adapter                          = self._make_adapter()
        adapter.native_device_name       = 'Living Room Sensor'
        adapter.native_device_state_name = 'temperature'

        with patch('sensor_adapter.indigo'):
            from sensor_adapter import _PredefinedDelegate
            delegate = _PredefinedDelegate(dev, adapter)

        name = delegate.name()
        self.assertIn('Living Room Sensor', name, "name() should contain the native device name.")
        self.assertIn('temperature',        name, "name() should contain the state name.")
        self.assertIn('F',                  name, "name() should contain the native unit suffix.")
        self.assertIn('C',                  name, "name() should contain the desired unit suffix.")

    # ===================================== _AffineTransformDelegate =====================================
    def test_affine_delegate_sets_measurement(self):
        """_AffineTransformDelegate reads multiplier/offset/format from pluginProps and stores a
        working AffineScaledMeasurement on adapter.desired_scale."""
        dev     = self._make_dev('customConvertedSensor', {
            'multiplier': '2.0',
            'offset':     '10.0',
            'format':     '{0:.1f} units',
        })
        adapter = self._make_adapter()

        with patch('sensor_adapter.indigo'):
            from sensor_adapter import _AffineTransformDelegate
            _AffineTransformDelegate(dev, adapter)

        self.assertAlmostEqual(adapter.desired_scale.convert(5), 20.0, 5, "(5 * 2.0) + 10.0 should equal 20.0.")
        self.assertEqual(adapter.desired_scale.format(5), "20.0 units",
                         "format() should apply the configured format_string.")

    def test_affine_delegate_name(self):
        """_AffineTransformDelegate.name() should embed native device name, state name, and format string."""
        dev     = self._make_dev('customConvertedSensor', {
            'multiplier': '1.0',
            'offset':     '0.0',
            'format':     '{0:.1f} units',
        })
        adapter                          = self._make_adapter()
        adapter.native_device_name       = 'Power Meter'
        adapter.native_device_state_name = 'watts'

        with patch('sensor_adapter.indigo'):
            from sensor_adapter import _AffineTransformDelegate
            delegate = _AffineTransformDelegate(dev, adapter)

        name = delegate.name()
        self.assertIn('Power Meter',      name, "name() should contain the native device name.")
        self.assertIn('watts',            name, "name() should contain the state name.")
        self.assertIn('{0:.1f} units',    name, "name() should contain the format string.")

    # ===================================== _FormulaDelegate =====================================
    def test_formula_delegate_sets_measurement(self):
        """_FormulaDelegate reads formula/format from pluginProps and stores a working
        ArbitraryFormulaScaledMeasurement on adapter.desired_scale."""
        dev     = self._make_dev('formulaConvertedSensor', {
            'formula': '(9/5 * x) + 32',
            'format':  '{0:.1f} °F',
        })
        adapter = self._make_adapter()

        with patch('sensor_adapter.indigo'):
            from sensor_adapter import _FormulaDelegate
            _FormulaDelegate(dev, adapter)

        self.assertAlmostEqual(adapter.desired_scale.convert(0),   32.0,  5, "C->F formula: 0°C should yield 32°F.")
        self.assertAlmostEqual(adapter.desired_scale.convert(100), 212.0, 5, "C->F formula: 100°C should yield 212°F.")
        self.assertEqual(adapter.desired_scale.format(0), "32.0 °F",
                         "format() should apply the configured format_string.")

    def test_formula_delegate_name(self):
        """_FormulaDelegate.name() should embed native device name, state name, and format string."""
        dev     = self._make_dev('formulaConvertedSensor', {
            'formula': 'x * 2',
            'format':  '{0:.1f} result',
        })
        adapter                          = self._make_adapter()
        adapter.native_device_name       = 'Temp Sensor'
        adapter.native_device_state_name = 'sensorValue'

        with patch('sensor_adapter.indigo'):
            from sensor_adapter import _FormulaDelegate
            delegate = _FormulaDelegate(dev, adapter)

        name = delegate.name()
        self.assertIn('Temp Sensor',       name, "name() should contain the native device name.")
        self.assertIn('sensorValue',       name, "name() should contain the state name.")
        self.assertIn('{0:.1f} result',    name, "name() should contain the format string.")

    # ===================================== SensorAdapter.go() =====================================
    def test_go_converts_and_updates_state(self):
        """SensorAdapter.go() should read the native value, convert it, and call
        dev.updateStateOnServer with the converted value and formatted string."""
        with patch('sensor_adapter.indigo') as mock_indigo:
            from sensor_adapter import SensorAdapter

            mock_indigo.devices[99].states.__getitem__ = MagicMock(return_value=0.0)

            sa                           = SensorAdapter.__new__(SensorAdapter)
            sa.logging                   = logging.getLogger('test')
            sa.native_device_id          = 99
            sa.native_device_state_name  = 'temperature'
            sa.precision                 = 1
            sa.dev                       = MagicMock()
            sa.desired_scale             = AffineScaledMeasurement(
                multiplier=1.8, offset=32.0, format_string="{0:.1f} °F"
            )
            sa.delegate                  = MagicMock()
            sa.delegate.name.return_value = 'test adapter'

            result = sa.go()

        self.assertEqual(result, "32.0 °F", "go() should return the formatted converted value.")
        sa.dev.updateStateOnServer.assert_called_once_with(
            key="sensorValue",
            value=32.0,
            decimalPlaces=1,
            uiValue="32.0 °F",
        )
