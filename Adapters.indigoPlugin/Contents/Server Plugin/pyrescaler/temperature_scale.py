#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pyrescaler import *

SCALE_TYPE = "temperature"

# Internal canonical representation is Kelvin
#
class TemperatureScale(PredefinedScaledMeasurement):
	def __init__(self, input_scale=None, precision=1):
		PredefinedScaledMeasurement.__init__(self, input_scale, precision=precision)


class Fahrenheit(TemperatureScale):
	def __init__(self, input_scale=None, precision=1):
		TemperatureScale.__init__(self, input_scale, precision=precision)

	# F -> K
	def _to_canonical(self, f_temp):
		return (459.67 + float(f_temp)) * 5 / 9

	# K -> F
	def _from_canonical(self, k_temp):
		return (1.8 * float(k_temp)) - 459.67

	def suffix(self):
		return u"°F"

register_scale(SCALE_TYPE, "Fahrenheit", "F", Fahrenheit)


class Celsius(TemperatureScale):
	def __init__(self, input_scale=None, precision=1):
		TemperatureScale.__init__(self, input_scale, precision=precision)

	# C -> K
	def _to_canonical(self, c_temp):
		return float(c_temp) + 273.15

	# K -> C
	def _from_canonical(self, k_temp):
		return float(k_temp) - 273.15

	def suffix(self):
		return u"°C"

register_scale(SCALE_TYPE, "Celsius", "C", Celsius)


class Kelvin(TemperatureScale):
	def __init__(self, input_scale=None, precision=1):
		TemperatureScale.__init__(self, input_scale, precision=precision)

	def _to_canonical(self, k_temp):
		# Kelvin is the canonical representation, so nothing to do
		return float(k_temp)

	def _from_canonical(self, k_temp):
		# Kelvin is the canonical representation, so nothing to do
		return float(k_temp)

	def suffix(self):
		return u"K"

register_scale(SCALE_TYPE, "Kelvin", "K", Kelvin)


class Rankine(TemperatureScale):
	def __init__(self, input_scale=None, precision=1):
		TemperatureScale.__init__(self, input_scale, precision=precision)

	# R -> K
	def _to_canonical(self, r_temp):
		return float(r_temp) * 5 / 9

	# K -> R
	def _from_canonical(self, k_temp):
		return 1.8 * float(k_temp)

	def suffix(self):
		return u"°Ra"

register_scale(SCALE_TYPE, "Rankine", "R", Rankine)
