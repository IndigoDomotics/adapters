#! /usr/bin/env python
# -*- coding: utf-8 -*-

FORMAT_STRING = "{0:.1f}"
DEFAULT_INPUT_SCALE = None

def _decode_scale_name(key):
	if 'F' == key:
		return Fahrenheit()
	elif 'C' == key:
		return Celsius()
	elif 'K' == key:
		return Kelvin()
	elif 'R' == key:
		return Rankine()

def temperature_converter(native_scale_key, desired_scale_key):
	native_scale = _decode_scale_name(native_scale_key)
	native_scale.set_input_scale(native_scale)

	desired_scale = _decode_scale_name(desired_scale_key)
	desired_scale.set_input_scale(native_scale)

	return desired_scale

# Internal canonical representation is Kelvin
#
class TemperatureScale:
	def __init__(self, i_s=DEFAULT_INPUT_SCALE):
		self.input_scale = i_s

	def set_input_scale(self, i_s):
		self.input_scale = i_s

	# for indigo HA software
	def report(self, dev, stateKey, reading):
		txt = self.format(reading)
		dev.updateStateOnServer(key=stateKey, value=self.convert(reading), decimalPlaces=1, uiValue=txt)
		return txt

	def format(self, reading):
		return u"%s%s" % (FORMAT_STRING.format(self.convert(reading)), self.suffix())

	def format_native(self, reading):
		return self.input_scale.format(reading)

	def convert(self, reading):
		return self._from_canonical(self.input_scale._to_canonical(reading))

	def suffix_native(self):
		return self.input_scale.suffix()


class Fahrenheit(TemperatureScale):
	def __init__(self, input_scale=DEFAULT_INPUT_SCALE):
		TemperatureScale.__init__(self, input_scale)

	# F -> K
	def _to_canonical(self, f_temp):
		return (459.67 + f_temp) * 5 / 9

	# K -> F
	def _from_canonical(self, k_temp):
		return (1.8 * k_temp) - 459.67

	def suffix(self):
		return u"°F"


class Celsius(TemperatureScale):
	def __init__(self, input_scale=DEFAULT_INPUT_SCALE):
		TemperatureScale.__init__(self, input_scale)

	# C -> K
	def _to_canonical(self, c_temp):
		return 273.15 + c_temp

	# K -> C
	def _from_canonical(self, k_temp):
		return (-273.15) + k_temp

	def suffix(self):
		return u"°C"


class Kelvin(TemperatureScale):
	def __init__(self, input_scale=DEFAULT_INPUT_SCALE):
		TemperatureScale.__init__(self, input_scale)

	def _to_canonical(self, k_temp):
		# Kelvin is the canonical representation, so nothing to do
		return 0.0 + k_temp

	def _from_canonical(self, k_temp):
		# Kelvin is the canonical representation, so nothing to do
		return 0.0 + k_temp

	def suffix(self):
		return u"K"


class Rankine(TemperatureScale):
	def __init__(self, input_scale=DEFAULT_INPUT_SCALE):
		TemperatureScale.__init__(self, input_scale)

	# R -> K
	def _to_canonical(self, r_temp):
		return float(r_temp) * 5 / 9

	# K -> R
	def _from_canonical(self, k_temp):
		return 1.8 * k_temp

	def suffix(self):
		return u"°Ra"


DEFAULT_INPUT_SCALE = Fahrenheit()
