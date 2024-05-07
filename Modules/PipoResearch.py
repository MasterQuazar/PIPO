import os
import sys
import scandir

from time import sleep


class PipoSearchingApplication:



	def get_folder_function(self, folder_name, folder_data, project_settings):
		print("FILES FOUND")

		kind_settings = project_settings["Scenes"][folder_data["KIND"]]

		found_file_list = {}

		for root, dirs, files in scandir.walk(folder_name):
			for file in files:
				

				filename, extension = os.path.splitext(file)

				#print(extension, filename)
				if extension not in project_settings["Global"]["3dScenesExtension"]:
					continue

				else:
					#CHECK THE LENGHT OF THE SPLITED FILE FOR THE GIVEN KIND
					splited_filename = filename.split("_")
					splited_nomenclature = kind_settings["syntax"].split("_")
					self.save_log_function("%s ; %s"%(splited_filename, splited_nomenclature))

					

		#sleep(5)




	def save_log_function(self, message):
		with open(os.path.join(os.getcwd(), "data/logs/logs_searching.dll"), "a") as save_log:
			save_log.write(str(message)+"\n")
