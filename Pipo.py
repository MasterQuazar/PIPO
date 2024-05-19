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
import aioprocessing

import psutil
import os 
import colorama
import copy
import pyfiglet
import asyncio

from termcolor import *


colorama.init() 


from Modules.PipoCommon import PipoCommonApplication
from Modules.PipoLog import PipoLogApplication









class PipoLobbyApplication(Screen, PipoCommonApplication, PipoLogApplication):
	CSS_PATH = ["Data/Style/styleGlobal.tcss", "Data/Style/styleLobby.tcss"]




	def __init__(self):
		super().__init__()


		#create instance of the search files class
		#self.search_app = PipoSearchFilesApplication()



		self.name_name_selection = []
		self.name_kind_selection = []
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

		self.kind_change_list = []

		self.searching_thread = None

		self.file_list_image = None
		self.searching_process_list = []



		


		

		
		#self.kind_list = app.current_project_settings["Scenes"].keys()

	
	

	def compose(self) -> ComposeResult:

		"""
		yield Laself.create_variable_function()


	def create_variable_function(self):
		print()bel("bonjour le monde!")


		self.test_list = ListView()
		yield self.test_list

		for i in range(0, 10):
			self.test_list.append(ListItem(Label("Item %s"%i)))

		self.back_button = Button("Back to login", id="lobby_back_button")
		yield self.back_button
		"""
		with Horizontal(classes="lobby_main_container"):
			with VerticalScroll(classes="lobby_left_column"):
				yield Static("hello world!")
			with VerticalScroll(classes="lobby_center_column"):
				#with Vertical(classes="container_t2"):
				with Horizontal(classes="lobby_list_container"):
					with Vertical(classes="container_t2"):
						

						#self.lobby_kind_list = OptionList(id="lobby_kind_list", classes="optionlist_t1")
						#yield self.lobby_kind_list
						self.lobby_kind_list = SelectionList[int](id="lobby_kind_list")
						self.lobby_kind_list.border_title = "Category"
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

										self.lobby_sequence_list = SelectionList(id="lobby_sequence_list", classes="optionlist_t1")
										self.lobby_sequence_list.border_title = "Sequence list"
										yield self.lobby_sequence_list
									with Vertical(classes="container_t2"):
										self.lobby_shot_list = SelectionList(id="lobby_shot_list", classes="optionlist_t1")
										self.lobby_shot_list.border_title = "Shot list"
										yield self.lobby_shot_list

					with Vertical(classes="container_t2"):
						

						self.lobby_type_list = SelectionList(id="lobby_type_list", classes="optionlist_t1")
						self.lobby_type_list.border_title = "Type"
						yield self.lobby_type_list


				with Vertical(classes="lobby_bottom_container"):
					
					self.lobby_file_list = SelectionList(classes="selectionlist_t1", id="lobby_file_list")
					self.lobby_file_list.border_title = "Found files"
					yield self.lobby_file_list


			with VerticalScroll(classes="lobby_right_column"):
				self.lobby_log = Log(classes="lobby_log")
				yield self.lobby_log
		


		#self.display_message_function("hello")
		#update list values
		self.update_lobby_list_function()
		#launch lobby log thread
		self.log_thread = threading.Thread(target=self.update_lobby_log_function, daemon=True, args=())
		self.log_thread.start()

		self.update_file_list_thread = threading.Thread(target=self.update_file_list_function, daemon=True, args=())
		self.update_file_list_thread.start()














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

		if event.selection_list.id == "lobby_name_list":
			name_selection = self.query_one("#lobby_name_list").selected
			self.name_name_selection = []

			for name in name_selection:
				self.name_name_selection.append(self.name_name_list[name])

		if event.selection_list.id == "lobby_sequence_list":
			sequence_selection = self.query_one("#lobby_sequence_list").selected 
			self.name_sequence_selection = []

			for sequence in sequence_selection:
				#self.display_message_function(self.name_sequence_list[sequence])
				self.name_sequence_selection.append(self.name_sequence_list[sequence])

		if event.selection_list.id == "lobby_shot_list":
			shot_selection = self.query_one("#lobby_shot_list").selected 
			self.name_shots_selection = []

			for shot in shot_selection:
				self.name_shots_selection.append(self.name_shots_list[shot])


		
		if event.selection_list.id in ["lobby_name_list", "lobby_type_list", "lobby_sequence_list", "lobby_shot_list", "lobby_kind_list"]:
			#get value of the selection
			#for each list
			self.kind_selection = self.query_one("#lobby_kind_list").selected
			self.type_selection = self.query_one("#lobby_type_list").selected 
			self.name_selection = self.query_one("#lobby_name_list").selected
			self.shot_selection = self.query_one("#lobby_shot_list").selected
			self.sequence_selection = self.query_one("#lobby_sequence_list").selected
			#self.display_message_function(str(kind_selection))
			#self.display_message_function(str(type_selection))
			#self.display_message_function(str(name_selection))


			self.search_files_function()			




				

		
		#self.display_message_function(self.name_kind_selection)





	def on_option_list_option_highlighted(self, event: OptionList.OptionHighlighted) -> None:
		if event.option_list.id == "lobby_type_list":
			self.display_message_function("hello world")




	def update_file_list_function(self):
		#check changes in the final file queue
		#if the queue changed, update the file list in lobby
		#and create an image of the queue to remember its current state!
		while True:
			#create a copy of the queue
			#queue_copy = self.app.final_file_queue
			#file_list = []

			if self.app.final_file_list != self.file_list_image: 
				#clean the options in the list
				self.lobby_file_list.clear_options()
				#copy the value of the current file list in image list
				#update the final file list
				self.file_list_image = self.app.final_file_list

				for i in range(len(self.file_list_image)):
					self.lobby_file_list.add_option(Selection(self.file_list_image[i],i))

			sleep(0.5)




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
	CSS_PATH = ["Data/Style/StyleGlobal.tcss","Data/Style/styleLogin.tcss"]




	def __init__(self):


		self.program_informations = {
			"author":"MasterQuazar",
			"github":"https://MasterQuazar/PIPO",
			"version":"v.02",
			"title":"PIPO",
		}

		self.personnal_data = {}


		self.program_path = os.getcwd()

		self.program_log = []
		self.program_log_copy = []

		self.project_name = None
		self.project_path = None




		manager = multiprocessing.Manager()
		self.final_file_queue = manager.Queue()
		self.final_file_list = []



		
		
		self.font_title = Figlet(font="bloody")
		self.font_big = Figlet(font="dos_rebel")
		self.font_subtitle = Figlet(font="digital")
		#self.content_list = ["bonjour", "bonsoir", "matin", "midi", "soir"]


		

		self.save_log_function("\n\n[%s] New Pipo session opened on %s"%(str(datetime.now()), socket.gethostname))
		super().__init__()





	







	def compose(self) -> ComposeResult:
		yield Header()

		self.title = "Pipo Pipeline Manager"
		self.sub_title = "created by Quazar"

		with Horizontal(classes="main_login_page_container"):
			yield VerticalScroll()

			with VerticalScroll(classes = "login_container"):
				with Horizontal(classes = "container_t2"):
					with Vertical(classes="login_title_container"):	
						self.login_welcomelabel = Label(self.font_title.renderText(self.program_informations["title"]), classes="login_main_title")
						self.login_versionlabel = Label(self.font_big.renderText(self.program_informations["version"]), classes="login_main_subtitle")
						yield self.login_welcomelabel
						yield self.login_versionlabel

						

					with Vertical(classes="login_project_settings_column"):
					
						#yield Label(self.font_subtitle.renderText("PROJECT LIST"), classes="label_t1")

						self.login_project_list = OptionList(classes="login_projectlist", id="login_projectlist")
						self.login_project_list.border_title = "PROJECT LIST"
						#self.login_project_list = ListView(classes="login_projectlist", id="login_projectlist")
						yield self.login_project_list

						

						with Vertical(classes="login_project_options_container"):

							self.login_openproject_button = Button("Open existing Project", id="login_open_button", classes="button_t1")
							self.login_loadproject_button = Button("Load an other Project", id="login_load_button", classes="button_t1")

							yield self.login_loadproject_button
							yield self.login_openproject_button

							self.login_newproject_input = Input(placeholder="New project name", classes="login_input_field")
							self.login_newprojectpath_input = Input(placeholder="New project path", classes="login_input_field")
							self.login_createproject_button = Button("Create a new Project", id="login_create_button", classes="button_t1")

							
							yield self.login_newproject_input
							yield self.login_newprojectpath_input
							yield self.login_createproject_button

						#self.login_alert_label = Label()
						#yield self.login_alert_label

			
			yield VerticalScroll()
		yield Horizontal()

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