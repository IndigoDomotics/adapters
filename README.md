This plugin for the Indigo home automation sever allows you to add thin "adapters" on top of your devices to perform 
all kinds of mathematical or formatting transformations. 

For example, suppose you have devices that report temperatures in Fahrenheit and you prefer Celsius, or the other way 
around. This plugin can generate "device adapters" that "wrap" around your native device and convert the temperature to 
the scale you prefer.

It supports all kinds of things:
- temperature, distance, and power conversions
- arbitrary linear translations of numeric sensors (i.e. multiplier and an offset factor)
- custom expressions and formats to transmogrify (single) sensor outputs in almost any way you can think of

Recent changes to this plugin include:
- Direct support for Indigo 2022 and Python 3.
- New tool in device configuration dialogs to select custom icon in the Indigo UI.
- New tool to test formula expressions before saving them to the device.
- Removes Rankine and Kelvin from temperature conversions.
- Adds UI icons to devices lacking them; improves state value alignment in the Indigo UI.
