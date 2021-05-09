#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# std lib
import os
import sys

try:
	from pynput import keyboard
except ModuleNotFoundError as e:
	print(f"ERROR - Missing dependency: {e}.\nRun:\npip install -r requirements.txt")
	exit(1)
# Modules
from src import Browser, Stackedit, WindowManager

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

		rootWM, dispWM = WindowManager.initialize()

		# Set the windows name for the WindowManager to know
		# if the focus window is stackedit's and prevent
		# shortcut actions if it's not this window
		# TODO Less hardcoded
		windowName = bytes(f"{browser.title} - Brave", "utf-8")

		# Setup keyboard listener
		def on_save_shortcut():
			global windowName
			global editorField, docFile
			if WindowManager.get_focused_window(rootWM, dispWM) == windowName:
				print(f"INFO - Saving the content of editorField to {docFile}")
				with open(docFile, "w") as f:
					f.write(editorField.text)
				Stackedit.make_notif(f"Document saved to {docFile}", browser)

		def on_quit_shortcut():
			global windowName
			global h
			global browser
			if WindowManager.get_focused_window(rootWM, dispWM) == windowName:
				Browser.on_close(SCRIPT_PATH, h, browser)
			else:
				print(f"INFO - Quit shortcut pressed, but the window {WindowManager.get_focused_window(rootWM, dispWM)} is not the proper one {windowName}")


		with keyboard.GlobalHotKeys({
			"<ctrl>+s": on_save_shortcut,
			"<ctrl>+q": on_quit_shortcut
		}) as h:
			h.join()


	except KeyboardInterrupt:
		Browser.on_close(SCRIPT_PATH, h, browser)	
