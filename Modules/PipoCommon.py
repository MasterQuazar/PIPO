import os
import json
import socket 
import copy

from textual.app import App, ComposeResult
from textual.widgets import Label,Button, Static, ListView, ListItem, OptionList, Header, Footer
from textual.screen import Screen 
from textual.widgets.selection_list import Selection
from textual import events
from textual.containers import Horizontal, Vertical, Container, VerticalScroll
from pyfiglet import Figlet 
from time import sleep
from random import randrange 
from datetime import datetime

import scandir
import threading
import multiprocessing


from Modules.PipoResearch import PipoSearchingApplication


<<<<<<< HEAD
class PipoSearchFilesApplication():
	def test_function(self):
		self.notify("hello world", timeout=5)
=======
>>>>>>> 6ee8f77d51a475f0e20757bbc382914487e8cb9a




class PipoCommonApplication():
		





	def load_personnal_settings_function(self):
		#search the personnal settings file in the data folder
		"""
		if the file doesn't exist create it
		if it's impossible to read the file print an error
		"""
		if os.path.isfile(os.path.join(os.getcwd(), "Data/PipoPersonnalData.json"))==False:
			#display error
			self.display_error_function("Settings file doesn't exist")
			#self.display_error_function("Settings file doesn't exists!")
			self.personnal_data = self.create_personnal_settings_file_function()
		else:
			try:
				with open("Data/PipoPersonnalData.json", "r") as read_data:
					self.personnal_data = json.load(read_data)
			except:
				#display error
				self.display_error_function("Impossible to read personnal settings file")
			else:
				self.display_message_function("Personnal settings opened")







	def create_personnal_settings_file_function(self):
		#create the personnal settings dictionnary
		personnal_dictionnary = {
			"ComputerName": socket.gethostname(),
			"ProjectList": {}
		}

		with open("Data/PipoPersonnalData.json", "w") as save_personnal_data:
			json.dump(personnal_dictionnary, save_personnal_data, indent=4)
		self.display_message_function("Default personnal settings created")
		return personnal_dictionnary




	def create_default_settings_file_function(self):
		default_settings = {
			"Scenes": {
				"character": {
					"syntax":"[key]_[name]_[type]_[version]",
					"keyword":"char",
					"type":["mod", "rig", "sculpt", "groom", "lookdev"],
					"folder":["[Origin]/ASSETS/[name]/[mayaProject]/scenes/[type]/[state]"]
				},
				"prop": {
					"syntax":"[key]_[name]_[type]_[version]",
					"keyword":"prop",
					"type":["mod", "rig", "sculpt", "groom", "lookdev"],
					"folder":["[Origin]/ASSETS/[name]/[mayaProject]/scenes/[type]/[state]"]
				},
				"item": {
					"syntax":"[key]_[name]_[type]_[version]",
					"keyword":"item",
					"type":["mod", "rig", "sculpt", "groom", "lookdev"],
					"folder":["[Origin]/ASSETS/[name]/[mayaProject]/scenes/[type]/[state]"]
				},
				"set": {
					"syntax":"[key]_[name]_[type]_[version]",
					"keyword":"set",
					"type":["mod", "rig", "sculpt", "groom", "lookdev"],
					"folder":["[Origin]/ASSETS/[name]/[mayaProject]/scenes/[type]/[state]"]
				},
				"shots": {
					"syntax":"[sqversion]_[shversion]_[type]_[version]",
					"keyword":None,
					"type":["mod", "rig", "sculpt", "groom", "lookdev"],
					"folder":["[Origin]/SHOTS/[sqversion]/[sqversion]_[shversion]/[type]/[state]"]
				},
			},
			"Global": {
				"mayaFolder":"maya",
				"stateList":["edit", "publish"],
				"lodList":["1","2","3"],
				"3dScenesExtension":[".ma", ".mb"],
				"3dItemsExtension":[".obj", ".fbx"],
			}
		}
		return default_settings




	def create_new_project_function(self):
		#get the content of the name
		project_name = self.login_newproject_input.value
		project_path = self.login_newprojectpath_input.value
		

		"""
		check if the project folder exists
		check if there is already a project inside
		check if the project is already in the project list
		"""

		if os.path.isdir(project_path)==False:
			self.display_error_function("That project folder doesn't exists!")
		else:
			if os.path.isdir(os.path.join(project_path, "PipoManagerData"))==True:
				self.display_error_function("A project is already defined here!")
			else:
				if project_name in list(self.personnal_data["ProjectList"].keys()):
					self.display_error_function("You already have a project with that name!")
				else:
					project_list = self.personnal_data["ProjectList"]
					project_list[project_name] = {
						"projectPath":project_path,
						"projectCreator":socket.gethostname(),
						"projectDate":str(datetime.now())
					}			
					os.mkdir(os.path.join(project_path, "PipoManagerData"))		
					default_settings = self.create_default_settings_file_function()
					
					with open(os.path.join(project_path, "PipoManagerData/PipelineSettings.json"), "w") as save_settings:
						json.dump(default_settings, save_settings, indent=4)

					self.personnal_data["ProjectList"] = project_list
					self.save_personnal_data()
					#update the project list
					self.login_project_list.append(ListItem(Label(project_name)))
					self.display_message_function("Project created successfully!")

		#self.login_alert_label.update("%s ; %s"%(project_name, project_path))





	def open_project_function(self):
		#get the current value selected in textscrolllist
		
		#FOR OPTION LIST
		project_list = self.query_one("#login_projectlist", OptionList)
		#current_option = project_selection.get_option_at_index(project_selection.highlighted)
		current_option_index = project_list.highlighted
		#current_content = project_selection.get_option_at_index(current_option_index)
		project_name = list(self.personnal_data["ProjectList"].keys())[current_option_index]
		

		self.display_message_function(str("Project selected : %s"%project_name))
		#check if project exists (path)
		#check if it's possible to get the settings from that project
		#go to lobby and load informations of that project!

		#get the path of the project
		project_path = self.personnal_data["ProjectList"][project_name]["projectPath"]
		if os.path.isdir(project_path)==False:
			self.display_error_function("Impossible to access that project!\nUnexisting path!")
			return
		else:
			#get settings function
			self.current_project_settings = self.load_project_settings_function(project_path)

			if self.current_project_settings != None:
				return [project_name,project_path]
			else:
				return False

				





	def load_project_settings_function(self, path):
		try:
			with open(os.path.join(path, "PipoManagerData/PipelineSettings.json"), "r") as read_settings:
				content = json.load(read_settings)
			self.display_message_function("Project settings loaded - %s"%path)
		except:
			#self.add_log_function("Impossible to load project settings - %s"%path)
			self.display_error_function("Impossible to load project settings!")
			return None
		else:
			self.display_message_function("Project settings loaded!")
			return content







	def save_personnal_data(self):
		with open("Data/PipoPersonnalData.json", "w") as save_file:
			json.dump(self.personnal_data, save_file, indent=4)
		self.display_message_function("Personnal settings updated!")






	def letter_verification_function(self, content):
		letter = list("abcdefghijklmnopqrstuvwxyz")
		capital_letter = list(letter.upper())
		splited_content = list(content)

		for i in range(0, len(splited_content)):
			if (splited_content[i] in letter) or (splited_content[i] in capital_letter) or (splited_content[i].isdigit()):
				return True

		return False






