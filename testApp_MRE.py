from textual.app import App, ComposeResult
from textual.widgets import TabbedContent, SelectionList, TabPane
from textual.widgets.selection_list import Selection
from textual import events
from textual.containers import Horizontal, Vertical, VerticalScroll

import multiprocessing
import threading 
import socket
import aioprocessing

import psutil
import os 
import colorama
import copy
import pyfiglet
import asyncio

from termcolor import *









class Example(App):
	CSS_PATH = "test.tcss"
	def __init__(self):
		super().__init__()






	def compose(self) -> ComposeResult:


		with VerticalScroll():
			with TabbedContent():
				with TabPane('test1'):
					with Vertical():
						self.test1_list = SelectionList(id="test1_list")
						yield self.test1_list
				with TabPane('test2'):
					with Vertical():
						self.test2_list = SelectionList(id='test2_list')
						yield self.test2_list


		for i in range(10):
			self.test1_list.add_option(Selection(str("hello world"),i))




	def on_selection_list_selection_toggled(self, event: SelectionList.SelectedChanged) -> None:

		"""
		when selecting something in the first selection list
		add the number to the second one
		"""
		if event.selection_list.id == "test1_list":
			#get selection
			selection = self.query_one("#test1_list").selected


			self.test2_list.clear_options()
			for i in range(len(selection)):
				self.test2_list.add_option(Selection(str(selection[i]), i))


	async def on_key(self, event: events.Key) -> None:
		if event.key == "p":
			self.exit()

if __name__ == "__main__":
	app = Example()
	app.run()
			