from textual.app import App, ComposeResult
from textual.widgets import Tabs, Tab, Label, Button, Static, Log, ListView, ListItem, OptionList, Header, SelectionList, Footer, Markdown, TabbedContent, TabPane, Input, DirectoryTree, Select, Tabs
from textual.widgets.option_list import Option, Separator
from textual.widgets.selection_list import Selection
from textual.screen import Screen 
from textual import events
from textual.containers import Horizontal, Vertical, Container, VerticalScroll
from pyfiglet import Figlet 
from time import sleep
from multiprocessing import freeze_support
from datetime import datetime
from textual import on

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

		if event.selection_list.id == "test1_list":
			self.notify("hello", timeout=2)


	async def on_key(self, event: events.Key) -> None:
		if event.key == "p":
			self.exit()

if __name__ == "__main__":
	app = Example()
	app.run()
			