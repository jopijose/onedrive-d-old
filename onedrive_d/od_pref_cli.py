"""
Pereference wizard program using command-line interface.
It guides user to set up the configurations step by step.
"""

import os
import sys
import shutil
import subprocess

from . import od_bootstrap
from . import od_account


def open_in_editor(file_path):
	subprocess.call(
			['${EDITOR:-vi} "' + file_path + '"'], shell=True)


def query_yes_no(question, default='yes'):
	valid = {'yes': True, 'y': True, 'ye': True, 'no': False, 'n': False}
	if default is None:
		prompt = ' [y/n] '
	elif default == "yes":
		prompt = ' [Y/n] '
	elif default == "no":
		prompt = ' [y/N] '
	else:
		raise ValueError("invalid default answer: '%s'" % default)
	while True:
		choice = input(question + prompt).lower()
		if default is not None and choice == '':
			return valid[default]
		elif choice in valid:
			return valid[choice]
		else:
			print("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


class bcolors:
	BLUE = '\033[96m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


class PreferenceGuide:
	def __init__(self):
		self.user_info = od_account.get_user_info()
		self.config_info = od_account.get_user_config(self.user_info)
		self.logger = od_bootstrap.get_logger()
		if self.config_info is None:
			if not os.path.isdir(od_account.ACCOUNT_INVENTORY):
				try:
					shutil.rmtree(od_account.ACCOUNT_INVENTORY)
				except:
					pass
				try:
					# create dir owned by root
					od_bootstrap.mkdir(od_account.ACCOUNT_INVENTORY, 0, 0)
				except OSError as e:
					self.logger.critical('Failed to create directory "{0}" as root - {1} (005.{2}).'.format(od_account.ACCOUNT_INVENTORY, e.strerror, e.errno))
					sys.exit(1)
			# TODO: format config information
		else:
			pass

	def start(self):
		print(bcolors.BLUE + 'Welcome, %s!' % self.user_info['os_user_name'])
		while True:
			print(bcolors.BLUE + bcolors.BOLD + 'Select one action from the following list:' + bcolors.ENDC)
			print(bcolors.BLUE + '1. Add a new OneDrive account' + bcolors.ENDC)
			print(bcolors.BLUE + '2. Edit a linked OneDrive account' + bcolors.ENDC)
			print(bcolors.BLUE + '3. Remove a linked OneDrive account' + bcolors.ENDC)
			print(bcolors.BLUE + '4. Change onedrive-d settings' + bcolors.ENDC)
			print(bcolors.BLUE + '5. Exit wizard' + bcolors.ENDC)
			choice = input(bcolors.BOLD + 'Which action do you want to perform (1-5): ' + bcolors.ENDC).strip()
			if choice == '1':
				self.add_onedrive_account()
			elif choice == '2':
				self.edit_onedrive_account()
			elif choice == '3':
				self.remove_onedrive_account()
			elif choice == '4':
				self.change_settings()
			elif choice == '5':
				sys.exit(0)
			else:
				print(bcolors.RED + 'Error: unrecognized action number "' + choice + '".' + bcolors.ENDC)

	def add_onedrive_account(self):
		pass

	def list_onedrive_account(self):
		pass

	def edit_onedrive_account(self):
		pass

	def remove_onedrive_account(self):
		pass

	def change_settings(self):
		print(bcolors.GREEN + 'Edit configuration file for user "%s"...' % self.user_info['os_user_name'] + bcolors.ENDC)
		config_file_path = self.user_info['os_user_home'] + '/' + od_account.USER_CONFIG_FILE_PATH
		config_dir_path = os.path.dirname(config_file_path)
		if not os.path.isdir(config_dir_path):
			print(bcolors.YELLOW + 'User config dir "%s" is missing. Try Creating it.' % config_dir_path + bcolors.ENDC)
			try:
				od_bootstrap.mkdir(config_dir_path, 0, 0)
			except Exception as e:
				print(bcolors.RED + 'Failed to create config dir - {0} (006.{1}).'.format(e.strerror, e.errno) + bcolors.ENDC)
				print(bcolors.RED + 'Action failed.' + bcolors.RED)
				return
		if self.config_info is None:
			print(bcolors.RED + 'Current configuration is missing. Load default.' + bcolors.ENDC)
			self.config_info = od_account.get_default_config()
			with open(config_file_path, 'w') as f:
				self.config_info.write(f)
		print('Opening config file "%s"...' % config_file_path)
		open_in_editor(config_file_path)
		# read the modified info and sanitize it
		config_info = od_account.get_user_config(self.user_info)
		with open(config_file_path, 'w') as f:
			config_info.write(f)
		self.config_info = config_info
		print(bcolors.GREEN + 'Action complete.' + bcolors.ENDC)
