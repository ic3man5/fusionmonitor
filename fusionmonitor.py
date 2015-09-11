#!/usr/bin/env python

from src import MainWindow
from gi.repository import Gtk

if __name__ == '__main__':
	main_window = MainWindow()
	main_window.window.show_all()
	Gtk.main()
