#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import indigo
import temperature_scale
import logging


DEBUG=True

TEMP_FORMATTERS = {
	'F': temperature_scale.Fahrenheit(),
	'C': temperature_scale.Celsius(),
	'K': temperature_scale.Kelvin(),
	'R': temperature_scale.Rankine()
}

class IndigoLoggingHandler(logging.Handler):

	def __init__(self, p):
		 logging.Handler.__init__(self)
		 self.plugin = p

	def emit(self, record):
		if record.levelno < 20:
			self.plugin.debugLog(record.getMessage())
		elif record.levelno < 40:
			indigo.server.log(record.getMessage())
		else:
			self.plugin.errorLog(record.getMessage())

class SensorAdapter:
	def __init__(self, dev):
		self.dev = dev
		self.address = dev.pluginProps["address"]

		self.native_scale = TEMP_FORMATTERS[dev.pluginProps["nativeScale"]]
		self.native_scale.set_input_scale(self.native_scale)
		self.desired_scale = TEMP_FORMATTERS[dev.pluginProps["desiredScale"]]
		self.desired_scale.set_input_scale(self.native_scale)

		native_device_info = self.address.split(".", 1)
		self.native_device_id = int(native_device_info[0])
		self.native_device_state_name = native_device_info[1]
		self.native_device_name = indigo.devices[self.native_device_id].name

		indigo.server.log("new adapter: %s" % self.name())

		self.go()

	def name(self):
		return "%s['%s'] %s -> %s" % (self.native_device_name, self.native_device_state_name, self.native_scale.suffix(), self.desired_scale.suffix())

	def go(self):
		native_value = indigo.devices[self.native_device_id].states[self.native_device_state_name]
		cv = self.desired_scale.report(self.dev, "temperature", native_value)
		indigo.server.log("%s: %s -> %s" % (self.name(), self.native_scale.format(native_value), cv))

class Plugin(indigo.PluginBase):

	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
		self.debug = DEBUG

		self.active_adapters = []
		self.adapters_for_device = {}

		logHandler = IndigoLoggingHandler(self)

		self.log = logging.getLogger('indigo.temp-converter.plugin')
		self.log.addHandler(logHandler)

		# subscribe to changes from all indigo devices, so we can update
		#   our 'converted' temperature any time the native Temperature
		#   changes.
		# would be nice to only subscribe to changes from individual objects,
		#   but that's not implemented yet.
		indigo.devices.subscribeToChanges()

		if DEBUG:
			self.log.setLevel(logging.DEBUG)
		else:
			self.log.setLevel(logging.WARNING)

	def __del__(self):
		indigo.PluginBase.__del__(self)

	def _get_eligible_sensors(self):
		return [("%d.%s" % (d.id, sk), "%s (%s): %s" % (d.name, sk, "{0:.1f}".format(sv)), d.address, d.name, sk)
			for d in indigo.devices
				# don't include instances of this plugin/device in the list
				if (not d.pluginId) or (d.pluginId != self.pluginId)
			for (sk, sv) in d.states.items()
				# only return devices that have a matching state name
				if (sk == "temperature") or (sk == "sensorValue")
		]

	def get_convertible_sensors(self, filter="", valuesDict=None, typeId="", targetId=0):
		return [
			(address, name)
			for (address, name, dev_address, dev_name, state_name) in self._get_eligible_sensors()
		]

	def validatePrefsConfigUi(self, valuesDict):
		indigo.server.log("validatePrefsConfigGui")
		return True

	def startup(self):
		self.debugLog(u"startup called")

	def shutdown(self):
		self.debugLog(u"shutdown called")

	def get_orphan_convertible_sensors(self, filter="", valuesDict=None, typeId="", targetId=0):
		return self._filter_for_orphans(
					self.get_convertible_sensors(filter, valuesDict, typeId, targetId),
					self.active_adapters
				)

	def _filter_for_orphans(self, tuples, actives):
		return [
			t for t in tuples
				if not [ a for a in actives if a.address == t[0] ]
		]


	def deviceStartComm(self, dev):
		newDevice = SensorAdapter(dev)
		self.active_adapters.append(newDevice)

		if not newDevice.native_device_id in self.adapters_for_device:
			self.adapters_for_device[newDevice.native_device_id] = []
		self.adapters_for_device[newDevice.native_device_id].append(newDevice)

		# set icon to 'temperature sensor'
		dev.updateStateImageOnServer(indigo.kStateImageSel.TemperatureSensor)

		indigo.server.log("added temperature adapter: %s" % newDevice.name())

	def deviceStopComm(self, dev):
		self.active_adapters = [
			rs for rs in self.active_adapters
				if rs.address != dev.pluginProps["address"]
		]

	def deviceUpdated(self, origDev, newDev):
		if newDev.id in self.adapters_for_device:
			for cs in self.adapters_for_device[newDev.id]:
				cs.go()

	def runConcurrentThread(self):
		try:

			while True:
				self.sleep(3600)

		except self.StopThread:
			pass	# Optionally catch the StopThread exception and do any needed cleanup.
