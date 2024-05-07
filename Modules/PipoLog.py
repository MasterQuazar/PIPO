import os
import json
import socket 

from textual.app import App, ComposeResult
from textual.widgets import Label, Button, Static, ListView, ListItem, OptionList, Header, Footer
from textual.screen import Screen 
from textual import events
from textual.containers import Horizontal, Vertical, Container, VerticalScroll
from pyfiglet import Figlet 

from time import sleep
from datetime import datetime

import multiprocessing




class PipoLogApplication:
	"""
	def __init__(self):
		self.program_path = os.getcwd()
	"""


	def save_log_function(self, line):
		#convert line into string variable
		line = str(line)
		try:
			destination = os.path.join(self.program_path, "Data/logs/logs_main.dll")
			self.program_log.append(format)
		except AttributeError:
			destination = os.path.join(self.app.program_path, "Data/logs/logs_main.dll")
			self.app.program_log.append(format)
		except:
			return
		try:
			self.lobby_log.write_line(line)
		except:
			pass

		with open(destination, "a") as save_file:
			save_file.write("%s\n"%line)


		





	def display_message_function(self, message = ""):
		message = str(message)
		if message != "":
			format = "[%s] UPDATE : %s"%(str(datetime.now()), message)
		else:
			format = ""
		
		#self.notify(message, timeout=5, severity="information")

		self.save_log_function(format)


	def display_warning_function(self, message = ""):
		message = str(message)
		format = "[%s] WARNING : %s"%(str(datetime.now()), message)
		self.notify(message, timeout=5, severity="warning")

		self.save_log_function(format)

	def display_error_function(self, message = ""):
		message = str(message)
		format = "[%s] ERROR : %s"%(str(datetime.now()), message)
		self.notify(message, timeout=5, severity="error")


		self.save_log_function(format)



	def update_lobby_log_function(self, line=None):
		#check if the value of the copy is the same
		#if different update the log
		try:
			self.lobby_log.write_line(line)
		except:
			pass
			