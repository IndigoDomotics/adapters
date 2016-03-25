#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pyrescaler import *


SCALE_TYPE = "length"

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

register_scale(SCALE_TYPE, "Inches", "in", Inches)


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

register_scale(SCALE_TYPE, "Feet", "ft", Feet)


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

register_scale(SCALE_TYPE, "Yards", "yd", Yards)

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

register_scale(SCALE_TYPE, "Miles", "mi", Miles)


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

register_scale(SCALE_TYPE, "Centimeters", "cm", Centimeters)


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

register_scale(SCALE_TYPE, "Meters", "m", Meters)


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

register_scale(SCALE_TYPE, "Kilometers", "km", Kilometers)


class NauticalMiles(LengthScale):
	def __init__(self, input_scale=None):
		LengthScale.__init__(self, input_scale)

	# nmi -> m
	def _to_canonical(self, x):
		return float(x) * 1852

	# m -> nmi
	def _from_canonical(self, x):
		return float(x) / 1852

	def suffix(self):
		return u"nmi"

register_scale(SCALE_TYPE, "Nautical Miles", "nmi", NauticalMiles)


class Fathoms(LengthScale):
	def __init__(self, input_scale=None):
		LengthScale.__init__(self, input_scale)

	# fm -> m
	def _to_canonical(self, x):
		return float(x) * 1.8288

	# m -> fm
	def _from_canonical(self, x):
		return float(x) / 1.8288

	def suffix(self):
		return u"fm"

register_scale(SCALE_TYPE, "Fathoms", "fm", Fathoms)


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

register_scale(SCALE_TYPE, "Cubits", "cbt", Cubits)


class Hands(LengthScale):
	def __init__(self, input_scale=None):
		LengthScale.__init__(self, input_scale)

	# h -> m
	def _to_canonical(self, x):
		return float(x) / 9.84252

	# m -> h
	def _from_canonical(self, x):
		return float(x) * 9.84252

	def suffix(self):
		return u"h"

register_scale(SCALE_TYPE, "Hands", "h", Hands)


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
