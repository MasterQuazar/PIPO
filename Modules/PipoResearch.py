import os
import sys
import scandir

from time import sleep


class PipoSearchingApplication:



	def get_folder_function(self, folder_name, folder_data, project_settings):
		print(folder_name)
		for key, value in folder_data.items():
			print(key, value)