<<<<<<< HEAD
	def search_files_function(self):
		self.display_message_function("")
		self.display_message_function("============================================= SEARCHING =============================================")


		#TRY TO TERMINATE PREVIOUS PROCESSES
		if len(self.screen.searching_process_list) != 0:
			for process in self.screen.searching_process_list:
				process.terminate()
				self.display_message_function("PROCESS TERMINATED : %s"%process)
		else:
			self.display_message_function("NO PROCESS TO END!")
		"""
		for the kind selected get data in current project settings
		"""
		default_folder_list = []
		new_name_list_content = []

		searching_folder_data = {}

		self.display_message_function(self.name_kind_selection)
		for kind in self.name_kind_selection:
			
			try:
				kind_data = self.app.current_project_settings["Scenes"][kind]
			except:
				self.display_error_function("Impossible to get data from kind : %s"%kind)
				continue 
			else:
				#self.display_message_function("hello world!")
				#define the name list for that kind and add it to the new content
				#get the default folder from kind and remove after [name] IF NAME
				kind_default_folder_list = kind_data["folder"]

				for kind_default_folder in kind_default_folder_list:
					self.display_message_function("Default folder for %s : %s"%(kind, kind_default_folder))


					#GET THE NAME LIST
					if "[name]" in kind_default_folder.split("/"):
						index = kind_default_folder.split("/").index("[name]")
						new_list = kind_default_folder.split("/")[:index]

						name_folder_path = self.get_path_from_default_folder_function(kind, "/".join(new_list))
						if os.path.isdir(name_folder_path)==True:
							name_folder_list = os.listdir(name_folder_path)
							for name_folder in name_folder_list:
								if os.path.isdir(os.path.join(name_folder_path, name_folder))==True:
									new_name_list_content.append(name_folder)
						else:
							self.display_error_function("Impossible to get name folder for that kind : %s"%kind)

					else:
						new_name_list_content = [None]
					

					#if name, type, state, or lod list are empty fill values with str(None)
					if len(self.name_name_selection) == 0:
						self.name_name_selection = [None]
					if len(self.name_type_selection) == 0:
						self.name_type_selection = [None]

					#FOR EACH NAME TRY TO GET THE END OF THE PATH
					for name_selected in self.name_name_selection:
						#self.display_message_function("searching folder for %s"%name_selected)
						
						#FOR EACH TYPE TRY TO GET THE END OF THE PATH
						for type_selected in self.name_type_selection:
							state_list = self.app.current_project_settings["Global"]["stateList"] if self.app.current_project_settings["Global"]["stateList"] != [] else [None]
							lod_list = self.app.current_project_settings["Global"]["lodList"] if self.app.current_project_settings["Global"]["lodList"] != [] else [None]


							for lod in lod_list:
								for state in state_list:
									#self.display_message_function(name_selected)
									searching_path = self.get_path_from_default_folder_function(kind, kind_default_folder, name_selected, None, None, type_selected, state, lod)
									self.display_message_function("Searching path %s : %s"%(os.path.isdir(searching_path), searching_path))
									#if the folder exists add it to the searching queue data
									if (os.path.isdir(searching_path) == True) and (searching_path not in searching_folder_data):
											searching_folder_data[searching_path] = {
												"KIND":kind,
												"NAME":name_selected,
												"TYPE":type_selected,
												"LOD":lod,
												"STATE":state
											}

		
		#LAUNCH MULTIPROCESSING
		self.searching_app = PipoSearchingApplication()
		

		self.display_message_function(self.name_name_selection)


		


		if ( len(self.name_name_selection) != 0) and (self.name_name_selection != [None]):



			for folder_name, folder_data in searching_folder_data.items():


				process = multiprocessing.Process(target=self.searching_app.get_folder_function, args=(self.screen.final_files_dictionnary, folder_name, folder_data, self.app.current_project_settings,))
				#self.display_message_function("PROCESS STARTED : %s"%process)
				process.start()
				#add new processes to process list
				self.screen.searching_process_list.append(process)
				self.display_message_function("PROCESS %s ADDED TO LIST : [%s]"%(process, folder_name))
		else:
			self.display_message_function("No name selected so no process launched!")



		

		self.display_message_function("%s : %s"%(self.name_name_list, new_name_list_content))
		#return
		#check if the name list is different than the previous one
		#if yes replace the name list in lists
		if self.name_name_list != new_name_list_content:
			self.name_name_list = new_name_list_content
			self.lobby_name_list.clear_options()

			for i in range(len(self.name_name_list)):
				if self.name_name_list[i] != None:
					self.lobby_name_list.add_option(Selection(str(self.name_name_list[i]), i))
		#self.display_message_function(new_name_list_content)
