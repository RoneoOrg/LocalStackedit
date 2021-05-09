#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import platform
import os, sys
import subprocess
from time import sleep
import pickle
from urllib3.exceptions import MaxRetryError

try:
	from pynput import keyboard
except ModuleNotFoundError as e:
	print(f"ERROR - Missing dependency: {e}.\nRun:\npip install -r requirements.txt")
	exit(1)

from src import Browser, Stackedit

# ==============================================================================
#                                     SETUP
# ==============================================================================

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

# ==============================================================================
#                                      MAIN
# ==============================================================================
if __name__ == "__main__":
	# Check user input
	if len(sys.argv) < 2:
		print("ERROR - The filename to open should be provided.")
		exit(1)

	# Set the download directory
	docFile = os.path.realpath((sys.argv[1]))

	try:
		browser = Browser.initialize(SCRIPT_PATH)
		editorField = Stackedit.initialize(sys.argv[1], browser)	
		import Xlib
		import Xlib.display

		disp = Xlib.display.Display()
		root = disp.screen().root

		NET_WM_NAME = disp.intern_atom('_NET_WM_NAME')
		NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')

		root.change_attributes(event_mask=Xlib.X.FocusChangeMask)

		def get_focused_window():
			try:
				window_id = root.get_full_property(NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
				window = disp.create_resource_object('window', window_id)
				window.change_attributes(event_mask=Xlib.X.PropertyChangeMask)
				window_name = window.get_full_property(NET_WM_NAME, 0).value
			except Xlib.error.XError: #simplify dealing with BadWindow
				window_name = None
			
			return window_name

		windowName = get_focused_window()


		# Setup keyboard listener
		def on_save_shortcut():
			global windowName
			global editorField, docFile
			if get_focused_window() == windowName:
				print(f"INFO - Saving the content of editorField to {docFile}")
				with open(docFile, "w") as f:
					f.write(editorField.text)
				Stackedit.make_notif(f"Document saved to {docFile}", browser)

		def on_quit_shortcut():
			global windowName
			global h
			global browser
			if get_focused_window() == windowName:
				Browser.on_close(SCRIPT_PATH, h, browser)
			else:
				print(f"INFO - Quit shortcut pressed, but the window {get_focused_window()} is not the proper one {windowName}")


		with keyboard.GlobalHotKeys({
			"<ctrl>+s": on_save_shortcut,
			"<ctrl>+q": on_quit_shortcut
		}) as h:
			h.join()


	except KeyboardInterrupt:
		Browser.on_close(SCRIPT_PATH, h, browser)	
