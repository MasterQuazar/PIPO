import os
import sys
import scandir


from time import sleep


class PipoSearchingApplication:



	def get_folder_function(self, final_file_queue,folder_name, folder_data, project_settings):
		self.save_log_function("\n")
		

		self.save_log_function("SEARCHING DATA : ")
		for key, value in folder_data.items():
			self.save_log_function("%s : %s"%(key, value))


		kind_settings = project_settings["Scenes"][folder_data["KIND"]]

		found_file_list = {}
		error_list = []

		for root, dirs, files in scandir.walk(folder_name):
			for file in files:


				
				

				filename, extension = os.path.splitext(file)

				#print(extension, filename)
				if extension not in project_settings["Global"]["3dScenesExtension"]:
					continue

				else:

					self.save_log_function("CHECKING FILE : %s"%file)
					#CHECK THE LENGHT OF THE SPLITED FILE FOR THE GIVEN KIND
					splited_filename = filename.split("_")
					splited_nomenclature = kind_settings["syntax"].split("_")
					#self.save_log_function("%s ; %s"%(splited_filename, splited_nomenclature))

					if len(splited_nomenclature) != len(splited_filename):
						#file_parsing_error = True 
						continue
					else:

						#check each syntax element
						#first check if the key is in the syntax
						#if yes check if the key is matching before anything else!
						if "[key]" in splited_nomenclature:
							key_index = splited_nomenclature.index("[key]")
							if splited_filename[key_index] != kind_settings["keyword"]:
								self.save_log_function("Key isn't matching!")
								continue
						else:
							self.save_log_function("Key not in the syntax!")
				
					
						file_parsing_error = False
						self.save_log_function("Parsing the file...")
						#check other part of the nomenclature to see if it is matching!
						for i in range(len(splited_nomenclature)):
							#PASSING KIND
							#already checked before!
							if splited_nomenclature[i] == "[key]":
								continue

							#CHECKING VERSION
							elif splited_nomenclature[i] == "[version]":
								#split the filename item
								if splited_filename[i] != project_settings["Global"]["stateList"][1]:
									splited_version = splited_filename[i].split("v")
									if (len(splited_version) != 2) or (splited_version[0] != "") or (splited_version[1].isdigit()==False):
										file_parsing_error=True
										error_list.append("version")

							#CHECKING TYPE
							elif splited_nomenclature[i] == "[type]":
								#check that the type of the scene is in the settings 
								file_type = splited_filename[i]
								if file_type not in kind_settings["type"]:
									file_parsing_error=True
									error_list.append("type1")

								else:
									if folder_data["TYPE"] != None:
										#check that the type is also selected!
										if splited_filename[i] not in folder_data["TYPE"]:
											file_parsing_error=True 
											error_list.append("type2")

							#CHECKING NAME
							#no verification if name restriction isn't checked!
							elif splited_nomenclature[i] == "[name]":
								pass

							elif splited_nomenclature[i] == "[shversion]":
								splited_shot = splited_filename[i].split("sh")
								if (len(splited_shot) != 2) or (splited_shot[0] != "") or (splited_shot[1].isdigit()==False):
									error_list.append("shot")
									file_parsing_error=True 

							elif splited_nomenclature[i] == "[sqversion]":
								splited_sequence = splited_filename[i].split("sq")

								if (len(splited_sequence) != 2) or (splited_sequence[0] != "") or (splited_sequence[1].isdigit()==False):
									error_list.append("sequence")
									file_parsing_error=True


							#CHECKING LOD
							elif splited_nomenclature[i] == "[lod]":
								filename_lod = splited_filename[i].split("LOD")

								if (filename_lod[0] != "") or (filename_lod[1] not in project_settings["Global"]["lodList"]):
									error_list.append("lod")
									file_parsing_error=True

							#NOT ASSOSIATED WITH A SYNTAX KEYWORD
							#if the word is the same in the nomenclature than in the filename
							#no error
							else:
								if splited_nomenclature[i] != splited_filename[i]:
									file_parsing_error=True 
									error_list.append("nomenclature item")


						for error in error_list:
							self.save_log_function(error)


						if file_parsing_error==False:
							self.save_log_function("file returned : %s"%file)
							final_file_queue.put(os.path.join(root, file))



		return





	def save_log_function(self, message):
		with open(os.path.join(os.getcwd(), "data/logs/Logs_searching.dll"), "a") as save_log:
			save_log.write(str(message)+"\n")
