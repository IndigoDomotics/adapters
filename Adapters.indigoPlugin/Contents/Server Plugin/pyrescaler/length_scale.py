#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Docstring placeholder
"""

from .pyrescaler import *

SCALE_TYPE = "length"


# Internal canonical representation is meters
class LengthScale(PredefinedScaledMeasurement):
    """
    Docstring placeholder
    """

    def __init__(self, input_scale=None, precision=1):
        """
        Docstring placeholder
        """
        PredefinedScaledMeasurement.__init__(self, input_scale, precision=precision)
        print(f"{self.suffix()}: {self.__class__}")


class Inches(LengthScale):
    """
    Docstring placeholder
    """

    def __init__(self, input_scale=None, precision=1):
        LengthScale.__init__(self, input_scale, precision=precision)

    # in -> m
    @staticmethod
    def _to_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) * 0.0254

    # m -> in
    @staticmethod
    def _from_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) / 0.0254

    def suffix(self):
        """
        Docstring placeholder
        """
        return "in"


register_scale(SCALE_TYPE, "Inches", "in", Inches)


class Feet(LengthScale):
    """
    Docstring placeholder
    """

    def __init__(self, input_scale=None, precision=1):
        """
        Docstring placeholder
        """
        LengthScale.__init__(self, input_scale, precision=precision)

    # ft -> m
    @staticmethod
    def _to_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) * 0.3048

    # m -> ft
    @staticmethod
    def _from_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) * 3.2808

    def suffix(self):
        """
        Docstring placeholder
        """
        return "ft"


register_scale(SCALE_TYPE, "Feet", "ft", Feet)


class Yards(LengthScale):
    """
    Docstring placeholder
    """

    def __init__(self, input_scale=None, precision=1):
        """
        Docstring placeholder
        """
        LengthScale.__init__(self, input_scale, precision=precision)

    # yd -> m
    @staticmethod
    def _to_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) / 1.0936

    # m -> yd
    @staticmethod
    def _from_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) * 1.0936

    def suffix(self):
        """
        Docstring placeholder
        """
        return "yd"


register_scale(SCALE_TYPE, "Yards", "yd", Yards)

# class Furlongs(LengthScale):
#     def __init__(self, input_scale=None):
#         LengthScale.__init__(self, input_scale)


class Miles(LengthScale):
    """
    Docstring placeholder
    """

    def __init__(self, input_scale=None, precision=1):
        """
        Docstring placeholder
        """
        LengthScale.__init__(self, input_scale, precision=precision)

    # mi -> m
    @staticmethod
    def _to_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) * 1609.34

    # m -> mi
    @staticmethod
    def _from_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) / 1609.34

    def suffix(self):
        """
        Docstring placeholder
        """
        return "mi"


register_scale(SCALE_TYPE, "Miles", "mi", Miles)


class Centimeters(LengthScale):
    """
    Docstring placeholder
    """

    def __init__(self, input_scale=None, precision=1):
        """
        Docstring placeholder
        """
        LengthScale.__init__(self, input_scale, precision=precision)

    # cm -> m
    @staticmethod
    def _to_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) / 100

    # m -> cm
    @staticmethod
    def _from_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) * 100

    def suffix(self):
        """
        Docstring placeholder
        """
        return "cm"


register_scale(SCALE_TYPE, "Centimeters", "cm", Centimeters)


class Meters(LengthScale):
    """
    Docstring placeholder
    """

    def __init__(self, input_scale=None, precision=1):
        """
        Docstring placeholder
        """
        LengthScale.__init__(self, input_scale, precision=precision)

    # no change
    @staticmethod
    def _to_canonical(val):
        """
        Docstring placeholder
        """
        return float(val)

    # no change
    @staticmethod
    def _from_canonical(val):
        """
        Docstring placeholder
        """
        return float(val)

    def suffix(self):
        """
        Docstring placeholder
        """
        return "m"


register_scale(SCALE_TYPE, "Meters", "m", Meters)


class Kilometers(LengthScale):
    """
    Docstring placeholder
    """

    def __init__(self, input_scale=None, precision=1):
        """
        Docstring placeholder
        """
        LengthScale.__init__(self, input_scale, precision=precision)

    # km -> m
    @staticmethod
    def _to_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) * 1000

    # m -> km
    @staticmethod
    def _from_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) / 1000

    def suffix(self):
        """
        Docstring placeholder
        """
        return "km"


register_scale(SCALE_TYPE, "Kilometers", "km", Kilometers)


class NauticalMiles(LengthScale):
    """
    Docstring placeholder
    """

    def __init__(self, input_scale=None, precision=1):
        """
        Docstring placeholder
        """
        LengthScale.__init__(self, input_scale, precision=precision)

    # nmi -> m
    @staticmethod
    def _to_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) * 1852

    # m -> nmi
    @staticmethod
    def _from_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) / 1852

    def suffix(self):
        """
        Docstring placeholder
        """
        return "nmi"


register_scale(SCALE_TYPE, "Nautical Miles", "nmi", NauticalMiles)


class Fathoms(LengthScale):
    """
    Docstring placeholder
    """

    def __init__(self, input_scale=None, precision=1):
        """
        Docstring placeholder
        """
        LengthScale.__init__(self, input_scale, precision=precision)

    # fm -> m
    @staticmethod
    def _to_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) * 1.8288

    # m -> fm
    @staticmethod
    def _from_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) / 1.8288

    def suffix(self):
        """
        Docstring placeholder
        """
        return "fm"


register_scale(SCALE_TYPE, "Fathoms", "fm", Fathoms)


class Cubits(LengthScale):
    """
    Docstring placeholder
    """

    def __init__(self, input_scale=None, precision=1):
        """
        Docstring placeholder
        """
        LengthScale.__init__(self, input_scale, precision=precision)

    # cbt -> m
    @staticmethod
    def _to_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) / 2.18723

    # m -> cbt
    @staticmethod
    def _from_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) * 2.18723

    def suffix(self):
        """
        Docstring placeholder
        """
        return "cbt"


register_scale(SCALE_TYPE, "Cubits", "cbt", Cubits)


class Hands(LengthScale):
    """
    Docstring placeholder
    """

    def __init__(self, input_scale=None, precision=1):
        """
        Docstring placeholder
        """
        LengthScale.__init__(self, input_scale, precision=precision)

    # h -> m
    @staticmethod
    def _to_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) / 9.84252

    # m -> h
    @staticmethod
    def _from_canonical(val):
        """
        Docstring placeholder
        """
        return float(val) * 9.84252

    def suffix(self):
        """
        Docstring placeholder
        """
        return "h"


register_scale(SCALE_TYPE, "Hands", "h", Hands)


#
# class Parsecs(LengthScale):
#     def __init__(self, input_scale=None):
#         LengthScale.__init__(self, input_scale)
#
# class LightYears(LengthScale):
#     def __init__(self, input_scale=None):
#         LengthScale.__init__(self, input_scale)
#
# class Angstroms(LengthScale):
#     def __init__(self, input_scale=None):
#         LengthScale.__init__(self, input_scale)
