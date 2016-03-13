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

class Plugin(indigo.PluginBase):

	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
		self.debug = DEBUG

		self.active_converters = []

		logHandler = IndigoLoggingHandler(self)

		self.log = logging.getLogger('indigo.temp-converter.plugin')
		self.log.addHandler(logHandler)

		if DEBUG:
			self.log.setLevel(logging.DEBUG)
		else:
			self.log.setLevel(logging.WARNING)

	def __del__(self):
		indigo.PluginBase.__del__(self)

	def _get_eligible_sensors(self):
		return [("%d.%s" % (d.id, sk), "%s (%s): %s" % (d.name, sk, "{0:.1f}".format(sv)), d.address, d.name, sk)
			for d in indigo.devices
			for (sk, sv) in d.states.items()
				if (sk == "temperature") or (sk == "sensorValue")
		]

	def get_convertible_sensors(self, filter="", valuesDict=None, typeId="", targetId=0):
		return [
			(address, name)
			for (address, name, dev_address, dev_name, state_name) in self._get_eligible_sensors()
		]

	def validatePrefsConfigUi(self, valuesDict):
		indigo.server.log("validatePrefsConfigGui")
		# scaleInfo = valuesDict[TEMPERATURE_SCALE_PLUGIN_PREF]
		# self._setTemperatureScale(scaleInfo[0])
		return True

	def startup(self):
		self.debugLog(u"startup called")

	def shutdown(self):
		self.debugLog(u"shutdown called")

	def get_orphan_convertible_sensors(self, filter="", valuesDict=None, typeId="", targetId=0):
		return self._filter_for_orphans(
					self.get_convertible_sensors(filter, valuesDict, typeId, targetId),
					self.active_converters
				)

	def _filter_for_orphans(self, tuples, actives):
		return [
			t for t in tuples
				if not [ a for a in actives if a.address == t[0] ]
		]


	def deviceStartComm(self, dev):
#		self.debugLog('deviceStartComm: %s' % dev)
		if dev.model == 'Ecobee Remote Sensor':
			self.debugLog("deviceStartComm: creating EcobeeRemoteSensor")
			newDevice = EcobeeRemoteSensor(dev.pluginProps["address"], dev, self.ecobee)
			self.active_remote_sensors.append(newDevice)

			# set icon to 'temperature sensor'
			dev.updateStateImageOnServer(indigo.kStateImageSel.TemperatureSensor)

			indigo.server.log("added remote sensor %s" % dev.pluginProps["address"])

		# TODO: try to set initial name for new devices, as other plugins do.
		# However, this doesn't work yet. Sad clown.
		self.debugLog('device name: %s  ecobee name: %s' % (dev.name, newDevice.name))
		if dev.name == 'new device' and newDevice.name:
			dev.name = newDevice.name
			dev.replaceOnServer()
			self.debugLog('device name set to %s' % dev.name)

#		indigo.server.log(u"device added; plugin props: %s" % dev.pluginProps)
#		indigo.server.log(u"device added: %s" % dev)

	def deviceStopComm(self, dev):
		if dev.model == 'Ecobee Remote Sensor':
			self.active_converters = [
				rs for rs in self.active_converters
					if rs.address != dev.pluginProps["address"]
			]

	def updateAllDevices(self):
		for ers in self.active_converters:
			ers.updateServer()

	def runConcurrentThread(self):
		try:

			while True:
				self.updateAllDevices()
				self.sleep(15)

		except self.StopThread:
			pass	# Optionally catch the StopThread exception and do any needed cleanup.
