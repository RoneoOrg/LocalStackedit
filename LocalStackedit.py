#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import platform
import os, sys
import subprocess
from time import sleep
import pickle
from urllib3.exceptions import MaxRetryError

try:
	from selenium import webdriver
	from selenium.webdriver.common.keys import Keys
	from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException
	from selenium.webdriver.remote.command import Command
	from selenium.webdriver.common.keys import Keys
	from pynput import keyboard
except ModuleNotFoundError as e:
	print(f"ERROR - Missing dependency: {e}.\nRun:\npip install -r requirements.txt")
	exit(1)

# ==============================================================================
#                                     SETUP
# ==============================================================================

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
COOKIES_FILE = os.path.join(SCRIPT_PATH, "cookies.pkl")


if platform.system() == "Linux":
	WEBDRIVER = os.path.join(SCRIPT_PATH, "Webdrivers", "chromedriver_linux64")
	BRAVE_PATH = subprocess.check_output(["which", "brave-browser"]).decode("utf-8")
else:
	raise NotImplementedError(f"ERROR - This script is not compatible with {platform.system()}")
	exit(1)

# For some reason, trailing spaces are added to the output
BRAVE_PATH = BRAVE_PATH.strip()
print("INFO - Brave binary path: ", BRAVE_PATH)
OPTION = webdriver.ChromeOptions()
OPTION.binary_location = BRAVE_PATH

# Directory for brave's user data
DATA_DIR = os.path.join(SCRIPT_PATH, "BraveData")
OPTION.add_argument("--user-data-dir=" + DATA_DIR)
if not os.path.exists(DATA_DIR):
	IS_FIRST_LAUNCH = True
	os.mkdir(DATA_DIR) 
	print(f"INFO - User data directory created: {DATA_DIR}")
else:
	print(f"INFO - Reusing prexisting user data directory: {DATA_DIR}")

# No popup for saving downloads
OPTION.add_argument("profile.default_content_settings.popups=0")

# ==============================================================================
#                                BROWSER ACTIONS
# ==============================================================================
def new_tab() -> None:
	global browser
	browser.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 't')
	browser.find_element_by_tag_name("body").send_keys(Keys.COMMAND + 't')
	return


def wait_for_element(element2Find: str) -> None:
	global browser
	try:
		browser.find_element_by_class_name(element2Find)
	except NoSuchElementException:
		isFound = False
	else: isFound = True

	while not isFound:
		try:
			browser.find_element_by_class_name(element2Find)
		except NoSuchElementException:
			isFound = False
			sleep(.25)
		else:
			isFound = True

	print(f"INFO - Page loaded with element of class: {element2Find}.")
	return



def is_alive() -> bool:
	global browser
	try:
		browser.current_url
	except (MaxRetryError, WebDriverException):
		return False 
	else:
		return True


def on_close() -> None:
	global browser
	global h
	# backup cookies
	if is_alive():
		with open(COOKIES_FILE, "wb") as f:
			pickle.dump(browser.get_cookies(), f)
		print("INFO - Cookies saved.")
		browser.close()
	else:
		print("WARN - Browser is dead. Cookies unsaved.")
	h.stop()
	print("INFO - Bye.")


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
		# Starts the browser
		try:
			browser = webdriver.Chrome(
					executable_path = WEBDRIVER,
					options = OPTION
				)
		except Exception as e:
			print(e)
			print("ERROR - It's seem an instance of brave is already running. Only one instance allowed.")
			exit(1)
		# Loads cookies
		if os.path.exists(COOKIES_FILE):
			print("INFO - Loading cookies...")
			with open(COOKIES_FILE, "rb") as f:
				cookies = pickle.load(f)
			for c in cookies:
				browser.add_cookies(c)
			browser.refresh()
		else:
			print("INFO - No cookies file")

		# Open stakedit page
		browser.get("https://stackedit.io/app#")
		wait_for_element("editor")

		# Get stackedit document title
		titleField = browser.find_elements_by_tag_name("input")[0]
		# Set the title
		titleField.click()
		docTitle = os.path.basename(sys.argv[1]).split(".")[0]
		titleField.send_keys(docTitle)
		
		# Get stackedit editor area
		editorField = browser.find_elements_by_class_name("editor")[0]
		editorField = editorField.find_element_by_tag_name("pre")
		# clear the editor
		browser.execute_script("arguments[0].innerHTML=''", editorField)

		# set the content of the editor
		with open(sys.argv[1], "r") as f:
			browser.execute_script("arguments[0].innerHTML=arguments[1]", editorField, f.read())

		# Set the windows title to be grabbed by Xlib
		browser.execute_script("document.title=arguments[0]", f"Stackedit - {docTitle}")

		from time import sleep
		# Wait for the document title to be set
		# It takes time for the windows title to be set
		# according to the document title
		sleep(.5)

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

		def save_content(field, file_):
			with open(file_, "w") as f:
				f.write(field.text)

		# Setup keyboard listener
		def on_save_shortcut():
			global windowName
			global editorField, docFile
			if get_focused_window() == windowName:
				print(f"INFO - Saving the content of editorField to {docFile}")
				with open(docFile, "w") as f:
					f.write(editorField.text)

				notifHtml = f"""
<div class="notification__item flex flex--row flex--align-center">
        <div class="notification__icon flex flex--column flex--center"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="icon"><path d="M 12,2C 17.5228,2 22,6.47716 22,12C 22,17.5228 17.5228,22 12,22C 6.47715,22 2,17.5228 2,12C 2,6.47716 6.47715,2 12,2 Z M 10.9999,16.5019L 17.9999,9.50193L 16.5859,8.08794L 10.9999,13.6739L 7.91391,10.5879L 6.49991,12.0019L 10.9999,16.5019 Z "></path></svg></div>
        <div class="notification__content">
			Document save to {docFile}
        </div>
    </div>
"""
				notifField = browser.find_element_by_class_name("notification")
				browser.execute_script("arguments[0].innerHTML = arguments[1];", notifField, notifHtml)
				sleep(1.)
				browser.execute_script("arguments[0].innerHTML = '';", notifField)

		def on_quit_shortcut():
			global windowName
			if get_focused_window() == windowName:
				on_close()
			else:
				print(f"INFO - Quit shortcut pressed, but the window {get_focused_window()} is not the proper one {windowName}")


		with keyboard.GlobalHotKeys({
			"<ctrl>+s": on_save_shortcut,
			"<ctrl>+q": on_quit_shortcut
		}) as h:
			h.join()

		# TODO Save on CTRL+S
		# Menu button: <button> tour-step-anchor menu
		#	<div> inner     Import/export
		#		<div> menu-entry__text flex flex--column
		#			<div>Export as Markdown


	except KeyboardInterrupt:
		on_close()	
