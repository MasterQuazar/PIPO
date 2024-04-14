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



class PipoCommonApplication():
	
	"""
	def __init__(self):
		super().__init__()

		self.program_path = os.getcwd()
		self.program_log = []
		self.program_log_copy = []
	"""
		#self.current_project_settings = {}
		





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





	def search_files_function(self):
		self.display_message_function("Searching...")
		
		if len(self.screen.name_type_selection) == 0:
			self.screen.name_type_selection = [None]
		if len(self.screen.name_name_selection) == 0:
			self.screen.name_name_selection = [None]
		
		if len(self.screen.name_kind_selection) != 0:

			default_folder_list = []
		
			for kind in self.screen.name_kind_selection:
				default_folder_list = self.app.current_project_settings["Scenes"][kind]["folder"]

				for default_folder in default_folder_list:

					#self.get_default_folder_path_function(default_folder, kind)
					for n in self.screen.name_name_selection:
						for t in self.screen.name_type_selection:
							for state in self.app.current_project_settings["Global"]["stateList"]:
								for lod in self.app.current_project_settings["Global"]["lodList"]:
									default_folder_path = self.get_default_folder_path_function(default_folder, kind, n, t, lod, state)
									if os.path.isdir(default_folder_path) == True:
										self.display_message_function("added")
										default_folder_list.append(default_folder_path)
									#self.display_message_function(default_folder_path)
					"""	
					for n in self.screen.name_name_selection:
						for t in self.screen.name_type_selection:
							for state in self.app.current_project_settings["Global"]["stateList"]:
								for lod in self.app.current_project_settings["Global"]["lodList"]:
									default_folder_path = self.get_default_folder_path_function(default_folder, kind, n, t, lod, state)
					"""
				
		





	def get_default_folder_path_function(self, default_folder = None, k=None, n=None,t=None, lod=None, state=None):
		splited_default_folder = default_folder.split("/")
		final_default_folder = []


		for item in splited_default_folder:
			if item == "[Origin]":
				final_default_folder.append(self.app.project_path)
			elif item == "[mayaProject]":
				final_default_folder.append(self.app.current_project_settings["Global"]["mayaFolder"])
			elif item == "[name]":
				if n == None:
					#self.display_message_function("limit reached : name")
					return "/".join(final_default_folder)
				final_default_folder.append(str(n))
			elif item == "[type]":
				if t == None:
					#self.display_error_function("limit reached : type")
					return "/".join(final_default_folder)
				final_default_folder.append(str(t))
			elif item == "[lod]":
				final_default_folder.append("LOD%s"%str(lod))
			elif item == "[state]":
				final_default_folder.append(str(state))
			elif item == "[key]":
				if k == None:
					#self.display_message_function("limit reached : key")
					return "/".join(final_default_folder)
				final_default_folder.append(str(k))
			else:
				final_default_folder.append(item)
		final_default_folder_path = "/".join(final_default_folder)
		#self.display_message_function(final_default_folder_path)
		return final_default_folder_path


		







	def get_shared_values(*data):
		if not data:
			return []
		intersection = set(data[0])
		for item in data[1:]:
			intersection = intersection.intersection(set(item))
		return list(intersection)