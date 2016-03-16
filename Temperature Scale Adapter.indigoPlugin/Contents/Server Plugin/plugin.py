#! /usr/bin/env python
# -*- coding: utf-8 -*-

import indigo
import indigo_logging_handler
from sensor_adapter import SensorAdapter
import logging
import re

DEBUGGING_ENABLED_MAP = {
	"y" : True,
	"n" : False
}

def _is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False


class Plugin(indigo.PluginBase):

	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)

		self.active_adapters = []
		self.adapters_for_device = {}
		logHandler = indigo_logging_handler.IndigoLoggingHandler(self)

		self.log = logging.getLogger('indigo.temp-converter.plugin')
		self.log.addHandler(logHandler)

		# subscribe to changes from all indigo devices, so we can update
		#   our 'converted' temperature any time the native Temperature
		#   changes.
		# would be nice to only subscribe to changes from individual objects,
		#   but that's not implemented yet.
		indigo.devices.subscribeToChanges()

	def __del__(self):
		indigo.PluginBase.__del__(self)

	def get_eligible_sensors(self):
		return [("%d.%s" % (d.id, sk), "%s (%s): %s" % (d.name, sk, "{0:.1f}".format(float(sv))), d.address, d.name, sk)
			for d in indigo.devices
				# don't include instances of this plugin/device in the list
				if (not d.pluginId) or (d.pluginId != self.pluginId)
			for (sk, sv) in d.states.items()
				# only return devices that have a matching state name
				if re.search("temperature|sensorValue", sk, re.IGNORECASE) and _is_number(sv)
		]

	def validatePrefsConfigUi(self, valuesDict):
		self.log.debug("validatePrefsConfigGui")
		self.update_logging(bool(valuesDict['debuggingEnabled'] and "y" == valuesDict['debuggingEnabled']))
		return True

	def update_logging(self, is_debug):
		if is_debug:
			self.debug = True
			self.log.setLevel(logging.DEBUG)
			logging.getLogger("indigo.temp-converter.plugin").setLevel(logging.DEBUG)
			self.log.debug("debug logging enabled")
		else:
			self.log.debug("debug logging disabled")
			self.debug=False
			self.log.setLevel(logging.INFO)
			logging.getLogger("indigo.temp-converter.plugin").setLevel(logging.INFO)

	def startup(self):
		self.log.debug(u"startup called")
		if "debuggingEnabled" not in self.pluginPrefs:
			self.pluginPrefs["debuggingEnabled"] = "n"

		self.update_logging(DEBUGGING_ENABLED_MAP[self.pluginPrefs["debuggingEnabled"]])


	def shutdown(self):
		self.log.debug(u"shutdown called")

	def get_orphan_eligible_sensors(self, filter="", valuesDict=None, typeId="", targetId=0):
		return [
			(t[0], t[1])
			for t in self.get_eligible_sensors()
			if not [ a for a in self.active_adapters if a.address == t[0] ]
		]

	def deviceStartComm(self, dev):
		self.log.debug("deviceStartComm: %s" % dev.pluginProps["address"])
		newDevice = SensorAdapter(dev)
		self.active_adapters.append(newDevice)

		if not newDevice.native_device_id in self.adapters_for_device:
			self.adapters_for_device[newDevice.native_device_id] = []
		self.adapters_for_device[newDevice.native_device_id].append(newDevice)

		# set icon to 'temperature sensor'
		dev.updateStateImageOnServer(indigo.kStateImageSel.TemperatureSensor)

		self.log.debug("added temperature adapter: %s" % newDevice.name())

	def deviceStopComm(self, dev):
		self.active_adapters = [
			rs for rs in self.active_adapters
				if rs.address != dev.pluginProps["address"]
		]
		# TODO: self.adapters_for_device

	def deviceUpdated(self, origDev, newDev):
		indigo.PluginBase.deviceUpdated(self, origDev, newDev)
		if newDev.id in self.adapters_for_device:
			for cs in self.adapters_for_device[newDev.id]:
				cs.go()

	def runConcurrentThread(self):
		try:

			while True:
				self.sleep(3600)

		except self.StopThread:
			pass	# Optionally catch the StopThread exception and do any needed cleanup.
