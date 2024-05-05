import os
import sys
import scandir

from time import sleep


class PipoSearchingApplication:



	def get_folder_function(self, folder_name, folder_data, project_settings):
		print("FILES FOUND")
		for root, dirs, files in scandir.walk(folder_name):
			for file in files:
				print(file)

