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


	def save_log_function(self, line):
		self.program_log.append(format)
		#self.notify("LOG UPDATED", timeout=3)

		with open(os.path.join(self.program_path, "Data/Logs/Logs_main.dll"), "a") as save_file:
			save_file.write("%s\n"%line)
		try:
			self.update_lobby_log_function(line)
		except:
			self.notify("Impossible to update log", severity="error", timeout=5)
		





	def display_message_function(self, message = ""):
		format = "[%s] UPDATE : %s"%(str(datetime.now()), message)
		self.notify(message, timeout=5, severity="information")

		self.save_log_function(format)


	def display_warning_function(self, message = ""):
		format = "[%s] WARNING : %s"%(str(datetime.now()), message)
		self.notify(message, timeout=5, severity="warning")

		self.save_log_function(format)

	def display_error_function(self, message = ""):
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
			