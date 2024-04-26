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






class PipoSearchFilesApplication():
	def test_function(self, text):
		self.display_message_function("message is : %s"%text)




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
		self.display_message_function("####################################################")
		self.display_message_function("Searching...")
		self.display_message_function("####################################################")
		
		if len(self.screen.name_type_selection) == 0:
			self.screen.name_type_selection = [None]
		if len(self.screen.name_name_selection) == 0:
			self.screen.name_name_selection = [None]
		
		#self.display_message_function(self.screen.name_name_selection)
		#self.display_message_function(self.screen.name_type_selection)
		temporary_name_list = []

		

			

		#DEFINE THE DEFAULT FOLDER PATH WITH CURRENT PROJECT SETTINGS FOR EACH TYPE SELECTED
		if len(self.screen.name_kind_selection) != 0:

			default_folder_list = []
			default_folder_path_list = {}
			
			#self.display_message_function
		
			for kind in self.screen.name_kind_selection:
				default_folder_list = self.app.current_project_settings["Scenes"][kind]["folder"]

				for default_folder in default_folder_list:
					for status in self.app.current_project_settings["Global"]["stateList"]:
						#self.get_default_folder_path_function(default_folder, kind)
						for n in self.screen.name_name_selection:
							for t in self.screen.name_type_selection:
								for s in self.app.current_project_settings["Global"]["stateList"]:
									for l in self.app.current_project_settings["Global"]["lodList"]:
										#self.display_message_function(status)
										
										default_folder_data = self.get_default_folder_path_function(default_folder, kind, n, s, l, t,)
										#self.display_message_function(default_folder_data[0]["path"])
										#from default folder function
										# 1 - data dictionnary
										# 2 - name list ?
										if (os.path.isdir(default_folder_data[0]["path"])==True) and (default_folder_data[0]["path"] not in default_folder_path_list):
											default_folder_path_list[default_folder_data[0]["path"]] = default_folder_data[0]

											for name in default_folder_data[1]:
												if name not in temporary_name_list:
													temporary_name_list.append(name)

									
			#check if the thread is still valid
			if self.searching_event.is_set():
				self.display_message_function("Main searching thread terminated")
				return None

			
			#DEFINE THE CONTENT LIST FOR EACH DEFAULT FOLDER
			"""
			for default_folder, default_folder_values in default_folder_path_list.items():
				#self.display_message_function(default_folder)
				#create a new thread trying to get the content of each default folder
			
				searching_thread = threading.Thread(target=self.get_folder_content_function, args=(default_folder_values,), daemon=True)
				searching_thread.start()
			"""
			self.thread_list = []
			self.thread_number = 10
			self.thread_count = 0

			for i in range(self.thread_number):
				x = threading.Thread(target=self.test_thread_function, args=(i, randrange(20,50),), daemon=True)
				x.start()
				self.display_message_function("thread %s started"%i)
				self.thread_list.append(x)
			

			

			"""
			while True:
				self.display_message_function("%s / %s"%(self.thread_count, self.thread_number))
				sleep(1)
			"""


		return
		#self.display_message_function(default_folder_list)
		#NEED TO CHANGE THE LIST IF THE KEY HAS CHANGED!!!
		if (self.name_name_list != temporary_name_list) and (self.screen.kind_change_list != self.screen.name_kind_selection):
			self.name_name_list = temporary_name_list
			self.name_name_selection = []	

			self.screen.kind_change_list = copy.copy(self.screen.name_kind_selection)
			self.screen.lobby_name_list.clear_options()

			for i in range(len(temporary_name_list)):
				self.screen.lobby_name_list.add_option(Selection(temporary_name_list[i],i)) 




	def test_thread_function(self,i, duration):
		for y in range(duration):

			if self.searching_event.is_set():
				break
			self.display_message_function("thread : %s"%y)
			sleep(1)
		self.display_message_function("thread %s DONE!"%i)
		self.thread_count += 1
		




	def get_folder_content_function(self, folder_data):
		self.display_message_function("Searching folder content : %s"%folder_data["path"])

		kind = folder_data["kind"]

		nomenclature = self.app.current_project_settings["Scenes"][kind]["syntax"]
		splited_nomenclature = nomenclature.split("_")

		keyword = self.app.current_project_settings["Scenes"][kind]["keyword"]
		type_list = self.app.current_project_settings["Scenes"][kind]["type"]


		final_folder_content_list = []


		for root, dirs, files in scandir.walk(folder_data["path"]):
			for f in files:
				filepath = os.path.join(root,f)
				filename, extension = os.path.splitext(f)
				splited_filename = filename.split("_")

				if (extension in self.app.current_project_settings["Global"]["3dScenesExtension"]) or (extension in self.app.current_project_settings["Global"]["3dItemsExtension"]):

					#self.display_message_function("%s - %s"%(splited_filename, splited_nomenclature))
					if len(splited_filename) == len(splited_nomenclature):
						self.display_message_function("checking file : %s"%f)
						parsing_error = False 

						for i in range(len(splited_filename)):


							self.display_message_function(splited_filename[i])
							
							#self.display_message_function("checking %s"%splited_filename[i])
							if splited_nomenclature[i] == "[key]":
								if splited_filename[i] != self.app.current_project_settings["Scenes"][kind]["keyword"]:
									self.display_message_function("kind error")
									parsing_error=True
									break

							elif splited_nomenclature[i] == "[type]":
								if splited_filename[i] not in type_list:
									parsing_error=True 
									self.display_message_function("type error")
									break
							elif splited_nomenclature[i] == "[lod]":
								if splited_filename[i] not in self.app.current_project_settings["Global"]["lodList"]:
									parsing_error=True 
									self.display_message_function("lod error")
									break

							#for sh and sq version check prefix and number version
							elif splited_nomenclature[i] in ["[sqversion]", "[shversion]"]:
								if splited_nomenclature[i] == "[sqversion]":
									splited_content = splited_filename[i].split("sq")
									type_keyword = "sq"
								
								else:
									splited_content = splited_filename[i].split("sh")
									type_keyword = "sh"

								if (len(splited_seq) != 2) or (splited_seq[0] != "") or (splited_seq[1].isdigit() == False):
									parsing_error=True

									self.display_message_function("sq sh version error")
									break


							elif splited_nomenclature[i] == "[name]":
								continue 

							elif splited_nomenclature[i] == "[version]":
								splited_content = splited_filename[i].split("v")

								if (len(splited_content) != 2) or (splited_content[0] != "") or (splited_content[1].isdigit()==False):
									parsing_error=True 
									self.display_message_function("version error")
									break


							else:
								if splited_nomenclature[i] != splited_filename[i]:
									self.display_message_function("not matching informations in nomenclature")
									parsing_error=True
									break






							"""
							elif splited_nomenclature[i] == "[version]":
								splited_content = splited_filename.split("v")

								if (len(splited_content) != 2) or (splited_content[0] != "") or (splited_content[1].isdigit()==False):
									parsing_error=True 
									self.display_message_function("version error")


							
							"""
						if parsing_error == False:
							final_folder_content_list.append(os.path.join(root, f))





							






	def get_default_folder_path_function(self, default_folder = None, k=None, n=None, s=None, l=None, t=None):
		folder_dictionnary_data = {}

		splited_default_folder = default_folder.split("/")
		final_default_folder = []
		folder_name_list = []
		#change_name = True

		#self.display_message_function("Searching default folder path")

		for item in splited_default_folder:
			if item == "[Origin]":
				final_default_folder.append(self.app.project_path)
			elif item == "[key]":
				final_default_folder.append(self.app.current_project_settings["Scenes"][k]["keyword"])
				folder_dictionnary_data["kind"] = k




			elif item == "[name]":
				if n == None:
					#get the current path
					#check if the path exists
					#get the list of folder name inside of that path
					name_folder_path = "/".join(final_default_folder)
					#self.display_message_function("NAME FOLDER : %s"%name_folder_path)
					#self.display_message_function(os.path.isdir(name_folder_path))
					try:
						name_folder_content = os.listdir(name_folder_path)
					except:
						#self.display_error_function("Impossible to get the name list in folder")
						break
					else:
						for item in name_folder_content:
							if os.path.isdir(os.path.join(name_folder_path, item)) == True:
								folder_name_list.append(item)

					break
				else:
					folder_dictionnary_data["name"] = n
					#self.display_message_function("name added : %s"%n)
					final_default_folder.append(n)

			elif item == "[type]":
				if t == None:
					break
				else:
					folder_dictionnary_data["type"] = t
					final_default_folder.append(t)

			elif item == "[lod]":
				if l == None:
					break
				else:
					folder_dictionnary_data["lod"] = l
					final_default_folder.append(l)

			elif item == "[state]":
				if s == None:
					break
				else:
					folder_dictionnary_data["state"] = s
					final_default_folder.append(s)

			elif item == "[mayaProject]":
				final_default_folder.append(self.app.current_project_settings["Global"]["mayaFolder"])

			else:
				final_default_folder.append(item)


			if os.path.isdir("/".join(final_default_folder))==False:
				#if the folder isn't existing anymore
				#remove the last folder of the path 
				#so the path is true
				del final_default_folder[-1]
				break

		folder_dictionnary_data["path"] = "/".join(final_default_folder)
		return [folder_dictionnary_data, folder_name_list]

		







	def get_shared_values(*data):
		if not data:
			return []
		intersection = set(data[0])
		for item in data[1:]:
			intersection = intersection.intersection(set(item))
		return list(intersection)