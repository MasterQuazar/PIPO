from textual.app import App, ComposeResult
from textual.widgets import Checkbox, Collapsible, Tabs, Tab, Label, Button, Static, Log, ListView, ListItem, OptionList, Header, SelectionList, Footer, Markdown, TabbedContent, TabPane, Input, DirectoryTree, Select, Tabs
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

import pygetwindow as pg
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
from Modules.PipoFile import PipoFileApplication
from Modules.PipoLog import PipoLogApplication









class PipoLobbyApplication(Screen, PipoCommonApplication, PipoFileApplication, PipoLogApplication):
	CSS_PATH = ["Data/Style/styleGlobal.tcss", "Data/Style/styleLobby.tcss"]




	def __init__(self):
		super().__init__()


		#create instance of the search files class
		#self.search_app = PipoSearchFilesApplication()


		self.opened_maya_scene_list = []

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
		with Horizontal(id = "main_application_horizontal_container"):
			with Vertical(id = "main_left_column"):

				

				with TabbedContent(id = "main_application_container_tab"):
					with TabPane("LOBBY"):
						with Horizontal(classes="lobby_main_container"):



							#CONTAIN ALL FEATURES AND OPTIONS
							with VerticalScroll(classes="lobby_left_column"):
								

								#MAYA SCENES MENU
								with Collapsible(title="MAYA SCENES MENU",classes="lobby_maya_scene_menu"):
									with Vertical(classes="lobby_maya_scene_container"):
										self.maya_scene_list = OptionList(id="lobby_maya_scene_list")
										self.maya_scene_list.border_title ="MAYA SCENES LIST" 
										yield self.maya_scene_list

								yield Button("Create sphere", id="create_sphere_button")




							with VerticalScroll(classes="lobby_center_column"):
								#with Vertical(classes="container_t2"):
								with Horizontal(classes="lobby_list_container"):
									with Vertical(classes="lobby_kind_container"):
										

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
												with Vertical(classes="lobby_name_container"):
													self.lobby_name_list = SelectionList(id="lobby_name_list", classes="optionlist_t1")
													self.lobby_name_list.border_title = "Name list"
													yield self.lobby_name_list
											with TabPane("Shots"):
												with Horizontal(classes="container_t2"):
													with Vertical(classes="lobby_sequence_container"):

														self.lobby_sequence_list = SelectionList(id="lobby_sequence_list", classes="optionlist_t1")
														self.lobby_sequence_list.border_title = "Sequence list"
														yield self.lobby_sequence_list
													with Vertical(classes="lobby_shot_container"):
														self.lobby_shot_list = SelectionList(id="lobby_shot_list", classes="optionlist_t1")
														self.lobby_shot_list.border_title = "Shot list"
														yield self.lobby_shot_list
										

									with Vertical(classes="lobby_type_container"):
										

										self.lobby_type_list = SelectionList(id="lobby_type_list", classes="optionlist_t1")
										self.lobby_type_list.border_title = "Type"
										yield self.lobby_type_list


								with Vertical(classes="lobby_file_container"):
									
									self.lobby_file_list = SelectionList(classes="selectionlist_t1", id="lobby_file_list")
									self.lobby_file_list.border_title = "Found files"
									yield self.lobby_file_list


							


					with TabPane("EXPORT"):
						with Horizontal(id="export_main_container"):
							with VerticalScroll(id = "export_left_container"):
								
								self.export_checkbox_customfolder = Checkbox("Export in custom folder")
								self.export_checkbox_currentfolder = Checkbox("Export in current folder")
								self.export_checkbox_defaultfolder = Checkbox("Export using default folder")
								self.export_checkbox_currentproject = Checkbox("Export in current project")

								yield self.export_checkbox_customfolder
								yield self.export_checkbox_currentfolder
								yield self.export_checkbox_defaultfolder
								yield self.export_checkbox_currentproject

								with Collapsible(title="Project template", classes="export_collapsible_project_template"):
									with VerticalScroll():
										self.export_project_template_list = OptionList(id="export_template_list")
										self.export_project_template_list.border_title = "Template list"
										yield self.export_project_template_list
										with Horizontal(id = "export_template_horizontal"):
											yield Button("Create new folder template", id="export_create_template_button")
											yield Button("Remove folder template", id="export_remove_template_button")
										yield Button("test")
									"""
									with VerticalScroll(id="export_collapsible_column"):
										

										with Horizontal(id = "export_template_horizontal"):
											yield Button("Create new folder template", id="export_create_template_button")
											yield Button("Remove folder template", id="export_remove_template_button")

										yield Button("Create template in project", id="export_create_folder_button")
									"""

								self.export_assetname_input =  Input(placeholder="Asset name", id="export_assetname_input")
								yield self.export_assetname_input
								yield Button("Get current scene name", id="export_getname_button")


								with Collapsible(title = "Export edit file", classes="export_collapsible_edit"):
									with VerticalScroll():
										with Horizontal(classes="export_collapsible_version_horizontal"):
											self.export_sequence_version = Input(value = "010",placeholder = "Sequence number", type="integer", id="export_sequence_version_textfield")
											self.export_shot_version = Input(value = "001",placeholder = "Shot number", type="integer", id="export_shot_version_textfield")
											yield self.export_sequence_version
											yield self.export_shot_version
										self.export_version = Input(value = "001",placeholder = "Asset version", type="integer", id="export_asset_version_textfield")

										
										yield self.export_version

										yield Button("Save edit file", id="export_edit_save")
										yield Button("Save edit from selection", id="export_edit_selection")
								with Collapsible(title = "Export publish file", classes="export_collapsible_publish"):
									yield Button("Save publish file", id="export_publish_save")
									yield Button("Save publish from selection", id="export_publish_selection")


							with Vertical(id = "export_right_container"):
								
								with Horizontal(id="export_list_container"):
									with Vertical(id="export_category_list_container"):
										self.export_category_list = OptionList(id = "export_category_list")
										self.export_category_list.border_title = "Category"
										yield self.export_category_list
									with Vertical(id = "export_type_list_container"):
										self.export_type_list = OptionList(id = "export_type_list")
										self.export_type_list.border_title = "Type"
										yield self.export_type_list

								self.export_nomenclature_display = Input(placeholder="", id="export_nomenclature_display")

								#yield Static("hello world")
				self.current_scene_label = Static("None", id="current_scene_label")
				yield self.current_scene_label					
			with VerticalScroll(classes="main_right_column"):
				self.lobby_log = Log(classes="lobby_log")
				self.lobby_log.border_title = "____ | LOGS | ___"
				yield self.lobby_log



		#self.display_message_function("hello")
		#update list values
		self.update_tui_list_function()
		#launch lobby log thread
		self.log_thread = threading.Thread(target=self.update_lobby_log_function, daemon=True, args=())
		self.log_thread.start()

		self.update_file_list_thread = threading.Thread(target=self.update_file_list_function, daemon=True, args=())
		self.update_file_list_thread.start()

		#create a thread that check each 1 seconds opened maya scene
		self.maya_scene_checker_thread = threading.Thread(target=self.update_maya_scene_list_function, daemon=True, args=())
		self.maya_scene_checker_thread.start()
		#self.display_message_function("checking started")











	def on_button_pressed(self, event: Button.Pressed) -> None:

		if event.button.id == "export_edit_save":
			#get kind and type selection
			#get value in each field
			#send to the save edit function
			self.save_edit_function()


		if event.button.id == "login_create_button":
			self.create_new_project_function()

		if event.button.id == "lobby_back_button":
			self.app.pop_screen()

		if event.button.id == "create_sphere_button":
			#get the currently selected scene
			#check if it is possible to get the associated port
			#in the connection log
			#try to open socket and send command
			
			#get the current selection
			#if no selection get the first scene in list
			current_maya_scene = self.query_one("#lobby_maya_scene_list").highlighted 

			if type(current_maya_scene) == int:
				#maya_scene_path = (self.opened_maya_scene_list[current_maya_scene].split("---")[0].split(" ")[-1]).replace("\\", "/")
				#self.display_message_function(self.opened_maya_scene_list[current_maya_scene])	
				#maya_scene_path = ((self.opened_maya_scene_list[current_maya_scene]).split(" ")[-1]).replace("\\", "/")
				#maya_scene_name = (self.opened_maya_scene_list[current_maya_scene].split("---"))[0].split(" ")
				#maya_scene_path = [item for item in maya_scene_name if item != ""][-1].replace("\\", "/")

				maya_scene_path = self.opened_maya_scene_list[current_maya_scene]


				scene_data = self.get_scene_data_function(maya_scene_path)

				if scene_data != None:
					self.display_message_function("%s : %s"%(scene_data["filename"], scene_data["port"]))
					command = "cmds.polySphere()"
					self.send_command_function(command, ("localhost",scene_data["port"]))
				else:
					self.display_error_function("Impossible to get scene data!")



	def on_option_list_option_highlighted(self, event: OptionList.OptionHighlighted) -> None:
		if event.option_list.id == "lobby_type_list":
			self.display_message_function("hello world")

		if event.option_list.id == "lobby_maya_scene_list":
			#get the selection of maya scenes
			scene_selection = self.query_one("#lobby_maya_scene_list").highlighted

			if type(scene_selection) == int:

				self.current_scene_label.update(self.opened_maya_scene_list[scene_selection])

		if event.option_list.id == "export_category_list":
			try:
				#get the current index selected
				kind_index = self.query_one("#export_category_list").highlighted
				kind_list = list(self.app.current_project_settings["Scenes"].keys())
				kind_selected = kind_list[kind_index]
				type_list = self.app.current_project_settings["Scenes"][kind_selected]["type"]
			except:
				self.display_error_function("Impossible to get the category type list!")
				return
			else:
				self.export_type_list.clear_options()

				for t in type_list:
					self.export_type_list.add_option(Option(t))
				



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
			self.display_message_function("SHOT SELECTED")
			shot_selection = self.query_one("#lobby_shot_list").selected 
			self.name_shots_selection = []

			for shot in shot_selection:

				self.name_shots_selection.append(self.name_shots_list[shot])
			self.display_message_function(self.name_shots_selection)

		
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




	def update_tui_list_function(self):
		#get the value in settings
		#empty current lists
		self.lobby_kind_list.clear_options
		self.lobby_type_list.clear_options

		i = 0
		for key, value in app.current_project_settings["Scenes"].items():
			self.lobby_kind_list.add_option(Selection(key,i))
			self.export_category_list.add_option(Option(key))
			i+=1

		#self.lobby_kind_list.select(0)

		#get the type list for the first type in settings
		#first_kind = list(app.current_project_settings["Scenes"].keys())[0]
		#type_list = app.current_project_settings["Scenes"][first_kind]["type"]
		"""
		for i in range(len(type_list)):
			self.lobby_type_list.add_option(Selection(type_list[i],i))
		"""






	async def on_key(self, event: events.Key) -> None:
		#if event.key == "1":
		#	self.app.push_screen(PipoLobbyApplication())
		if event.key == "m":
			self.app.pop_screen()

		"""
		if event.key == "2":
			self.app.switch_screen(PipoExportApplication())
		if event.key == "3":
			self.app.switch_screen(PipoObserverApplication())
		"""





	









class PipoSettingsApplication(Screen):
	def compose(self) -> ComposeResult:
		yield Label("SETTINGS PAGE")


class PipoExportApplication(Screen, PipoCommonApplication, PipoLogApplication):
	def compose(self) -> ComposeResult:


		"""
		EXPORT PAGES NEEDED FEATURES
			informations required for filename
				category
				name
				version / sequence - shots version
				type
			destination settings
				-> export using default folder settings (automatic)
				-> export in the current maya project (even with different name)
				-> export in a custom location (open file explorer for custom destination if possible)
		"""
		


		#self.update_export_list_function()
		yield Button("hello world")

	def update_export_list_function(self):
		for key, value in self.app.current_project_settings.items():
			self.display_message_function("%s : %s"%(key, value))

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
		self.check_for_autorun_function()

		self.display_message_function(self.personnal_data)
		
		#put the differents projects inside the project list
		try:
			for key, value in self.personnal_data["ProjectList"].items():
				#self.login_project_list.append(ListItem(Label(key)))
				self.login_project_list.add_option(Option(key))
		except:
			self.display_error_function("Impossible to display project list!")


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