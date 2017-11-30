import logging
import indigo
from pyrescaler.pyrescaler import get_converter, ArbitaryFormulaScaledMeasurement


DEFAULT_FORMAT_STRING = "{0:.1f}"

class SensorAdapter:
	def __init__(self, dev):
		self.log = logging.getLogger('indigo.temp-converter.plugin')

		self.dev = dev
		self.address = dev.pluginProps["address"]

		native_device_info = self.address.split(".", 1)
		self.native_device_id = int(native_device_info[0])
		self.native_device_state_name = native_device_info[1]
		self.native_device_name = indigo.devices[self.native_device_id].name

		# default
		self.precision = 1
		self.log.debug("initializing adapter of device type '%s'" % (self.dev.deviceTypeId))
		if "linearConvertedSensor" == self.dev.deviceTypeId:
			self.delegate = _FormulaDelegate(
				formula="(x * %f) + %f" % (float(dev.pluginProps["multiplier"]), float(dev.pluginProps["offset"])),
				format_string=dev.pluginProps["format"], 
				adapter=self)
		elif "tempConvertedSensor" == self.dev.deviceTypeId:
			self.delegate = _PredefinedDelegate (dev, self)
		else:
			self.delegate = _FormulaDelegate(
				formula=dev.pluginProps["formula"],
				format_string=dev.pluginProps["format"], 
				adapter=self)


		self.log.debug("new adapter: %s" % self.name())

		self.go()

	def name(self):
		return self.delegate.name()


	def go(self):
		native_value = indigo.devices[self.native_device_id].states[self.native_device_state_name]

		converted_txt = self.desired_scale.format(native_value)
		converted_value = self.desired_scale.convert(native_value)

		self.dev.updateStateOnServer(key="sensorValue", value=converted_value, decimalPlaces=self.precision, uiValue=converted_txt)
		self.log.debug("%s: %s" % (self.name(), converted_txt))

class _PredefinedDelegate:
	def __init__(self, dev, adapter):
		self.adapter = adapter
		self.scale_type = dev.pluginProps["scaleType"]

		if "precision" in dev.pluginProps:
			self.adapter.precision = int(dev.pluginProps["precision"])

		if 'temperature' == self.scale_type:
			# set icon to 'temperature sensor'
			dev.updateStateImageOnServer(indigo.kStateImageSel.TemperatureSensor)

		self.adapter.desired_scale = get_converter(self.scale_type, dev.pluginProps["nativeScale"], dev.pluginProps["desiredScale"], precision=self.adapter.precision)

	def name(self):
		return "%s['%s'] %s -> %s" % (self.adapter.native_device_name, self.adapter.native_device_state_name, self.adapter.desired_scale.suffix_native(), self.adapter.desired_scale.suffix())

class _FormulaDelegate:
	def __init__(self, formula="x", format_string=DEFAULT_FORMAT_STRING, adapter=None):
		self.adapter = adapter
		self.formula = formula
		self.format_string=format_string
		adapter.desired_scale = ArbitaryFormulaScaledMeasurement(self.formula, self.format_string)

	def name(self):
		return "%s['%s'] %s" % (self.adapter.native_device_name, self.adapter.native_device_state_name, self.format_string)
