#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Docstring placeholder
"""

import logging
from simpleeval import simple_eval

FORMAT_STRING = "{0:.1f}"

_all_scales = {}
_logger = logging.getLogger('pyrescaler')


# ==============================================================================
def _decode_scale_name(scale_type, key, precision=1):
    """
    Docstring placeholder
    """
    item_list = []
    for scale in _all_scales[scale_type]:
        if scale[0] == key:
            item_list.append(scale[1](precision=precision))

    return item_list[0]


# ==============================================================================
def get_scale_options(scale_type=None):
    """
    Docstring placeholder
    """
    option_list = []
    for key in _all_scales.keys():
        if (scale_type is None) or (scale_type == key):
            for scale in _all_scales[key]:
                option_list.append((scale[0], scale[2]))
    return option_list


# ==============================================================================
def register_scale(scale_type, scale_name, scale_key, scale_class):
    """
    Docstring placeholder
    """
    if scale_type not in _all_scales:
        _all_scales[scale_type] = []
    _logger.debug(f"registered '{scale_type}' scale '{scale_name}' ({scale_key})")
    _all_scales[scale_type].append((scale_key, scale_class, scale_name))


# ==============================================================================
def get_converter(scale_type, native_scale_key, desired_scale_key, precision=1):
    """
    Docstring placeholder
    """
    return _decode_scale_name(scale_type, desired_scale_key, precision)._with_input_scale(_decode_scale_name(scale_type, native_scale_key))  # noqa


# ==============================================================================
class ScaledMeasurement:
    """
    Docstring placeholder
    """

    # ==============================================================================
    def __init__(self):
        """
        Docstring placeholder
        """
        pass

    # ==============================================================================
    def format(self, reading):
        """
        Docstring placeholder
        """
        pass

    # ==============================================================================
    def convert(self, reading):
        """
        Docstring placeholder
        """
        pass


# ==============================================================================
class PredefinedScaledMeasurement(ScaledMeasurement):
    """
    Docstring placeholder
    """

    # ==============================================================================
    def __init__(self, i_s=None, precision=1):
        ScaledMeasurement.__init__(self)
        self.precision = precision
        if i_s:
            self.input_scale = i_s
        else:
            self.input_scale = self

    # ==============================================================================
    def set_input_scale(self, i_s):
        """
        Docstring placeholder
        """
        self.input_scale = i_s

    # ==============================================================================
    def _with_input_scale(self, i_s):
        """
        Docstring placeholder
        """
        self.input_scale = i_s
        return self

    # ==============================================================================
    def format(self, reading):
        """
        Docstring placeholder
        """
        format_with_precision = f"{{0:.{self.precision:d}f}} {{1}}"
        _logger.debug(f"resulting format with precision applied: {format_with_precision}")
        result = format_with_precision.format(self.convert(reading), self.suffix())
        _logger.debug(f"formatted result: {result}")
        return result

    # ==============================================================================
    def format_native(self, reading):
        """
        Docstring placeholder
        """
        return self.input_scale.format(reading)

    # ==============================================================================
    def convert(self, reading):
        """
        Docstring placeholder
        """
        return self._from_canonical(self.input_scale._to_canonical(reading))  # noqa

    # ==============================================================================
    def suffix_native(self):
        """
        Docstring placeholder
        """
        return self.input_scale.suffix()


# Note that these imports must remain here.
from .temperature_scale import *  # noqa
from .length_scale import *  # noqa
from .power_scale import *  # noqa


# ==============================================================================
class AffineScaledMeasurement(ScaledMeasurement):
    """
    Docstring placeholder
    """

    # ==============================================================================
    def __init__(self, offset=0.0, multiplier=1.0, format_string="{0:.1f}"):
        """
        Docstring placeholder
        """
        super().__init__()
        self.offset = offset
        self.multiplier = multiplier
        self.format_string = format_string

    # ==============================================================================
    def format(self, reading):
        """
        Docstring placeholder
        """
        return self.format_string.format(self.convert(reading))

    # ==============================================================================
    def convert(self, reading):
        """
        Docstring placeholder
        """
        return (float(reading) * float(self.multiplier)) + float(self.offset)


# ==============================================================================
class ArbitraryFormulaScaledMeasurement(ScaledMeasurement):
    """
    Docstring placeholder
    """

    # ==============================================================================
    def __init__(self, formula="x", format_string="{0:.1f}"):
        super().__init__()
        self.formula = formula
        self.format_string = format_string

    # ==============================================================================
    def format(self, reading):
        """
        Docstring placeholder
        """
        return self.format_string.format(self.convert(reading))

    # ==============================================================================
    def convert(self, reading):
        """
        Docstring placeholder
        """
        return simple_eval(self.formula, names={"x": float(reading)})
