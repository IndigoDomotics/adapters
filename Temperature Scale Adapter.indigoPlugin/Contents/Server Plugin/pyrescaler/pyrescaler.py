#! /usr/bin/env python
# -*- coding: utf-8 -*-

FORMAT_STRING = "{0:.1f}"

import logging

_all_scales = {}
_log = logging.getLogger('pyrescaler')

def _decode_scale_name(scale_type, key):
	return [
		a[1]()
		for a in _all_scales[scale_type]
		if a[0] == key
	][0]

def get_scale_options(scale_type=None):
	return [
		(a[0], a[2])
		for k in _all_scales.keys()
			if (scale_type == None) or (scale_type == k)
		for a in _all_scales[k]
	]

def register_scale(scale_type, scale_name, scale_key, scale_class):
	if not scale_type in _all_scales:
		_all_scales[scale_type] = []
	_log.debug("registered '%s' scale '%s' (%s)" % (scale_type, scale_name, scale_key))
	_all_scales[scale_type].append((scale_key, scale_class, scale_name))

def get_converter(scale_type, native_scale_key, desired_scale_key):
	return _decode_scale_name(scale_type, desired_scale_key)._with_input_scale(_decode_scale_name(scale_type, native_scale_key))



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

import temperature_scale
import length_scale
