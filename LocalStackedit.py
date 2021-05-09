#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Allows to use Stackedit.io with local file, with quit on <ctrl>+'q' and save to the local file on <ctrl>+s"""

# std lib
import os
import sys
from time import sleep

# Modules
from src import Browser, Stackedit, WindowManager, HotKeys

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

# ==============================================================================
#                                      MAIN
# ==============================================================================
if __name__ == "__main__":
	# Check user input
	if len(sys.argv) < 2:
		print("ERROR - The filename to open should be provided.")
		exit(1)

	# Get the opened document absolute path
	docFile = os.path.realpath((sys.argv[1]))

	try:
		# Start Selenium
		browser = Browser.initialize(SCRIPT_PATH)
		# Start stackedit
		editorField = Stackedit.initialize(sys.argv[1], browser)	
		# Start the windows manager
		rootWM, dispWM = WindowManager.initialize()

		# Set the windows name for the WindowManager to know
		# if the focus window is stackedit's and prevent
		# shortcut actions if it's not this window
		# TODO Less hardcoded
		windowName = bytes(f"{browser.title} - Brave", "utf-8")

		# Start the keyboard listener
		h = HotKeys.initialize(
				SCRIPT_PATH,
				windowName,
				editorField,
				docFile,
				rootWM,
				dispWM,
				browser
			)

		# Block execution until the browser is closed
		while Browser.is_alive(browser):
			sleep(0.5)

	except KeyboardInterrupt:
		Browser.on_close(SCRIPT_PATH, browser)	
