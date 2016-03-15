import logging
import indigo
from temperature_scale import *

class SensorAdapter:
	def __init__(self, dev):
		self.log = logging.getLogger('indigo.temp-converter.plugin')

		self.dev = dev
		self.address = dev.pluginProps["address"]

		self.desired_scale = temperature_converter(dev.pluginProps["nativeScale"], dev.pluginProps["desiredScale"])

		native_device_info = self.address.split(".", 1)
		self.native_device_id = int(native_device_info[0])
		self.native_device_state_name = native_device_info[1]
		self.native_device_name = indigo.devices[self.native_device_id].name

		self.log.debug("new adapter: %s" % self.name())

		self.go()

	def name(self):
		return "%s['%s'] %s -> %s" % (self.native_device_name, self.native_device_state_name, self.desired_scale.suffix_native(), self.desired_scale.suffix())

	def go(self):
		native_value = indigo.devices[self.native_device_id].states[self.native_device_state_name]
		cv = self.desired_scale.report(self.dev, "temperature", native_value)
		self.log.debug("%s: %s -> %s" % (self.name(), self.desired_scale.format_native(native_value), cv))
