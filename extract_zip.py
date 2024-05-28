#!/usr/bin/python3

import zipfile, os, sys

def extract_zip(zip_file, dict_file):

  #Check if the provided files exist (and is a zip file)
	if not os.path.isfile(zip_file):
		print(f"Error: The file '{zip_file}' does not exist.")
		return
	if not os.path.isfile(dict_file):
		print(f"Error: The file '{dict_file}' does not exist.")
		return
	if not zipfile.is_zipfile(zip_file):
		print(f"Error: The file '{zip_file}' is not a valid zip file.")
		return
	
	#Extract base name of the zip file (omit directory & extension)
	base_name = os.path.splitext(os.path.basename(zip_file))[0]

	#Create directory to hold zip file contents
	if not os.path.exists(base_name):
		os.makedirs(base_name)
		
	#Retrieve passwords from dict file
	with open(dict_file) as stream:
		data = stream.readlines()
	
	try:
		#Extract the contents of the zip file to the directory
		with zipfile.ZipFile(zip_file, 'r') as zip_ref:
			extracted = False
			#check if zip is password protected
			if any(file.flag_bits & 0x1 for file in zip_ref.infolist()):
				for passw in data:
					#zip function expects bytes not strings
					passwd = passw.strip("\n")
					passwd_en = passwd.encode()
					
					if zip_pass(zip_file, passwd_en, base_name) == True:
						extracted = True
						print(f"Succesfully extracted '{zip_file}' to '{base_name}' with password '{passwd}'")
					else:
						continue
			else:
				extracted = True
				zip_ref.extractall(base_name)
				print(f"Succesfully extracted '{zip_file}' to '{base_name}'")
			
			if extracted == False:			
				print(f"Error: The file '{zip_file}' cannot be extracted.")
	except Exception as ex:
		template = "An exception of type {0} occurred. Arguments:\n{1!r}"
		message = template.format(type(ex).__name__, ex.args)
		print(message)
		
def zip_pass(zip_file, passw, base_folder):
	with zipfile.ZipFile(zip_file) as file:
		try:
			file.extractall(path=base_folder, pwd=passw)
			return True
		except RuntimeError:
			return False
			
def print_help():
	print("This script attempts to extract the contents of a zip file.")
  print("Usage: python script.py <zip_file> <password_dict_file>")

if __name__ == "__main__":
	if len(sys.argv) < 2 or len(sys.argv) > 3:
		print_help()
		sys.exit(1)
	else:
		zip_file = sys.argv[1]
		dict_file = sys.argv[2]
		extract_zip(zip_file, dict_file)
