#!/usr/bin/env python
from gi.repository import Gtk, GObject

from gpu import NvidiaDevice

class MainWindow(object):
	def __init__(self):
		self.ui = Gtk.Builder()
		self.ui.add_from_file('src/ui/main.ui')
		self.window = self.ui.get_object('window')
		self.ui.connect_signals(self)
		self.gpu = NvidiaDevice()
		self.window.set_title(self.window.get_title() + " " + self.gpu.get_name())
		GObject.timeout_add(500, self.update_ui)
		
	def update_ui(self):
		temp = self.gpu.get_temperature()
		core, core_max = self.gpu.get_core_clock()
		mem, mem_max = self.gpu.get_memory_clock()
		core_util = self.gpu.get_core_utilization()
		mem_util = self.gpu.get_memory_utilization()
		pstate = self.gpu.get_performance_state()
		
		self.ui.get_object('progressbarTemperature').set_fraction(temp/90.0)
		self.ui.get_object('progressbarTemperature').set_text(str(temp) + 'C')
		self.ui.get_object('labelCoreValue').set_text(str(core) + 'MHz')
		self.ui.get_object('progressbarGpuCoreClock').set_fraction(core/(core_max*1.0))
		self.ui.get_object('labelMemoryValue').set_text(str(mem) + 'MHz')
		self.ui.get_object('progressbarGpuMemClock').set_fraction(mem/(mem_max*1.0))
		self.ui.get_object('progressbarCoreUtilization').set_fraction(core_util/100.0)
		self.ui.get_object('progressbarCoreUtilization').set_text(str(core_util) + '%')
		self.ui.get_object('progressbarMemUtilization').set_fraction(mem_util/100.0)
		self.ui.get_object('progressbarMemUtilization').set_text(str(mem_util) + '%')
		self.ui.get_object('labelPStateValue').set_text('P' + str(pstate))

		return True
	
	def on_window_destroy(self, window, user_data=None):
		Gtk.main_quit()
	
if __name__ == '__main__':
	main_window = MainWindow()
	main_window.window.show_all()
	Gtk.main()