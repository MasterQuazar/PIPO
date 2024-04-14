from textual.app import App, ComposeResult
from textual.widgets import Label, Button, Static, Log, ListView, ListItem, OptionList, Header, SelectionList, Footer, Markdown, TabbedContent, TabPane, Input, DirectoryTree, Select, Tabs
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

import psutil
import os 
import colorama
import copy
import pyfiglet


from termcolor import *


colorama.init() 


from Modules.PipoCommon import PipoCommonApplication
from Modules.PipoLog import PipoLogApplication










class PipoLobbyApplication(Screen, PipoCommonApplication, PipoLogApplication):
	CSS_PATH = "Data/Style/styleLobby.tcss"



	def __init__(self):
		super().__init__()

		self.name_kind_selection = []
		self.name_name_selection = []
		self.name_shots_selection = []
		self.name_sequence_selection = []
		self.name_type_selection = []
		self.name_file_selection = []

		self.name_kind_list = []
		self.name_name_list = []
		self.name_shots_list = []
		self.name_sequence_list = []
		self.name_type_list = []
		self.name_file_list = []

		
		#self.kind_list = app.current_project_settings["Scenes"].keys()


	

	def compose(self) -> ComposeResult:

		"""
		yield Label("bonjour le monde!")


		self.test_list = ListView()
		yield self.test_list

		for i in range(0, 10):
			self.test_list.append(ListItem(Label("Item %s"%i)))

		self.back_button = Button("Back to login", id="lobby_back_button")
		yield self.back_button
		"""
		with Horizontal(classes="lobby_main_container"):
			with VerticalScroll(classes="lobby_left_column"):
				yield Button("Hello world", classes="button_t1")
				yield Button("Hello world", classes="button_t1")
				yield Button("Hello world", classes="button_t1")

			with VerticalScroll(classes="lobby_center_column"):
				#with Vertical(classes="container_t2"):
				with Horizontal(classes="lobby_list_container"):
					with Vertical(classes="container_t2"):
						yield Label("Category")

						#self.lobby_kind_list = OptionList(id="lobby_kind_list", classes="optionlist_t1")
						#yield self.lobby_kind_list
						self.lobby_kind_list = SelectionList[int](id="lobby_kind_list")
						yield self.lobby_kind_list

						"""
						for i in range(0, 10):
							self.lobby_kind_list.add_option(Selection("Hello world %s"%i, i))
						"""



					with Vertical(classes="container_t2"):

						with TabbedContent(classes="tabbedcontent_t1"):
							with TabPane("Name"):
								with Vertical(classes="container_t2"):
									self.lobby_name_list = SelectionList(id="lobby_name_list", classes="optionlist_t1")
									yield self.lobby_name_list
							with TabPane("Shots"):
								with Horizontal(classes="container_t2"):
									with Vertical(classes="container_t2"):
										yield Label("Sequence")
										self.lobby_sequence_list = SelectionList(id="lobby_sequence_list", classes="optionlist_t1")
										yield self.lobby_sequence_list
									with Vertical(classes="container_t2"):
										yield Label("Shots")
										self.lobby_shot_list = SelectionList(id="lobby_shot_list", classes="optionlist_t1")
										yield self.lobby_shot_list

					with Vertical(classes="container_t2"):
						yield Label("Type")

						self.lobby_type_list = SelectionList(id="lobby_type_list", classes="optionlist_t1")
						yield self.lobby_type_list


				with Vertical(classes="lobby_bottom_container"):
					yield Label("Found files")
					self.lobby_file_list = SelectionList(classes="lobby_file_list")
					yield self.lobby_file_list


			with VerticalScroll(classes="lobby_right_column"):
				self.lobby_log = Log(classes="lobby_log")
				yield self.lobby_log
		


		#self.display_message_function("hello")
		#update list values
		self.update_lobby_list_function()
		#launch lobby log thread
		#self.log_thread = threading.Thread(target=self.update_lobby_log_function, daemon=True, args=())
		#self.log_thread.start()











	def on_selection_list_selection_toggled(self, event: SelectionList.SelectedChanged ) -> None:
		#self.display_message_function(str(event.selection_list.id))

		#UPDATE THE TYPE LIST
		if event.selection_list.id == "lobby_kind_list":
			self.lobby_type_list.clear_options()
			#get the type list for the selected type
			#make the difference between both lists if several kind selected
			kind_selection = self.query_one("#lobby_kind_list").selected 

			self.name_kind_selection = []

			for index in kind_selection:
				self.name_kind_selection.append(list(app.current_project_settings["Scenes"].keys())[index])

			self.full_type_list = []
			for kind in self.name_kind_selection:
				self.full_type_list.append(app.current_project_settings["Scenes"][kind]["type"])
			#self.display_message_function(self.full_type_list)
			#create the intersection of all lists
			
			self.name_type_list =[]
			self.name_type_selection = []
			try:
				self.name_type_list = list(set.intersection(*map(set, self.full_type_list)))
			except:
				pass
			else:
				for i in range(len(self.name_type_list)):
					#self.name_type_selection.append(self.name_type_list[i])
					#self.display_message_function(self.name_type_list[i])
					self.lobby_type_list.add_option(Selection(self.name_type_list[i],i))	



		if event.selection_list.id == "lobby_type_list":
			type_selection = self.query_one("#lobby_type_list").selected
			self.name_type_selection = []

			for index in type_selection:
				self.name_type_selection.append(self.name_type_list[index])


		
		if event.selection_list.id in ["lobby_name_list", "lobby_type_list", "lobby_sequence_list", "lobby_shots_list", "lobby_kind_list"]:
			#get value of the selection
			#for each list
			kind_selection = self.query_one("#lobby_kind_list").selected
			type_selection = self.query_one("#lobby_type_list").selected 
			name_selection = self.query_one("#lobby_name_list").selected
			shot_selection = self.query_one("#lobby_shot_list").selected
			sequence_selection = self.query_one("#lobby_sequence_list").selected
			#self.display_message_function(str(kind_selection))
			#self.display_message_function(str(type_selection))
			#self.display_message_function(str(name_selection))

			self.display_message_function(kind_selection)

			#self.name_kind_selection = []

			self.search_files_function()
		







		
		
		#self.display_message_function(self.name_kind_selection)





	def on_option_list_option_highlighted(self, event: OptionList.OptionHighlighted) -> None:
		if event.option_list.id == "lobby_type_list":
			self.display_message_function("hello world")




	def update_lobby_list_function(self):
		#get the value in settings
		#empty current lists
		self.lobby_kind_list.clear_options
		self.lobby_type_list.clear_options

		i = 0
		for key, value in app.current_project_settings["Scenes"].items():
			self.lobby_kind_list.add_option(Selection(key,i))
			i+=1

		#self.lobby_kind_list.select(0)

		#get the type list for the first type in settings
		#first_kind = list(app.current_project_settings["Scenes"].keys())[0]
		#type_list = app.current_project_settings["Scenes"][first_kind]["type"]
		"""
		for i in range(len(type_list)):
			self.lobby_type_list.add_option(Selection(type_list[i],i))
		"""



	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "login_create_button":
			self.create_new_project_function()

		if event.button.id == "lobby_back_button":
			self.app.pop_screen()

	async def on_key(self, event: events.Key) -> None:
		#if event.key == "1":
		#	self.app.push_screen(PipoLobbyApplication())
		if event.key == "m":
			self.app.pop_screen()
		if event.key == "2":
			self.app.switch_screen(PipoExportApplication())
		if event.key == "3":
			self.app.switch_screen(PipoObserverApplication())















