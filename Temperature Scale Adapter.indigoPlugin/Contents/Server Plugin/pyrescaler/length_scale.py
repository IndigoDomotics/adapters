#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pyrescaler import *


def _decode_scale_name(key):
	if 'm' == key:
		return Meters()
	elif 'in' == key:
		return Inches()
	elif 'ft' == key:
		return Feet()
	elif 'yd' == key:
		return Yards()
	elif 'mi' == key:
		return Miles()
	elif 'cm' == key:
		return Centimeters()
	elif 'km' == key:
		return Kilometers()
	elif 'cbt' == key:
		return Cubits()
	else:
		return None

def length_converter(native_scale_key, desired_scale_key):
	return _decode_scale_name(desired_scale_key)._with_input_scale(_decode_scale_name(native_scale_key))

# Internal canonical representation is meters
#
class LengthScale(ScaledMeasurement):
	def __init__(self, input_scale=None):
		ScaledMeasurement.__init__(self, input_scale)
		print "%s: %s" % (self.suffix(), self.__class__)

class Inches(LengthScale):
	def __init__(self, input_scale=None):
		LengthScale.__init__(self, input_scale)

	# in -> m
	def _to_canonical(self, x):
		return float(x) * 0.0254

	# m -> in
	def _from_canonical(self, x):
		return float(x) / 0.0254

	def suffix(self):
		return u"in"

class Feet(LengthScale):
	def __init__(self, input_scale=None):
		LengthScale.__init__(self, input_scale)

	# ft -> m
	def _to_canonical(self, x):
		return float(x) * 0.3048

	# m -> ft
	def _from_canonical(self, x):
		return float(x) * 3.2808

	def suffix(self):
		return u"ft"

class Yards(LengthScale):
	def __init__(self, input_scale=None):
		LengthScale.__init__(self, input_scale)

	# yd -> m
	def _to_canonical(self, x):
		return float(x) / 1.0936

	# m -> yd
	def _from_canonical(self, x):
		return float(x) * 1.0936

	def suffix(self):
		return u"yd"

# class Furlongs(LengthScale):
# 	def __init__(self, input_scale=None):
# 		LengthScale.__init__(self, input_scale)

class Miles(LengthScale):
	def __init__(self, input_scale=None):
		LengthScale.__init__(self, input_scale)

	# mi -> m
	def _to_canonical(self, x):
		return float(x) * 1609.34

	# m -> mi
	def _from_canonical(self, x):
		return float(x) / 1609.34

	def suffix(self):
		return u"mi"

class Centimeters(LengthScale):
	def __init__(self, input_scale=None):
		LengthScale.__init__(self, input_scale)

	# cm -> m
	def _to_canonical(self, x):
		return float(x) / 100

	# m -> cm
	def _from_canonical(self, x):
		return float(x) * 100

	def suffix(self):
		return u"cm"

class Meters(LengthScale):
	def __init__(self, input_scale=None):
		LengthScale.__init__(self, input_scale)

	# no change
	def _to_canonical(self, x):
		return float(x)

	# no change
	def _from_canonical(self, x):
		return float(x)

	def suffix(self):
		return u"m"

class Kilometers(LengthScale):
	def __init__(self, input_scale=None):
		LengthScale.__init__(self, input_scale)

	# km -> m
	def _to_canonical(self, x):
		return float(x) * 1000

	# m -> km
	def _from_canonical(self, x):
		return float(x) / 1000

	def suffix(self):
		return u"km"

# class NauticalMiles(LengthScale):
# 	def __init__(self, input_scale=None):
# 		LengthScale.__init__(self, input_scale)
#
# class Fathoms(LengthScale):
# 	def __init__(self, input_scale=None):
# 		LengthScale.__init__(self, input_scale)

class Cubits(LengthScale):
	def __init__(self, input_scale=None):
		LengthScale.__init__(self, input_scale)

	# cbt -> m
	def _to_canonical(self, x):
		return float(x) / 2.18723

	# m -> cbt
	def _from_canonical(self, x):
		return float(x) * 2.18723

	def suffix(self):
		return u"cbt"

# class Hands(LengthScale):
# 	def __init__(self, input_scale=None):
# 		LengthScale.__init__(self, input_scale)
#
# class Parsecs(LengthScale):
# 	def __init__(self, input_scale=None):
# 		LengthScale.__init__(self, input_scale)
#
# class LightYears(LengthScale):
# 	def __init__(self, input_scale=None):
# 		LengthScale.__init__(self, input_scale)
#
# class Angstroms(LengthScale):
# 	def __init__(self, input_scale=None):
# 		LengthScale.__init__(self, input_scale)
