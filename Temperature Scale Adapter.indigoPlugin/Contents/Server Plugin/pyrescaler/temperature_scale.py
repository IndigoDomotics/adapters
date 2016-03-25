#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pyrescaler import *


_scale_list = []

def _all_scales():
	return _scale_list
	# return [
	# 	('F', Fahrenheit, "Fahrenheit"),
	# 	('C', Celsius, "Celsius"),
	# 	('K', Kelvin, "Kelvin"),
	# 	('R', Rankine, "Rankine"),
	# ]

def _decode_scale_name(key):
	return [
		a[1]()
		for a in _scale_list
		if a[0] == key
	]

def get_temperature_scale_options():
	return [
		(a[0], a[2])
		for a in _scale_list
	]


def temperature_converter(native_scale_key, desired_scale_key):
	return _decode_scale_name(desired_scale_key)._with_input_scale(_decode_scale_name(native_scale_key))

# Internal canonical representation is Kelvin
#
class TemperatureScale(ScaledMeasurement):
	def __init__(self, input_scale=None):
		ScaledMeasurement.__init__(self, input_scale)


class Fahrenheit(TemperatureScale):
	def __init__(self, input_scale=None):
		TemperatureScale.__init__(self, input_scale)

	# F -> K
	def _to_canonical(self, f_temp):
		return (459.67 + float(f_temp)) * 5 / 9

	# K -> F
	def _from_canonical(self, k_temp):
		return (1.8 * float(k_temp)) - 459.67

	def suffix(self):
		return u"°F"

_scale_list.append(('F', Fahrenheit, "Fahrenheit"))

class Celsius(TemperatureScale):
	def __init__(self, input_scale=None):
		TemperatureScale.__init__(self, input_scale)

	# C -> K
	def _to_canonical(self, c_temp):
		return float(c_temp) + 273.15

	# K -> C
	def _from_canonical(self, k_temp):
		return float(k_temp) - 273.15

	def suffix(self):
		return u"°C"

_scale_list.append(('C', Celsius, "Celsius"))


class Kelvin(TemperatureScale):
	def __init__(self, input_scale=None):
		TemperatureScale.__init__(self, input_scale)

	def _to_canonical(self, k_temp):
		# Kelvin is the canonical representation, so nothing to do
		return float(k_temp)

	def _from_canonical(self, k_temp):
		# Kelvin is the canonical representation, so nothing to do
		return float(k_temp)

	def suffix(self):
		return u"K"

_scale_list.append(('K', Kelvin, "Kelvin"))


class Rankine(TemperatureScale):
	def __init__(self, input_scale=None):
		TemperatureScale.__init__(self, input_scale)

	# R -> K
	def _to_canonical(self, r_temp):
		return float(r_temp) * 5 / 9

	# K -> R
	def _from_canonical(self, k_temp):
		return 1.8 * float(k_temp)

	def suffix(self):
		return u"°Ra"

_scale_list.append(('R', Rankine, "Rankine"))
