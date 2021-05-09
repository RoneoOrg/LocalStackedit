#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Handles hotkeys (shortcuts)"""

# Dependencies
try:
	from pynput import keyboard
except ModuleNotFoundError as e:
	print(f"ERROR - Missing dependency: {e}.\nRun:\npip install -r requirements.txt")
	exit(1)
# Modules
from src import WindowManager
from src import Stackedit
from src import Browser


def on_save_shortcut(
						windowName: bytes,
						editorField: object,
						docFile: str,
						rootWM: object,
						dispWM: object,
						browser: object
					) -> None:
	if WindowManager.get_focused_window(rootWM, dispWM) == windowName:
		print(f"INFO - Saving the content of editorField to {docFile}")
		with open(docFile, "w") as f:
			f.write(editorField.text)
		Stackedit.make_notif(f"Document saved to {docFile}", browser)
	else:
		print(f"DEBUG - Save shortcut pressed, but the window {WindowManager.get_focused_window(rootWM, dispWM)} is not the proper one {windowName}")


def on_quit_shortcut(
						scriptPath: str,
						windowName: bytes,
						rootWM: object,
						dispWM: object,
						browser: object
					) -> None:
	if WindowManager.get_focused_window(rootWM, dispWM) == windowName:
		print(f"Browser at quit shortcut: {browser}")
		Browser.on_close(scriptPath, browser)
	else:
		print(f"DEBUG - Quit shortcut pressed, but the window {WindowManager.get_focused_window(rootWM, dispWM)} is not the proper one {windowName}")


def initialize(
				scriptPath: str,
				windowName: bytes,
				editorField: object,
				docFile: str,
				rootWM: object,
				dispWM: object,
				browser: object
			) -> object:

	h = keyboard.GlobalHotKeys({
		"<ctrl>+s": lambda: on_save_shortcut(windowName, editorField, docFile, rootWM, dispWM, browser),
		"<ctrl>+q": lambda: on_quit_shortcut(scriptPath, windowName, rootWM, dispWM, browser)
	})
	print(f"Browser at init: {browser}")
	h.start()
	print("INFO - Hotkey listener started.")
	return h
