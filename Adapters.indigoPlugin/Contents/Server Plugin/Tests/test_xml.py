"""
Test Plugin XML files for format and content

The test_xml file tests the XML files located in the plugin package for format and content and will flag entries that
are incomplete or don't comport with XML (and Indigo) conventions. These tests do not require access to the Indigo IOM,
can be run from an IDE, and do not require the plugin to be installed or enabled. The files tested are listed in the
setUpClass method below. The tests include checks for required elements (like element `id` and `type` attributes) and
syntax.

The code below may need to be modified to run on different environments (specifically, references to where the files
are stored) within an IDE or from the command line. Using the BASE_PATH variable in .env makes this easier.

For example, in Terminal run this test with:
    > cd <path/to/test/folder/>
    > export PYTHONPATH=/path/to/your/repo/Adapters.indigoPlugin/Contents/Server\ Plugin
    > python -m unittest test_xml

The change to the PYTHONPATH in Terminal will revert when Terminal is closed (or you reset it).
"""
import dotenv
from unittest import TestCase
from indigo_devices_filters import DEVICE_FILTERS
from httpcodes import codes as httpcodes
import httpx
import os
import xml.etree.ElementTree as ET  # noqa


dotenv.load_dotenv()
BASE_PATH = os.getenv('BASE_PATH')


class TestXml(TestCase):
    """
    The TestXml class is used to test the various XML files that are part of a standard Indigo plugin.

    The files tested are listed in the setUpClass method below. The tests include checks for required elements (like
    element `id` and `type` attributes) and syntax.
    """
    @classmethod
    def setUpClass(cls):
        cls.xml_files   = [f'{BASE_PATH}/Actions.xml', f'{BASE_PATH}/MenuItems.xml', f'{BASE_PATH}/Devices.xml', f'{BASE_PATH}/Events.xml']
        cls.field_types = ['button', 'checkbox', 'colorpicker', 'label', 'list', 'menu', 'separator', 'textfield']
        # Load the plugin.py code into a var for testing later.
        with open(f'{BASE_PATH}/plugin.py', 'r') as infile:
            cls.plugin_lines = infile.read()

    @staticmethod
    def get_item_name(xml_file: str, item_id: int):
        tree = ET.parse(xml_file)
        return tree.getroot()

    def test_xml_files(self):
        try:
            for file_type in self.xml_files:
                try:
                    root = self.get_item_name(file_type, 0)
                except FileNotFoundError:
                    print(f"\"{file_type}\" file not present.")
                    continue
                for item in root:
                    # Test the 'id' attribute (required):
                    node_id = item.get('id')
                    self.assertIsNotNone(node_id,
                                         f"\"{file_type}\" element \"{item.tag}\" attribute 'id' is required.")
                    self.assertIsInstance(node_id, str, "id names must be strings.")
                    self.assertNotIn(' ', node_id, f"`id` names should not contain spaces.")

                    # Test the 'deviceFilter' attribute:
                    dev_filter = item.get('deviceFilter', "")
                    self.assertIsInstance(dev_filter, str, "`deviceFilter` values must be strings.")
                    if dev_filter:  # None if not specified in item attributes
                        self.assertIn(dev_filter, DEVICE_FILTERS, "'deviceFilter' values must be strings.")

                    # Test the 'uiPath' attribute. It can be essentially anything as long as it's a string.
                    ui_path = item.get('uiPath', "")
                    self.assertIsInstance(ui_path, str, "uiPath names must be strings.")

                # Test items that have a 'Name' element. The reference to `root.tag[:-1]` takes the tag name and
                # converts it to the appropriate child element name. For example, `Actions` -> `Action`, etc.
                for thing in root.findall(f"./{root.tag[:-1]}/Name"):
                    self.assertIsInstance(thing.text, str, "Action names must be strings.")

                # Test items that have a 'CallBackMethod` element:
                for thing in root.findall(f"./{root.tag[:-1]}/CallbackMethod"):
                    self.assertIsInstance(thing.text, str, "Action callback names must be strings.")
                    # We can't directly access the plugin.py file from here, so we read it into a variable instead.
                    # We then search for the string `def <CALLBACK METHOD>` within the file as a proxy to doing a
                    # `dir()` to see if it's in there.
                    self.assertTrue(f"def {thing.text}" in self.plugin_lines,
                                    f"The callback method \"{thing.text}\" does not exist in the plugin.py file.")

                # Test items that have a 'configUI' element
                for thing in root.findall(f"./{root.tag[:-1]}/ConfigUI/SupportURL"):
                    self.assertIsInstance(thing.text, str, "Config UI support URLs must be strings.")
                    result = httpx.get(thing.text).status_code
                    self.assertEqual(result, 200,
                                     f"ERROR: Got status code {result} -> {httpcodes[result]}.")

                # Test Config UI `Field` elements
                for thing in root.findall(f"./{root.tag[:-1]}/ConfigUI/Field"):
                    # Required attributes. Will throw a KeyError if missing.
                    self.assertIsInstance(thing.attrib['id'], str, "Config UI field IDs must be strings.")
                    self.assertFalse(thing.attrib['id'] == "", "Config UI field IDs must not be an empty string.")
                    self.assertIsInstance(thing.attrib['type'], str, "Config UI field types must be strings.")
                    self.assertIn(thing.attrib['type'], self.field_types,
                                  f"Config UI field types must be one of {self.field_types}.")
                    # Optional attributes
                    self.assertIsInstance(thing.attrib.get('defaultValue', ""), str,
                                          "Config UI defaultValue types must be strings.")
                    self.assertIsInstance(thing.attrib.get('enabledBindingId', ""), str,
                                          "Config UI enabledBindingId types must be strings.")
                    self.assertIsInstance(thing.attrib.get('enabledBindingNegate', ""), str,
                                          "Config UI enabledBindingNegate types must be strings.")
                    self.assertIn(thing.attrib.get('hidden', "false"), ['true', 'false'],
                                  f"Config UI hidden attribute must be 'true' or 'false'.")
                    self.assertIn(thing.attrib.get('readonly', "false"), ['true', 'false'],
                                  f"Config UI readonly attribute must be 'true' or 'false'.")
                    self.assertIn(thing.attrib.get('secure', "false"), ['true', 'false'],
                                  f"Config UI secure attribute must be 'true' or 'false'.")
                    self.assertIsInstance(thing.attrib.get('tooltip', ""), str,
                                          "Config UI field tool tips must be strings.")
                    self.assertIsInstance(thing.attrib.get('visibleBindingId', ""), str,
                                          "Config UI visibleBindingId types must be strings.")
                    self.assertIsInstance(thing.attrib.get('visibleBindingValue', ""), str,
                                          "Config UI visibleBindingValue types must be strings.")

        except AssertionError as err:
            print(f"ERROR: {self._testMethodName}: {err}")
