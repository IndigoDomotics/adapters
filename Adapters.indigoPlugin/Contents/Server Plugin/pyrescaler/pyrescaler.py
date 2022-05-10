import logging
import sys
sys.path.append("Adapters.indigoPlugin/Contents/Server Plugin")
from simpleeval import simple_eval


FORMAT_STRING = "{0:.1f}"

_all_scales = {}
_log = logging.getLogger('pyrescaler')


def _decode_scale_name(scale_type, key, precision=1):
	# return [
	# 	a[1](precision=precision)
	# 	for a in _all_scales[scale_type]
	# 	if a[0] == key
	# ][0]
	bar = []
	for a in _all_scales[scale_type]:
		if a[0] == key:
			bar.append(a[1](precision=precision))
	return bar[0]

def get_scale_options(scale_type=None):
	foo = []
	# foo = [
	# 	(a[0], a[2])
	# 	for k in _all_scales.keys()
	# 	if scale_type is None or (scale_type == k)
	# 	for a in _all_scales[k]
	# ]
	# scale_type = 'temperature', 'power', or 'length'
	_log.debug(f"get_scale_options._all_scales = {_all_scales}")
	for k in _all_scales.keys():
		if scale_type is None or (scale_type == k):
			for a in _all_scales[k]:
				foo.append((a[0], a[2]))
	return foo


def register_scale(scale_type, scale_name, scale_key, scale_class):
	if scale_type not in _all_scales:
		_all_scales[scale_type] = []
	_log.debug("registered '%s' scale '%s' (%s)" % (scale_type, scale_name, scale_key))
	_all_scales[scale_type].append((scale_key, scale_class, scale_name))
	_log.debug(f"register_scale._all_scales = {_all_scales}")


def get_converter(scale_type, native_scale_key, desired_scale_key, precision=1):
	return _decode_scale_name(scale_type, desired_scale_key, precision)._with_input_scale(_decode_scale_name(scale_type, native_scale_key))


class ScaledMeasurement:
	def __init__(self):
		pass

	def format(self, reading):
		pass

	def convert(self, reading):
		pass


class PredefinedScaledMeasurement(ScaledMeasurement):
	def __init__(self, i_s=None, precision=1):
		ScaledMeasurement.__init__(self)
		self.precision = precision
		if i_s:
			self.input_scale = i_s
		else:
			self.input_scale = self

	def set_input_scale(self, i_s):
		self.input_scale = i_s

	def _with_input_scale(self, i_s):
		self.input_scale = i_s
		return self

	def format(self, reading):
		format_with_precision = u"{{0:.{0:d}f}} {{1}}".format(self.precision)
		_log.debug("resulting format with precision applied: %s" % format_with_precision)
		result = format_with_precision.format(self.convert(reading), self.suffix())
		_log.debug("formatted result: %s" % result)
		return result

	def format_native(self, reading):
		return self.input_scale.format(reading)

	def convert(self, reading):
		return self._from_canonical(self.input_scale._to_canonical(reading))

	def suffix_native(self):
		return self.input_scale.suffix()


class AffineScaledMeasurement(ScaledMeasurement):
	def __init__(self, offset=0.0, multiplier=1.0, format_string="{0:.1f}"):
		self.offset = offset
		self.multiplier = multiplier
		self.format_string = format_string

	def format(self, reading):
		return self.format_string.format(self.convert(reading))

	def convert(self, reading):
		return (float(reading) * float(self.multiplier)) + float(self.offset)


class ArbitaryFormulaScaledMeasurement(ScaledMeasurement):
	def __init__(self, formula="x", format_string="{0:.1f}"):
		self.formula = formula
		self.format_string = format_string

	def format(self, reading):
		return self.format_string.format(self.convert(reading))

	def convert(self, reading):
		return simple_eval(self.formula, names={"x": float(reading)})
