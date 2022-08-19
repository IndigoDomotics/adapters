#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Docstring placeholder
"""

from .pyrescaler import *


SCALE_TYPE = "power"


# Internal canonical representation is watts
class PowerScale(PredefinedScaledMeasurement):
    """
    Docstring placeholder
    """

    def __init__(self, input_scale=None, precision=1):
        """
        Docstring placeholder
        """
        PredefinedScaledMeasurement.__init__(self, input_scale, precision=precision)
        print(f"{self.suffix()}: {self.__class__}")


class Watts(PowerScale):
    """
    Docstring placeholder
    """

    def __init__(self, input_scale=None, precision=1):
        """
        Docstring placeholder
        """
        PowerScale.__init__(self, input_scale, precision=precision)

    # nothing to do; canonical representation
    @staticmethod
    def _to_canonical(val):
        """
        Docstring placeholder
        """
        return float(val)

    # nothing to do; canonical representation
    @staticmethod
    def _from_canonical(val):
        """
        Docstring placeholder
        """
        return float(val)

    @staticmethod
    def suffix():
        """
        Docstring placeholder
        """
        return "W"


register_scale(SCALE_TYPE, "Watts", "W", Watts)


class Kilowatts(PowerScale):
    """
    Docstring placeholder
    """

    def __init__(self, input_scale=None, precision=1):
        """
        Docstring placeholder
        """
        PowerScale.__init__(self, input_scale, precision=precision)

    # kW -> W
    @staticmethod
    def _to_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) * 1000

    # W -> kW
    @staticmethod
    def _from_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) / 1000

    @staticmethod
    def suffix():
        """
        Docstring placeholder
        """
        return "kW"


register_scale(SCALE_TYPE, "Kilowatts", "kW", Kilowatts)


class Horsepower(PowerScale):
    """
    Docstring placeholder
    """

    def __init__(self, input_scale=None, precision=1):
        """
        Docstring placeholder
        """
        PowerScale.__init__(self, input_scale, precision=precision)

    # hp -> W
    @staticmethod
    def _to_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) * 745.69987158227

    # W -> hp
    @staticmethod
    def _from_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) / 745.69987158227

    @staticmethod
    def suffix():
        """
        Docstring placeholder
        """
        return "hp"


register_scale(SCALE_TYPE, "Horsepower", "hp", Horsepower)
