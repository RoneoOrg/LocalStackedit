#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Handles manipulation of the OS' windows"""

# dependencies
import Xlib
import Xlib.display


def initialize() -> tuple:
	"""Grab the root windows manager and the active display."""

	disp = Xlib.display.Display()
	root = disp.screen().root

	root.change_attributes(event_mask=Xlib.X.FocusChangeMask)

	return root, disp
	

def get_focused_window(root: object, disp: object) -> str:
	"""Get the window the user has in focus."""

	try:
		NET_WM_NAME = disp.intern_atom('_NET_WM_NAME')
		NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
		window_id = root.get_full_property(NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
		window = disp.create_resource_object('window', window_id)
		window.change_attributes(event_mask=Xlib.X.PropertyChangeMask)
		window_name = window.get_full_property(NET_WM_NAME, 0).value
	except Xlib.error.XError: #simplify dealing with BadWindow
		window_name = None

	return window_name

