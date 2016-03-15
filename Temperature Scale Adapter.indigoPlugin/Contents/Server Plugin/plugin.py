#! /usr/bin/env python
# -*- coding: utf-8 -*-

import indigo
import indigo_logging_handler
from sensor_adapter import SensorAdapter
import logging

DEBUG=True

class Plugin(indigo.PluginBase):

	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
		self.debug = DEBUG

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
		self.log.debug("validatePrefsConfigGui")
		return True

	def startup(self):
		self.log.debug(u"startup called")

	def shutdown(self):
		self.log.debug(u"shutdown called")

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

		self.log.debug("added temperature adapter: %s" % newDevice.name())

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
