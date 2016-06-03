import logging
import indigo
from pyrescaler.pyrescaler import get_converter, CustomScaledMeasurement

class SensorAdapter:
	def __init__(self, dev):
		self.log = logging.getLogger('indigo.temp-converter.plugin')

		self.dev = dev
		self.address = dev.pluginProps["address"]

		native_device_info = self.address.split(".", 1)
		self.native_device_id = int(native_device_info[0])
		self.native_device_state_name = native_device_info[1]
		self.native_device_name = indigo.devices[self.native_device_id].name

		if "customConvertedSensor" == self.dev.deviceTypeId:
			self.format=dev.pluginProps["format"]
			self.desired_scale = CustomScaledMeasurement(multiplier=dev.pluginProps["multiplier"],
				offset=dev.pluginProps["offset"], format_string=self.format)
			self.precision = 1 # only used in debugging messages
		else:
			self.scale_type = dev.pluginProps["scaleType"]

			self.precision = 1
			if "precision" in dev.pluginProps:
				self.precision = int(dev.pluginProps["precision"])

			if 'temperature' == self.scale_type:
				# set icon to 'temperature sensor'
				dev.updateStateImageOnServer(indigo.kStateImageSel.TemperatureSensor)

			self.desired_scale = get_converter(self.scale_type, dev.pluginProps["nativeScale"], dev.pluginProps["desiredScale"], precision=self.precision)


		self.log.debug("new adapter: %s" % self.name())

		self.go()

	def name(self):
		if "customConvertedSensor" == self.dev.deviceTypeId:
			return "%s['%s'] %s" % (self.native_device_name, self.native_device_state_name, self.format)
		else:
			return "%s['%s'] %s -> %s" % (self.native_device_name, self.native_device_state_name, self.desired_scale.suffix_native(), self.desired_scale.suffix())


	def go(self):
		native_value = indigo.devices[self.native_device_id].states[self.native_device_state_name]

		converted_txt = self.desired_scale.format(native_value)
		converted_value = self.desired_scale.convert(native_value)

		self.dev.updateStateOnServer(key="sensorValue", value=converted_value, decimalPlaces=self.precision, uiValue=converted_txt)

		if "customConvertedSensor" == self.dev.deviceTypeId:
			self.log.debug("%s: %s" % (self.name(), converted_txt))
		else:
			self.log.debug("%s: %s -> %s" % (self.name(), self.desired_scale.format_native(native_value), converted_txt))
