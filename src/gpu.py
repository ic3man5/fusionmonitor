#!/usr/bin/env python
from pynvml import *

class DeviceError(RuntimeError):
	pass

class Device(object):
	def __init__(self, id=0):
		self.id = 0

	def get_temperature(self):
		raise NotImplementedError

	def get_temperature_threshold(self):
		raise NotImplementedError

	def get_name(self):
		raise NotImplementedError
		
	def get_core_clock(self):
		raise NotImplementedError
		
	def get_memory_clock(self):
		raise NotImplementedError
	
	def get_core_utilization(self):
		raise NotImplementedError
		
	def get_memory_utilization(self):
		raise NotImplementedError
		
	def get_performance_state(self):
		raise NotImplementedError
		
	
class NvidiaDevice(Device):
	def __init__(self, id=0):
		Device.__init__(self, id)
		try:
			nvmlInit()
			self.device = nvmlDeviceGetHandleByIndex(self.id)
		except NVMLError as ex:
			raise DeviceError(ex)
	
	def __del__(self):
		try:
			nvmlShutdown()
		except NVMLError as ex:
			raise DeviceError(ex)

	def get_temperature(self):
		try:
			return nvmlDeviceGetTemperature(self.device, NVML_TEMPERATURE_GPU)
		except NVMLError as ex:
			print(ex)
			return 0

	def get_temperature_threshold(self):
		raise NotImplementedError

	def get_name(self):
		try:
			return nvmlDeviceGetName(self.device)
		except NVMLError as ex:
			print(ex)
			return "Unknown"
		
	def get_core_clock(self):
		try:
			current = nvmlDeviceGetClockInfo(self.device, NVML_CLOCK_GRAPHICS)
			maximum = nvmlDeviceGetMaxClockInfo(self.device, NVML_CLOCK_GRAPHICS)
			return current, maximum
		except NVMLError as ex:
			print(ex)
			return 0
		
	def get_memory_clock(self):
		try:
			current = nvmlDeviceGetClockInfo(self.device, NVML_CLOCK_MEM)
			maximum = nvmlDeviceGetMaxClockInfo(self.device, NVML_CLOCK_MEM)
			return current, maximum
		except NVMLError as ex:
			print(ex)
			return 0
	
	def get_core_utilization(self):
		try:
			return nvmlDeviceGetUtilizationRates(self.device).gpu
		except NVMLError as ex:
			print(ex)
			return 0
		
	def get_memory_utilization(self):
		try:
			return nvmlDeviceGetUtilizationRates(self.device).memory
		except NVMLError as ex:
			print(ex)
			return 0
		
	def get_performance_state(self):
		try:
			states = {
				NVML_PSTATE_0: 0,
				NVML_PSTATE_1: 1,
				NVML_PSTATE_2: 2,
				NVML_PSTATE_3: 3,
				NVML_PSTATE_4: 4,
				NVML_PSTATE_5: 5,
				NVML_PSTATE_6: 6,
				NVML_PSTATE_7: 7,
				NVML_PSTATE_8: 8,
				NVML_PSTATE_9: 9,
				NVML_PSTATE_10: 10,
				NVML_PSTATE_11: 11,
				NVML_PSTATE_12: 12,
				NVML_PSTATE_13: 13,
				NVML_PSTATE_14: 14,
				NVML_PSTATE_15: 15,
				NVML_PSTATE_UNKNOWN: -1,
			}
			state = nvmlDeviceGetPerformanceState(self.device)
			return states[state]
		except NVMLError as ex:
			print(ex)
			return -1