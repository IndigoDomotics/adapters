#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pyrescaler import *


SCALE_TYPE = "power"

# Internal canonical representation is watts
#
class PowerScale(ScaledMeasurement):
	def __init__(self, input_scale=None):
		ScaledMeasurement.__init__(self, input_scale)
		print "%s: %s" % (self.suffix(), self.__class__)

class Watts(PowerScale):
	def __init__(self, input_scale=None):
		PowerScale.__init__(self, input_scale)

	# nothing to do; canonical representation
	def _to_canonical(self, x):
		return float(x)

	# nothing to do; canonical representation
	def _from_canonical(self, x):
		return float(x)

	def suffix(self):
		return u"W"

register_scale(SCALE_TYPE, "Watts", "W", Watts)


class Kilowatts(PowerScale):
	def __init__(self, input_scale=None):
		PowerScale.__init__(self, input_scale)

	# kW -> W
	def _to_canonical(self, x):
		return float(x) * 1000

	# W -> kW
	def _from_canonical(self, x):
		return float(x) / 1000

	def suffix(self):
		return u"kW"

register_scale(SCALE_TYPE, "Kilowatts", "kW", Kilowatts)


class Horsepower(PowerScale):
	def __init__(self, input_scale=None):
		PowerScale.__init__(self, input_scale)

	# hp -> W
	def _to_canonical(self, x):
		return float(x) * 745.69987158227

	# W -> hp
	def _from_canonical(self, x):
		return float(x) / 745.69987158227

	def suffix(self):
		return u"hp"

register_scale(SCALE_TYPE, "Horsepower", "hp", Horsepower)