class PipoSettingsApplication(Screen):
	def compose(self) -> ComposeResult:
		yield Label("SETTINGS PAGE")


class PipoExportApplication(Screen):
	def compose(self) -> ComposeResult:
		yield Label("EXPORT PAGE")

	async def on_key(self, event: events.Key) -> None:
		if event.key == "1":
			self.app.switch_screen(PipoLobbyApplication())
		if event.key == "3":
			self.app.switch_screen(PipoObserverApplication())
		if event.key == "m":
			self.app.pop_screen()


class PipoObserverApplication(Screen):
	def compose(self) -> ComposeResult:
		yield Label("OBSERVER PAGE")


	async def on_key(self, event: events.Key) -> None:
		if event.key == "1":
			self.app.switch_screen(PipoLobbyApplication())
		if event.key == "2":
			self.app.switch_screen(PipoExportApplication())

		if event.key == "m":
			self.app.pop_screen()

















class PipoLoginApplication(App, PipoCommonApplication, PipoLogApplication):

	SCREENS = {
		"LOBBY": PipoLobbyApplication(),
	}
	CSS_PATH = "Data/Style/styleLogin.tcss"




	def __init__(self):

		self.personnal_data = {}


		self.program_path = os.getcwd()

		self.program_log = []
		self.program_log_copy = []

		self.current_project_name = None
		self.current_project_path = None
		
		

		self.font_title = Figlet(font="bloody")
		self.font_subtitle = Figlet(font="digital")
		#self.content_list = ["bonjour", "bonsoir", "matin", "midi", "soir"]


		

		self.save_log_function("\n\n[%s] New Pipo session opened on %s"%(str(datetime.now()), socket.gethostname))
		super().__init__()





	







	def compose(self) -> ComposeResult:
		yield Header()

		self.title = "Pipo Pipeline Manager"
		self.sub_title = "created by Quazar"

		yield VerticalScroll()

		with VerticalScroll(classes = "login_container"):
			with Horizontal(classes = "container_t2"):
				with Vertical(classes="container_t3"):	
					self.login_welcomelabel = Label(self.font_title.renderText("PIPO\npipeline manager"), classes="title_t1")
					yield self.login_welcomelabel

					

				with Vertical(classes="container_t3"):
					with Vertical(classes="container_t4"):
						yield Label(self.font_subtitle.renderText("PROJECT LIST"), classes="label_t1")

						self.login_project_list = OptionList(classes="login_projectlist", id="login_projectlist")
						#self.login_project_list = ListView(classes="login_projectlist", id="login_projectlist")
						yield self.login_project_list

					self.login_openproject_button = Button("Open existing Project", id="login_open_button", classes="button_t1")
					self.login_loadproject_button = Button("Load an other Project", id="login_load_button", classes="button_t1")

					yield self.login_loadproject_button
					yield self.login_openproject_button

					with Vertical(classes="container_t5"):
						self.login_newproject_input = Input(placeholder="New project name", classes="login_input_field")
						self.login_newprojectpath_input = Input(placeholder="New project path", classes="login_input_field")
						self.login_createproject_button = Button("Create a new Project", id="login_create_button", classes="button_t1")

						
						yield self.login_newproject_input
						yield self.login_newprojectpath_input
						yield self.login_createproject_button

					#self.login_alert_label = Label()
					#yield self.login_alert_label

		
		yield VerticalScroll()

		self.load_personnal_settings_function()
		#put the differents projects inside the project list
		for key, value in self.personnal_data["ProjectList"].items():
			#self.login_project_list.append(ListItem(Label(key)))
			self.login_project_list.add_option(Option(key))


	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "login_create_button":
			self.create_new_project_function()

		if event.button.id == "login_open_button":
			project_opening_value = self.open_project_function()

			#self.display_message_function(str(project_opening_value))
			if type(project_opening_value) == list:
				self.project_name = project_opening_value[0]
				self.project_path = project_opening_value[1]
				self.push_screen(PipoLobbyApplication())



	async def on_key(self, event: events.Key) -> None:
		if event.key == "p":
			self.exit()


	



	






if __name__ == "__main__":
	app = PipoLoginApplication()
	app.run()