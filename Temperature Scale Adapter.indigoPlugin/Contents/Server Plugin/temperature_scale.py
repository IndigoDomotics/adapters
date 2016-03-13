#! /usr/bin/env python
# -*- coding: utf-8 -*-

FORMAT_STRING = "{0:.1f}"
DEFAULT_INPUT_SCALE = None

# Internal canonical representation is Kelvin
#
class TemperatureScale:
	input_scale = None

	def __init__(self, i_s=DEFAULT_INPUT_SCALE):
		input_scale = i_s

	def report(self, dev, stateKey, reading):
		txt = self.format(reading)
		dev.updateStateOnServer(key=stateKey, value=self.convert(reading), decimalPlaces=1, uiValue=txt)
		return txt

	def format(self, reading):
		return u"%s%s" % (FORMAT_STRING.format(self.convert(reading)), self.suffix())

	def convert(self, reading):
		return self._from_canonical(input_scale.to_canonical(reading))


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
