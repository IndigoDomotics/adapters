# noqa pylint: disable=too-many-lines, line-too-long, invalid-name, unused-argument, redefined-builtin, broad-except, fixme

from pyrescaler import *


SCALE_TYPE = "length"

# Internal canonical representation is meters
#
class LengthScale(PredefinedScaledMeasurement):
	def __init__(self, input_scale=None, precision=1):
		PredefinedScaledMeasurement.__init__(self, input_scale, precision=precision)
		print("%s: %s" % (self.suffix(), self.__class__))

class Inches(LengthScale):
	def __init__(self, input_scale=None, precision=1):
		LengthScale.__init__(self, input_scale, precision=precision)

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
	def __init__(self, input_scale=None, precision=1):
		LengthScale.__init__(self, input_scale, precision=precision)

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
	def __init__(self, input_scale=None, precision=1):
		LengthScale.__init__(self, input_scale, precision=precision)

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
	def __init__(self, input_scale=None, precision=1):
		LengthScale.__init__(self, input_scale, precision=precision)

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
	def __init__(self, input_scale=None, precision=1):
		LengthScale.__init__(self, input_scale, precision=precision)

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
	def __init__(self, input_scale=None, precision=1):
		LengthScale.__init__(self, input_scale, precision=precision)

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
	def __init__(self, input_scale=None, precision=1):
		LengthScale.__init__(self, input_scale, precision=precision)

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
	def __init__(self, input_scale=None, precision=1):
		LengthScale.__init__(self, input_scale, precision=precision)

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
	def __init__(self, input_scale=None, precision=1):
		LengthScale.__init__(self, input_scale, precision=precision)

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
	def __init__(self, input_scale=None, precision=1):
		LengthScale.__init__(self, input_scale, precision=precision)

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
	def __init__(self, input_scale=None, precision=1):
		LengthScale.__init__(self, input_scale, precision=precision)

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
