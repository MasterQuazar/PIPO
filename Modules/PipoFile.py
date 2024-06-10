import os
import json
import socket 
import copy

#c:/users/metal/onedrive/bureau/testproject
from textual.app import App, ComposeResult
from textual.widgets import Label,Button, Static, ListView, ListItem, OptionList, Header, Footer
from textual.screen import Screen 
from textual.widgets.selection_list import Selection
from textual.widgets.option_list import Option
from textual import events
from textual.containers import Horizontal, Vertical, Container, VerticalScroll
from pyfiglet import Figlet 
from time import sleep
from random import randrange 
from datetime import datetime
from multiprocessing import Manager

from collections import Counter

import scandir
import threading
import multiprocessing
import getpass
import pygetwindow as pg


#from Modules.PipoResearch import PipoSearchingApplication




"""
project_name = self.login_newproject_input.value
project_path = self.login_newprojectpath_input.value
"""

class PipoFileApplication():
	def save_edit_function(self):
		#get value in each text field
		#sequence version / shot version / asset version / asset name
		asset_name = self.screen.export_assetname_input.value
		asset_version = self.screen.export_version.value
		sequence_version = self.screen.export_sequence_version.value
		shot_version = self.screen.export_shot_version.value

		self.display_message_function("%s ; %s ; %s ; %s"%(asset_name, asset_version, sequence_version, shot_version))