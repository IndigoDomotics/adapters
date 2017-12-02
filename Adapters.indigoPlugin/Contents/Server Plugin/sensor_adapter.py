import logging
import indigo
import yaml
from simpleeval import simple_eval



DEFAULT_FORMAT_STRING = "{0:.1f}"
_log = logging.getLogger('pyrescaler')

# Read in list of predefined scales from YAML file
stream = file('scales.yaml', 'r')
try:
	scales = yaml.load(stream)
except yaml.YAMLError, exc:
	print "Error in YAML file: ", exc

print "scales: %s" % yaml.dump(scales)

def get_scale_options(scale_type):
	return [
		(a['key'], a['name'])
		for a in scales[scale_type]
	]

def get_scale(scale_type, scale_key):
	return [
		a
		for a in scales[scale_type]
		if a["key"] == scale_key
	][0]


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
		self.log.debug("initializing adapter of device type '%s'" % (self.dev.deviceTypeId))

		if "precision" in dev.pluginProps:
			self.precision = int(dev.pluginProps["precision"])
		else:
			self.precision = 1

		if "linearConvertedSensor" == self.dev.deviceTypeId:
			# linear/affine transformation
			self.desired_scale = ArbitaryFormulaScaledMeasurement(
				formula="(x * %f) + %f" % (float(dev.pluginProps["multiplier"]), float(dev.pluginProps["offset"])),
				format_string=dev.pluginProps["format"])
		elif "tempConvertedSensor" == self.dev.deviceTypeId:
			# predefined scale conversion
			#   find the objects representing the two scales ('from'/'native' and 'to'/'desired') in our data structure
			from_scale = get_scale(dev.pluginProps["scaleType"], dev.pluginProps["nativeScale"])
			to_scale = get_scale(dev.pluginProps["scaleType"], dev.pluginProps["desiredScale"])
			#   format string built dynamically based on the user's selected precision value
			format_string = u"{{0:.{0:d}f}} ".format(self.precision) + to_scale["suffix"]
			# 	formula string also built dynamically by connverting first from native to canonical, then from canonical to desired
			native_to_canonical_formula = from_scale["to_c"]
			canonical_to_desired_formula = to_scale["from_c"]
			#     to get our desired calculation, the result of the "to-canonical" formula is the input into the "from-canonical" formula.
			#       surround the native-to-canonical formula in parentheses to avoid operator precedence issues.
			full_formula = canonical_to_desired_formula.replace('x', '('+native_to_canonical_formula+")")
			#   Now we have all we need to just use a Formula delegate as we do in all other cases
			# self.delegate = _PredefinedDelegate (dev, self)
			self.desired_scale = ArbitaryFormulaScaledMeasurement(
				formula=full_formula,
				format_string=format_string)
		else:
			# custom formula transformation
			self.desired_scale = ArbitaryFormulaScaledMeasurement(
				formula=dev.pluginProps["formula"],
				format_string=dev.pluginProps["format"])

		self.log.debug("new adapter: %s" % self.name())

		self.go()

	def name(self):
		return "%s['%s'] %s" % (self.native_device_name, self.native_device_state_name, self.desired_scale.format_string)


	def go(self):
		native_value = indigo.devices[self.native_device_id].states[self.native_device_state_name]

		converted_txt = self.desired_scale.format(native_value)
		converted_value = self.desired_scale.convert(native_value)

		self.log.debug("converted results; numeric: '%f', formatted '%s'" % (converted_value, converted_txt))

		self.dev.updateStateOnServer(key="sensorValue", value=converted_value, decimalPlaces=self.precision, uiValue=converted_txt)
		self.log.debug("%s: %s" % (self.name(), converted_txt))


class ArbitaryFormulaScaledMeasurement:
	def __init__(self, formula="x", format_string=DEFAULT_FORMAT_STRING):
		_log.debug("creating new formula adapter; formula: '%s'  format string: '%s'"  % (formula, format_string))
		self.formula = formula
		self.format_string = format_string

	def format(self, reading):
		result = self.convert(reading)
		_log.debug("formatting '%f' using format string: '%s'" % (result, self.format_string))
		s = self.format_string.format(result)
		_log.debug("formatted result: '%s'" % (s))
		return s

	def convert(self, reading):
		_log.debug("converting using formula: '%s'" % (self.formula))
		result = simple_eval(self.formula, names={"x": float(reading)})
		_log.debug("conversion result: %f" % (result))
		return result
