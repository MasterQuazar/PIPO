import os
import json
import socket 
import copy

#c:/users/metal/onedrive/bureau/testproject
from textual.app import App, ComposeResult
from textual.widgets import Label,Button, Static, ListView, ListItem, OptionList, Header, Footer
from textual.screen import Screen 
from textual.widgets.selection_list import Selection
from textual.widgets.option_list import Option
from textual import events
from textual.containers import Horizontal, Vertical, Container, VerticalScroll
from pyfiglet import Figlet 
from time import sleep
from random import randrange 
from datetime import datetime
from multiprocessing import Manager

from collections import Counter

import scandir
import threading
import multiprocessing
import getpass
import pygetwindow as pg


from Modules.PipoResearch import PipoSearchingApplication



class PipoSearchFilesApplication():
	def test_function(self):
		self.notify("hello world", timeout=5)





class PipoCommonApplication():





	def get_scene_data_function(self, maya_scene_path):
		maya_path = None
		if os.path.isfile(os.path.join(self.app.personnal_data["MayaScriptPath"], "scripts/pipoConnectionLog.json"))==True:
				maya_path =self.app.personnal_data["MayaScriptPath"]
		elif os.path.isfile(os.path.join(self.app.personnal_data["MayaProgramPath"], "scripts/pipoConnectionLog.json"))==True:
			maya_path = self.app.personnal_data["MayaProgramPath"]

		if maya_path != None:
			#get connection port
			try:
				with open(os.path.join(maya_path, "scripts/pipoConnectionLog.json"), "r") as read:
					connection_log = json.load(read)
			except:
				self.display_error_function("Impossible to load Connection log!")
				return
			else:
				found = False
				for index, data in connection_log.items():
					self.display_message_function("%s : %s"%(maya_scene_path, data["filename"]))
					if data["filename"] == maya_scene_path:
						found=True
						break

				if found != False:
					return data






	def send_command_function(self, command, server, display = "show"):
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect(server)

		except Exception as e:
			self.display_message_function("Impossible to connect to server : %s"% str(server)) 
			self.display_message_function(e)
			return None

		else:
			#test = "print('hello world')"
			try:
				sock.sendall(command.encode("utf-8"))
				answer = sock.recv(4096).decode("utf-8").replace("\x00", "").strip()
				#self.display_message_function("answer : %s"%answer)
			
				
			except Exception as e:
				self.display_message_function("Impossible to send command")
				self.display_message_function(e)
				return False
			else:

				
				if display== "show":
					self.display_message_function("%s | Command sent : %s"%(server, command))
					


				return answer








	def update_maya_scene_list_function(self):
		
		#self.display_message_function("maya checking started! : %s"%maya_path)
		"""
		get opened maya scenes
		list them in the lobby list
		update the connection log file in the maya path with the right maya scene 
				--> TRY A PING?
		"""

		#maya_window_list = pg.getWindowsWithTitle("Autodesk MAYA")
		#try to assign the name of the maya scenes to connection log items
		#get the maya path


		
		while True:
			maya_window_list = pg.getWindowsWithTitle("Autodesk MAYA")
			maya_window_list_name = []
			for maya in maya_window_list:

				#try to get only the filepath in the maya filename
				#quite an tough parsing to do!
				maya_filepath = (maya.title.split("---")[0]).split(" ")

				maya_window_list_name.append([item for item in maya_filepath if item != ""][-1].replace("\\", "/"))


			#try to assign to each maya path in connection log a name instead of index!
			#try to ping the scene and to get the port opened
			maya_path = None

			if os.path.isfile(os.path.join(self.app.personnal_data["MayaScriptPath"], "scripts/pipoConnectionLog.json"))==True:
				maya_path =self.app.personnal_data["MayaScriptPath"]
			elif os.path.isfile(os.path.join(self.app.personnal_data["MayaProgramPath"], "scripts/pipoConnectionLog.json"))==True:
				maya_path = self.app.personnal_data["MayaProgramPath"]


			if maya_path != None:
				#self.display_message_function("connection log exists!")

				try:
					with open(os.path.join(maya_path, "scripts/pipoConnectionLog.json"), "r") as read_file:
						connection_log = json.load(read_file)
					#self.display_message_function("opened")
				except:
					self.display_message_function("Impossible to read log")
					
				else:
					#self.display_message_function("try connection")


					#changes = False
					connection_log_copy = copy.deepcopy(connection_log)
					to_remove = []

					try:

						"""
						if the filename value of the dictionnary == None
						or if the filename is different
							-> update the value and save the new dictionnary
						"""
						
						for index, data in connection_log.items():
							
							#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
							#self.display_message_function("%s : %s"%(key, value))
							#PING THE SCENE AND ASK FOR THE PORT OPENED
							try:
								#sock.connect(server_adress)

								#self.display_message_function("connected")
								command = 'cmds.file(q=True, sn=True)'
								server = ("localhost", data["port"])
								output = self.send_command_function(command, server, "hide")
								#self.display_message_function("output : %s"%output)
								if output == None:
									#remove the connexion port from the connection log
									to_remove.append(index)
								elif output != False:
									#self.display_message_function("%s : %s"%(os.path.isfile(output), output))
									if os.path.isfile(output)==True:
										#connection_log[output] = connection_log.pop(index)
										#change the value of the current dictionnary item
										connection_log[index] = {
											"port":data["port"],
											"filename":output,
										}
										#self.display_message_function("value changed")

										
							except Exception as e:
								self.display_message_function(e)
					except Exception as e:
						self.display_message_function(e)


					remove_connexion = False
					for remove in to_remove:
						
						del connection_log[remove]
						self.display_message_function("Connexion removed : %s"%str(server))
						remove_connexion=True
					
					
					#check if the new dictionnary is different
					#if old_connection_log != connection_log:
					#save the new connection log in file

					if (connection_log_copy!=connection_log) or (remove_connexion == True):

						try:
							with open(os.path.join(maya_path, "scripts/PipoConnectionLog.json"), "w") as save_file:
								json.dump(connection_log, save_file, indent=4)
							
						except Exception as e:
							self.display_error_function("Impossible to save new connection log")
							self.display_error_function(e)

						else:
							self.display_message_function("Connection log saved!")
					
			else:
				self.display_message_function("doesn't exists!")

			#if the two lists are different update the list*
			#use set to check if both containers are identical even if
			#items are not in the same order

			
			if set(maya_window_list_name) != set(self.opened_maya_scene_list):
				#self.display_message_function("DIFFERENCE")
				#self.display_message_function("old : %s"%self.opened_maya_scene_list)
				#self.display_message_function("new : %s"%maya_window_list_name)
				self.opened_maya_scene_list = maya_window_list_name.copy()





				self.screen.maya_scene_list.clear_options()
				for i in range(len(self.opened_maya_scene_list)):
					self.screen.maya_scene_list.add_option(Selection(self.opened_maya_scene_list[i],i))
		




			sleep(2)
		





	def check_for_autorun_function(self):
		"""
		check if the maya path exists (maya script path)
		-> if the path exists try to create the autorun in it
		-> if the path doesn't exists don't fill the personnal settings file
		"""
		if (self.personnal_data["MayaScriptPath"] == None) or (os.path.isdir(self.personnal_data["MayaScriptPath"]) == False):
			self.display_error_function("Wrong maya path in personnal settings!\nImpossible to put the maya autorun!")
		elif os.path.isfile(os.path.join(self.personnal_data["MayaScriptPath"],"scripts/userSetup.py"))==True:
			self.display_message_function("User setup file detected in maya script path!")
		else:
			#create autorun file
			autorun_code = '''



#PIPO AUTORUN FOR MAYA
import os
import uuid
import maya.cmds as mc
import json
import socket

from time import sleep
from random import randrange



def try_socket_connection(host,port):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as co:
		co.settimeout(1)

		try:
			co.connect((host, port))
			return True
		except (socket.timeout, socket.error):
			return False


while True:
	port_number = randrange(49152, 65535)

	try:
		mc.commandPort(name=":%s"%port_number, sourceType="python")
	except:
		print("Impossible to open an outside connection for Pipo : %s"%port_number)
		#sleep(1)
		break
	else:
		print("Outside connection established with Pipo : %s"%port_number)
		print("Path of the connection Log File : %s"%(os.path.join(os.getcwd(), "scripts/pipoConnectionLog.json")))
		

		try:
			#save the command port in a json file
			with open(os.path.join(os.getcwd(), "scripts/pipoConnectionLog.json"), "r") as read_file:
				content = json.load(read_file)
		except:
			content = {}
		else:
			if type(content) != dict:
				content = {}
			else:
				key_to_remove = []
				#go through the whole dictionnary and delete connections that are not opened
				for key, value in content.items():
					co_value = try_socket_connection("localhost", value["port"])
					if co_value == False:
						key_to_remove.append(key)

				for key in key_to_remove:
					del content[key]

		len_dictionnary = len(list(content.keys()))
		content[len_dictionnary+1] = {
			"filename":None,
			"port":port_number
			}

		with open(os.path.join(os.getcwd(), "scripts/pipoConnectionLog.json"), "w") as save_file:
			json.dump(content, save_file, indent=4)
		print("Connection json updated")
		break







'''
			with open(os.path.join(self.personnal_data["MayaPath"], "scripts/userSetup.py"), "w") as save_file:
				save_file.write(autorun_code)
			self.display_message_function("Pipo autorun created!")





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
			self.display_message_function("Personnal settings created")
		else:
			self.display_message_function("trying to load settings")
			try:
				with open("Data/PipoPersonnalData.json", "r") as read_data:
					self.personnal_data = json.load(read_data)
			except:
				#display error
				self.display_error_function("Impossible to read personnal settings file")
				self.personnal_data = self.create_personnal_settings_file_function()
				self.display_message_function("Personnal settings created")
			else:
				self.display_message_function("Personnal settings opened")







	def create_personnal_settings_file_function(self):
		#create the personnal settings dictionnary
		personnal_dictionnary = {
			"MayaPath":None,
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
					self.login_project_list.add_option(Option(project_name))
					self.display_message_function("Project created successfully!")

		#self.login_alert_label.update("%s ; %s"%(project_name, project_path))





	def open_project_function(self):
		#get the current value selected in textscrolllist
		
		#FOR OPTION LIST
		project_list = self.query_one("#login_projectlist", OptionList)
		#current_option = project_selection.get_option_at_index(project_selection.highlighted)
		current_option_index = project_list.highlighted
		#current_content = project_selection.get_option_at_index(current_option_index)
		try:
			project_name = list(self.personnal_data["ProjectList"].keys())[current_option_index]
		except TypeError:
			self.display_error_function("You have to select a project first!")
			return

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
		self.display_message_function("")
		self.display_message_function("============================================= SEARCHING =============================================")


		#TRY TO TERMINATE PREVIOUS PROCESSES
		if len(self.screen.searching_process_list) != 0:
			for process in self.screen.searching_process_list:
				process.terminate()
				self.display_message_function("PROCESS TERMINATED : %s"%process)
		else:
			self.display_message_function("NO PROCESS TO END!")



		#CLEAN THE FILE QUEUE
		while not self.app.final_file_queue.empty():
			self.app.final_file_queue.get()


		"""
		for the kind selected get data in current project settings
		"""
		default_folder_list = []

		new_name_list_content = []
		new_sequence_list_content = []
		new_shot_list_content = []

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



					if "[sqversion]" in kind_default_folder.split("/"):
						sequence_index = kind_default_folder.split("/").index("[sqversion]")
						sequence_folder = kind_default_folder.split("/")[:sequence_index]

						sequence_folder_path = self.get_path_from_default_folder_function(kind, "/".join(sequence_folder))

						self.display_message_function(sequence_folder_path)
						if os.path.isdir(sequence_folder_path)==True:
							sequence_folder_list = os.listdir(sequence_folder_path)

							for sequence_folder in sequence_folder_list:
								if os.path.isdir(os.path.join(sequence_folder_path, sequence_folder))==True:
									#self.display_message_function("sequence folder : %s"%sequence_folder)
									new_sequence_list_content.append(sequence_folder)
						else:
							self.display_error_function("Impossible to get the sequence folder!")
					else:
						new_sequence_list_content = [None]


				
						



					
					self.display_message_function(self.name_sequence_selection)


					"""
					#if name, type, state, or lod list are empty fill values with str(None)
					if len(self.name_sequence_selection) != 0:			
						for sequence in self.name_sequence_selection:
							self.display_message_function("searching sequence : %s"%sequence)
							if "[shversion]" in kind_default_folder.split("/"):
								shot_index = kind_default_folder.split("/").index("[shversion]")
								shot_folder= kind_default_folder.split("/")[:shot_index]

								shot_folder_path = self.get_path_from_default_folder_function(kind, "/".join(shot_folder), None, None, sequence)

								self.display_message_function(shot_folder_path)
					else:
						self.name_sequence_selection = [None]
					"""
					if len(self.name_sequence_selection) != 0:
						for sequence in self.name_sequence_selection:
							if "[shversion]" in kind_default_folder.split("/"):
								shot_index = kind_default_folder.split("/").index("[shversion]")
								shot_folder = kind_default_folder.split("/")[:shot_index]

								shot_folder_path = self.get_path_from_default_folder_function(kind, "/".join(shot_folder), None, sequence)
								
								if os.path.isdir(shot_folder_path) == True:
									shot_folder_content = os.listdir(shot_folder_path)

									for shot_content in shot_folder_content:
										if os.path.isdir(os.path.join(shot_folder_path, shot_content))==True:
											new_shot_list_content.append(shot_content)
								else:
									self.display_error_function("Impossible to get shots folder!")
							else:
								new_shot_list_content = [None]






								
					if len(self.name_shots_selection) == 0:
						self.name_shots_selection = [None]

					if len(self.name_sequence_selection) == 0:
						self.name_sequence_selection = [None]

					#self.display_message_function("SHOTS : %s"%self.name_shots_selection)
					if len(self.name_name_selection) == 0:
						self.name_name_selection = [None]

					if len(self.name_type_selection) == 0:
						self.name_type_selection = [None]

					#FOR EACH NAME TRY TO GET THE END OF THE PATH
					for name_selected in self.name_name_selection:
						#self.display_message_function("searching folder for %s"%name_selected)
						for sequence_selected in self.name_sequence_selection:
							for shot_selected in self.name_shots_selection:
								#FOR EACH TYPE TRY TO GET THE END OF THE PATH
								for type_selected in self.name_type_selection:
									state_list = self.app.current_project_settings["Global"]["stateList"] if self.app.current_project_settings["Global"]["stateList"] != [] else [None]
									lod_list = self.app.current_project_settings["Global"]["lodList"] if self.app.current_project_settings["Global"]["lodList"] != [] else [None]


									for lod in lod_list:
										for state in state_list:
											#self.display_message_function(name_selected)
											searching_path = self.get_path_from_default_folder_function(kind, kind_default_folder, name_selected, sequence_selected, shot_selected, type_selected, state, lod)
											#self.display_message_function("Searching path %s : %s"%(os.path.isdir(searching_path), searching_path))
											#if the folder exists add it to the searching queue data
											if (os.path.isdir(searching_path) == True) and (searching_path not in searching_folder_data):
													#self.display_message_function(searching_path)
													searching_folder_data[searching_path] = {
														"KIND":kind,
														"NAME":name_selected,
														"SEQUENCE":sequence_selected,
														"SHOT":shot_selected,
														"TYPE":type_selected,
														"LOD":lod,
														"STATE":state
													}

		
		#LAUNCH MULTIPROCESSING
		self.searching_app = PipoSearchingApplication()
		

		#self.display_message_function(self.name_name_selection)


		
		self.display_message_function(searching_folder_data)
		if searching_folder_data != {}:
		#if ( len(self.name_name_selection) != 0) and (self.name_name_selection != [None]):


		


			for folder_name, folder_data in searching_folder_data.items():
				+0


				process = multiprocessing.Process(target=self.searching_app.get_folder_function, args=(self.app.final_file_queue, folder_name, folder_data, self.app.current_project_settings,))
				#self.display_message_function("PROCESS STARTED : %s"%process)
				process.start()
				#add new processes to process list
				self.screen.searching_process_list.append(process)
				self.display_message_function("PROCESS %s ADDED TO LIST : [%s]"%(process, folder_name))


			for process in self.screen.searching_process_list:
				process.join()


			if self.app.final_file_queue.empty() == False:
				self.app.final_file_list = []
				self.display_message_function("file list cleaned")

				#self.display_message_function("FINAL QUEUE CONTENT : ")
				while not self.app.final_file_queue.empty():
					self.app.final_file_list.append(self.app.final_file_queue.get())
					self.display_message_function("element added")

				self.display_message_function(self.app.final_file_list)
					#self.display_message_function(self.app.final_file_queue.get(block=False))
			else:
				self.display_message_function("NO FILES FOUND!")
		else:
			self.display_message_function("No name selected so no process launched!")

		
		

		#self.display_message_function("%s : %s"%(self.name_name_list, new_name_list_content))
		#return
		#check if the name list is different than the previous one
		#if yes replace the name list in lists


		
		if self.name_sequence_list != new_sequence_list_content:
			self.name_sequence_list = new_sequence_list_content
			

			try:
				self.lobby_sequence_list.clear_options()
				for i in range(len(self.name_sequence_list)):
					if self.name_sequence_list[i] != None:
						self.lobby_sequence_list.add_option(Selection(str(self.name_sequence_list[i]), i))
			except:
				self.display_error_function("Impossible to update sequence list in lobby")

		if self.name_shots_list != new_shot_list_content:
			self.name_shots_list = new_shot_list_content

			try:
				self.lobby_shot_list.clear_options()
				for i in range(len(self.name_shots_list)):
					if self.name_shots_list[i] != None:
						self.lobby_shot_list.add_option(Selection(str(self.name_shots_list[i]), i))	
			except:
				self.display_error_function("Impossible to update shot list in lobby")

		if self.name_name_list != new_name_list_content:
			self.name_name_list = new_name_list_content
			self.lobby_name_list.clear_options()

			try:
				self.lobby_name_list.clear_options()
				for i in range(len(self.name_name_list)):
					if self.name_name_list[i] != None:
						self.lobby_name_list.add_option(Selection(str(self.name_name_list[i]), i))
			except:
				self.display_error_function("Impossible to update name list in lobby")

		
		#self.display_message_function(new_name_list_content)





							












	def get_path_from_default_folder_function(self, kind=None, default_path=None, name_selection=None, sequence_selection=None, shot_selection=None, type_selection=None, state=None, lod=None):
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
			elif path[i] == "[sqversion]": 
				path[i] = sequence_selection
			elif path[i] == "[shversion]":
				path[i] = shot_selection

			else:
				pass

		


		#try to find None values in the list
		#if there is delete all values after the first None value
		if (None in path):
			none_index = path.index(None)
			path = path[:none_index]
			#self.display_message_function(path)
		return "/".join(path)
		#self.display_message_function("%s : %s"%(os.path.isdir(final_path), final_path))






							



