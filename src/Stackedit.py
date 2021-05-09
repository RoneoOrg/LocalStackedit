#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Stackedit handles all the interactions with stackedit.io/#app"""

# Std libs
from time import sleep
import os
# Modules
from . import Browser


def make_notif(content: str, browser: object) -> None:
	"""Popup a notification"""
	notifHtml = f"""
<div class="notification__item flex flex--row flex--align-center">
<div class="notification__icon flex flex--column flex--center"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="icon"><path d="M 12,2C 17.5228,2 22,6.47716 22,12C 22,17.5228 17.5228,22 12,22C 6.47715,22 2,17.5228 2,12C 2,6.47716 6.47715,2 12,2 Z M 10.9999,16.5019L 17.9999,9.50193L 16.5859,8.08794L 10.9999,13.6739L 7.91391,10.5879L 6.49991,12.0019L 10.9999,16.5019 Z "></path></svg></div>
<div class="notification__content">
{content}
</div>
</div>
"""
	notifField = browser.find_element_by_class_name("notification")
	browser.execute_script("arguments[0].innerHTML = arguments[1];", notifField, notifHtml)
	sleep(1.)
	browser.execute_script("arguments[0].innerHTML = '';", notifField)
	

def initialize(filePath: str, browser: object) -> object:
		"""Open stackedit.io and loads the filePath file. Returns the editor area."""
		# Open stakedit page
		browser.get("https://stackedit.io/app#")
		Browser.wait_for_element("editor", browser)

		# Get stackedit document title
		titleField = browser.find_elements_by_tag_name("input")[0]
		# Set the title
		titleField.click()
		docTitle = os.path.basename(filePath).split(".")[0]
		titleField.send_keys(docTitle)
		
		# Get stackedit editor area
		editorField = browser.find_elements_by_class_name("editor")[0]
		editorField = editorField.find_element_by_tag_name("pre")
		# clear the editor
		browser.execute_script("arguments[0].innerHTML=''", editorField)

		# set the content of the editor
		with open(filePath, "r") as f:
			browser.execute_script("arguments[0].innerHTML=arguments[1]", editorField, f.read())

		# Set the windows title to be grabbed by Xlib
		browser.execute_script("document.title=arguments[0]", f"Stackedit - {docTitle}")

		# Wait for the document title to be set
		# It takes time for the windows title to be set
		# according to the document title
		sleep(.5)
	
		return editorField

