"""
Docstring placeholder
"""
import logging
import indigo  # noqa
from pyrescaler.pyrescaler import (get_converter,
                                   AffineScaledMeasurement,
                                   ArbitraryFormulaScaledMeasurement
                                   )


class SensorAdapter:
    """
    Docstring placeholder
    """

    def __init__(self, dev):
        """
        Docstring placeholder
        """
        self.log = logging.getLogger('indigo.temp-converter.plugin')

        self.dev = dev
        self.address = dev.pluginProps["address"]

        native_device_info = self.address.split(".", 1)
        self.native_device_id = int(native_device_info[0])
        self.native_device_state_name = native_device_info[1]
        self.native_device_name = indigo.devices[self.native_device_id].name

        # default
        self.precision = 1

        if "customConvertedSensor" == self.dev.deviceTypeId:
            self.delegate = _AffineTransformDelegate(dev, self)
        elif "tempConvertedSensor" == self.dev.deviceTypeId:
            self.delegate = _PredefinedDelegate(dev, self)
        else:
            self.delegate = _FormulaDelegate(dev, self)

        self.log.debug(f"new adapter: {self.name()}")

        self.go()

    def name(self):
        """
        Docstring placeholder
        """
        return self.delegate.name()

    def go(self):
        """
        Docstring placeholder
        """
        native_value = indigo.devices[self.native_device_id].states[self.native_device_state_name]

        converted_txt = self.desired_scale.format(native_value)
        converted_value = self.desired_scale.convert(native_value)

        self.dev.updateStateOnServer(
            key="sensorValue",
            value=converted_value,
            decimalPlaces=self.precision,
            uiValue=converted_txt.lstrip()
        )
        self.log.debug(f"{self.name()}: {converted_txt}")


class _PredefinedDelegate:
    """
    Docstring placeholder
    """

    def __init__(self, dev, adapter):
        """
        Docstring placeholder
        """
        self.adapter = adapter
        self.scale_type = dev.pluginProps["scaleType"]

        if "precision" in dev.pluginProps:
            self.adapter.precision = int(dev.pluginProps["precision"])

        if 'temperature' == self.scale_type:
            # set icon to 'temperature sensor'
            dev.updateStateImageOnServer(indigo.kStateImageSel.TemperatureSensor)

        self.adapter.desired_scale = (
            get_converter(self.scale_type,
                          dev.pluginProps["nativeScale"],
                          dev.pluginProps["desiredScale"],
                          precision=self.adapter.precision
                          )
        )

    def name(self):
        """
        Docstring placeholder
        """
        return (
            f"{self.adapter.native_device_name}['{self.adapter.native_device_state_name}'] "
            f"{self.adapter.desired_scale.suffix_native()} -> {self.adapter.desired_scale.suffix()}"
        )


class _AffineTransformDelegate:
    """
    Docstring placeholder
    """

    def __init__(self, dev, adapter):
        """
        Docstring placeholder
        """
        self.adapter = adapter
        self.format = dev.pluginProps["format"]
        adapter.desired_scale = (
            AffineScaledMeasurement(multiplier=dev.pluginProps["multiplier"],
                                    offset=dev.pluginProps["offset"],
                                    format_string=self.format
                                    )
        )

    def name(self):
        """
        Docstring placeholder
        """
        return (
            f"{self.adapter.native_device_name}['{self.adapter.native_device_state_name}'] "
            f"{self.format}"
        )


class _FormulaDelegate:
    """
    Docstring placeholder
    """

    def __init__(self, dev, adapter):
        """
        Docstring placeholder
        """
        self.adapter = adapter
        self.format = dev.pluginProps["format"]
        adapter.desired_scale = (
            ArbitraryFormulaScaledMeasurement(
                formula=dev.pluginProps["formula"], format_string=self.format
            )
        )

    def name(self):
        """
        Docstring placeholder
        """
        return (
            f"{self.adapter.native_device_name}['{self.adapter.native_device_state_name}'] "
            f"{self.format}"
        )