=======




							
>>>>>>> 6ee8f77d51a475f0e20757bbc382914487e8cb9a






<<<<<<< HEAD




	def get_path_from_default_folder_function(self, kind=None, default_path=None, name_selection=None, shot_selection=None, sequence_selection=None, type_selection=None, state=None, lod=None):
		path = default_path.split("/")

		#self.display_message_function("GET FOLDER FOR %s / %s: %s"%(kind, name_selection, default_path))
		for i in range(len(path)):
			if path[i] == "[Origin]":
				path[i] = self.app.project_path
			elif path[i] == "[key]":
				path[i] = self.app.current_project_settings["Scenes"][kind]["keyword"]
			elif path[i] == "[mayaProject]":
				path[i] = self.app.current_project_settings["Global"]["mayaFolder"]
			elif path[i] == "[type]":
				path[i] =(type_selection)
			elif path[i] == "[state]":
				path[i] = (state)
			elif path[i] == "[lod]":
				path[i] = (lod)
			elif path[i] == "[name]":
				path[i] = (name_selection)

			else:
				pass

		


		#try to find None values in the list
		#if there is delete all values after the first None value
		if None in path:
			none_index = path.index(None)
			path = path[:none_index]
			#self.display_message_function(path)
		return "/".join(path)
		#self.display_message_function("%s : %s"%(os.path.isdir(final_path), final_path))



=======
>>>>>>> 6ee8f77d51a475f0e20757bbc382914487e8cb9a


							



