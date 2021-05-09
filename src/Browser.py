#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Browser handles all the interaction with the Selenium driver"""
# std libs
import os
import platform
import subprocess
import pickle
from time import sleep
from urllib3.exceptions import MaxRetryError

# dependencies
try:
	from selenium import webdriver
	from selenium.common.exceptions import NoSuchElementException, WebDriverException
except ModuleNotFoundError as e:
	print(f"ERROR - Missing dependency: {e}.\nRun:\npip install -r requirements.txt")
	exit(1)



def new_tab(browser: object) -> None:
	"""Open a new tab"""
	browser.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 't')
	browser.find_element_by_tag_name("body").send_keys(Keys.COMMAND + 't')
	return


def wait_for_element(element2Find: str, browser: object) -> None:
	"""Alt the execution until an element2find by classname is on the page."""
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


def is_alive(browser: object) -> bool:
	"""Check if an instance of webdriver is still being executed."""
	try:
		browser.current_url
	except (MaxRetryError, WebDriverException):
		return False 
	else:
		return True


def on_close(scriptPath: str, browser: object) -> None:
	"""Actions to perform when the user request closing the browser."""
	# backup cookies
	if is_alive(browser):
		cookiesFile = os.path.join(scriptPath, "cookies.pkl")
		with open(cookiesFile, "wb") as f:
			pickle.dump(browser.get_cookies(), f)
		print("INFO - Cookies saved.")
		browser.close()
	else:
		print("WARN - Browser is dead. Cookies unsaved.")
	print("INFO - Bye.")
	exit(0)


def initialize(scriptPath: str) -> object:
	"""Launch a new instance of Selenium webdriver."""

	cookiesFile = os.path.join(scriptPath, "cookies.pkl")

	if platform.system() == "Linux":
		WEBDRIVER = os.path.join(scriptPath, "Webdrivers", "chromedriver_linux64")
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
	DATA_DIR = os.path.join(scriptPath, "BraveData")
	OPTION.add_argument("--user-data-dir=" + DATA_DIR)
	if not os.path.exists(DATA_DIR):
		os.mkdir(DATA_DIR) 
		print(f"INFO - User data directory created: {DATA_DIR}")
	else:
		print(f"INFO - Reusing prexisting user data directory: {DATA_DIR}")

		# Starts the browser
		try:
			browser = webdriver.Chrome(
					executable_path = WEBDRIVER,
					options = OPTION
				)
		except Exception as e:
			print(f"ERROR - It's seem an instance of brave is already running. Only one instance allowed: {e}")
			exit(1)

		# Loads cookies
		if os.path.exists(cookiesFile):
			print(f"INFO - Loading cookies from {cookiesFile}")
			with open(cookiesFile, "rb") as f:
				cookies = pickle.load(f)
			for c in cookies:
				browser.add_cookies(c)
			browser.refresh()
		else:
			print("INFO - No cookies file")

	return browser
