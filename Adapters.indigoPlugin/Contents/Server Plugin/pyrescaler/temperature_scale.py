#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Docstring placeholder
"""

from .pyrescaler import *

SCALE_TYPE = "temperature"


# Internal canonical representation is Kelvin
class TemperatureScale(PredefinedScaledMeasurement):
    """
    Docstring placeholder
    """

    def __init__(self, input_scale=None, precision=1):
        """
        Docstring placeholder
        """
        PredefinedScaledMeasurement.__init__(self, input_scale, precision=precision)


class Fahrenheit(TemperatureScale):
    """
    Docstring placeholder
    """

    def __init__(self, input_scale=None, precision=1):
        """
        Docstring placeholder
        """
        TemperatureScale.__init__(self, input_scale, precision=precision)

    # F -> K
    @staticmethod
    def _to_canonical(f_temp):
        """
        Docstring placeholder
        """
        return (459.67 + float(f_temp)) * 5 / 9

    # K -> F
    @staticmethod
    def _from_canonical(k_temp):
        """
        Docstring placeholder
        """
        return (1.8 * float(k_temp)) - 459.67

    def suffix(self):
        """
        Docstring placeholder
        """
        return "°F"


register_scale(SCALE_TYPE, "Fahrenheit", "F", Fahrenheit)


class Celsius(TemperatureScale):
    """
    Docstring placeholder
    """

    def __init__(self, input_scale=None, precision=1):
        """
        Docstring placeholder
        """
        TemperatureScale.__init__(self, input_scale, precision=precision)

    # C -> K
    @staticmethod
    def _to_canonical(c_temp):
        """
        Docstring placeholder
        """
        return float(c_temp) + 273.15

    # K -> C
    @staticmethod
    def _from_canonical(k_temp):
        """
        Docstring placeholder
        """
        return float(k_temp) - 273.15

    def suffix(self):
        """
        Docstring placeholder
        """
        return "°C"


register_scale(SCALE_TYPE, "Celsius", "C", Celsius)


class Kelvin(TemperatureScale):
    """
    Docstring placeholder
    """

    def __init__(self, input_scale=None, precision=1):
        """
        Docstring placeholder
        """
        TemperatureScale.__init__(self, input_scale, precision=precision)

    @staticmethod
    def _to_canonical(k_temp):
        """
        Docstring placeholder
        """
        # Kelvin is the canonical representation, so nothing to do
        return float(k_temp)

    @staticmethod
    def _from_canonical(k_temp):
        """
        Docstring placeholder
        """
        # Kelvin is the canonical representation, so nothing to do
        return float(k_temp)

    def suffix(self):
        """
        Docstring placeholder
        """
        return "K"


register_scale(SCALE_TYPE, "Kelvin", "K", Kelvin)


class Rankine(TemperatureScale):
    """
    Docstring placeholder
    """

    def __init__(self, input_scale=None, precision=1):
        """
        Docstring placeholder
        """
        TemperatureScale.__init__(self, input_scale, precision=precision)

    # R -> K
    @staticmethod
    def _to_canonical(r_temp):
        """
        Docstring placeholder
        """
        return float(r_temp) * 5 / 9

    # K -> R
    @staticmethod
    def _from_canonical(k_temp):
        """
        Docstring placeholder
        """
        return 1.8 * float(k_temp)

    def suffix(self):
        """
        Docstring placeholder
        """
        return "°Ra"


register_scale(SCALE_TYPE, "Rankine", "R", Rankine)
