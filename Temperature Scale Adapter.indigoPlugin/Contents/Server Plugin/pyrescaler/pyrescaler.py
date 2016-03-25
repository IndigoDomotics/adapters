#! /usr/bin/env python
# -*- coding: utf-8 -*-

FORMAT_STRING = "{0:.1f}"

class ScaledMeasurement:
	def __init__(self, i_s=None):
		if (i_s):
			self.input_scale = i_s
		else:
			self.input_scale = self

	def set_input_scale(self, i_s):
		self.input_scale = i_s

	def _with_input_scale(self, i_s):
		self.input_scale = i_s
		return self

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
