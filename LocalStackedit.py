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
except ModuleNotFoundError as e:
	print(f"Missing dependency: {e}. Run:\npip install -r requirements.txt")
	exit(1)

# ==============================================================================
#                                     SETUP
# ==============================================================================

PLATFORM = platform.system()
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
COOKIES_FILE = os.path.join(SCRIPT_PATH, "cookies.pkl")


if PLATFORM == "Windows":
	WEBDRIVER = os.path.join(SCRIPT_PATH, "Webdrivers", "chromedriver.exe")
	BRAVE_PATH = subprocess.check_output(["where", "brave-browser"]).decode("utf-8")
elif PLATFORM == "Linux":
	WEBDRIVER = os.path.join(SCRIPT_PATH, "Webdrivers", "chromedriver_linux64")
	BRAVE_PATH = subprocess.check_output(["which", "brave-browser"]).decode("utf-8")
else:
	raise NotImplementedError("This script doesn't deal with MacOS")
	exit(1)

# For some reason, trailing spaces are added to the output
BRAVE_PATH = BRAVE_PATH.strip()
print("Brave binary path: ", BRAVE_PATH)
OPTION = webdriver.ChromeOptions()
OPTION.binary_location = BRAVE_PATH

# Directory for brave's user data
DATA_DIR = os.path.join(SCRIPT_PATH, "BraveData")
OPTION.add_argument("--user-data-dir=" + DATA_DIR)
if not os.path.exists(DATA_DIR):
	IS_FIRST_LAUNCH = True
	os.mkdir(DATA_DIR) 
	print(f"User data directory created:\n{DATA_DIR}")
else:
	print(f"Reusing prexisting user data directory:\n{DATA_DIR}")

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

	while not isFound:
		try:
			browser.find_element_by_class_name(element2Find)
		except NoSuchElementException:
			isFound = False
			sleep(.25)
		else:
			isFound = True

	print(f"Page loaded with element of class {element2Find}.")
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
	# backup cookies
	if is_alive():
		with open(COOKIES_FILE, "wb") as f:
			pickle.dump(browser.get_cookies(), f)
		print("Cookies saved.")
		browser.close()
	else:
		print("Browser is dead. Cookies unsaved.")
	print("Bye.")


# ==============================================================================
#                                      MAIN
# ==============================================================================
if __name__ == "__main__":
	# Check user input
	if len(sys.argv) < 2:
		print("The filename to open should be provided.")
		exit(1)

	try:
		# Starts the browser
		try:
			browser = webdriver.Chrome(
					executable_path = WEBDRIVER,
					options = OPTION
				)
		except Exception as e:
			print(e)
			print("It's seem an instance of brave is already running. Only one instance allowed.")
			exit(1)
		# Loads cookies
		if os.path.exists(COOKIES_FILE):
			print("Loading cookies...")
			with open(COOKIES_FILE, "rb") as f:
				cookies = pickle.load(f)
			for c in cookies:
				browser.add_cookies(c)
			browser.refresh()
		else:
			print("No cookies file")

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

	except KeyboardInterrupt:
		on_close()	
