# -*- coding: UTF-8 -*-
"""
	npp.py
	~~~~~~

	Install Notepad++

	License of this script file:
	   MIT License

	License is available online:
	  https://github.com/lordmikefin/LMAutoSetBotWin/blob/master/LICENSE

	Latest version of this script file:
	  https://github.com/lordmikefin/LMAutoSetBotWin/blob/master/setup_apps/npp.py


	:copyright: (c) 2019, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
	:license: MIT License
"""

from . import PATH_APP_NPP, PATH_INSTALLERS
from . import util


import os


_installer_file_fullname = ''
_file_name = ''

def is_installed_npp():
	# TODO: This will open help windows. Is there better way to test ?
	#command = str(PATH_APP_NPP) + '\\notepad++ --help'
	command = '"' + str(PATH_APP_NPP) + '\\notepad++" -quickPrint'
	print(str(command))
	res = int(os.system(command))
	if res > 0:
		print('Notepad++ NOT installed.')
		return False

	print('Notepad++ already installed.')
	return True


def is_download_npp():
	# TODO: Check if we already have the installer
	# \\192.168.122.1\sambashare\windows\npp.7.5.8.Installer.x64
	# By now \\192.168.122.1\sambashare\windows\ should be bind to W: drive
	print(str(_installer_file_fullname))

	# https://stackabuse.com/python-check-if-a-file-or-directory-exists/
	return os.path.isfile(_installer_file_fullname)


def download_npp():
	# https://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3
	# TODO: download file from web
	#   Verify downloaded file is what we were downloading.

	# https://notepad-plus-plus.org/downloads/
	# https://notepad-plus-plus.org/downloads/v7.7.1/
	# http://download.notepad-plus-plus.org/repository/7.x/7.7.1/npp.7.7.1.Installer.exe
	print('Download notepad++ installer.')
	
	if _file_name:
		url = 'http://download.notepad-plus-plus.org/repository/7.x/7.7.1/' + str(_file_name)
		## Download the file from `url` and save it locally under `file_name`
		#file_name, headers = urllib.request.urlretrieve(url, _installer_file_fullname)
		#print('file_name : ' + str(file_name))
		#print('headers   : ' + str(headers))
		util.download(url, _installer_file_fullname)


def define_file_npp():
	global _installer_file_fullname
	global _file_name

	#installer_file = "npp.7.5.8.Installer.x64"
	#installer_file = "npp.7.7.1.Installer.exe"
	installer_file = "npp.7.7.1.Installer.x64.exe"
	_file_name = installer_file

	#installer_path = "W:/"
	installer_path = PATH_INSTALLERS
	_installer_file_fullname = str(installer_path) + str(installer_file)

	print(str(_installer_file_fullname))

def install_npp():
	# Install notepad++
	#define_file_npp()

	# https://stackoverflow.com/questions/14894993/running-windows-shell-commands-with-python

	# https://notepad-plus-plus.org/download
	# TODO: download file from web
	#   Verify downloaded file is what we were downloading.

	# https://stackoverflow.com/questions/42792305/trying-to-set-up-a-deployment-package-for-silent-uninstall-of-notepad-and-inst#
	# https://www.itninja.com/software/open-source-1/notepad-2/5-1399

	command = str(str(_installer_file_fullname) + ' /S /D=' + str(PATH_APP_NPP) + ' ')
	print('Start notepad++ installer.')
	print(command)
	print('')
	print(' Installing ... wait ... wait ... ')
	print('')
	res = int(os.system(command))
	print('')
	if res > 0:
		# TODO: Installer may not throw error ?
		print('notepad++ installation FAILED.')
		#sys.exit(1)
		return False
	else:
		print('notepad++ installation done.')
		return True

def run():
	# TODO: Download Notepad++ installer

	# TODO: Install Notepad++

	print('Test comment from "npp.py"')

	print('Value of variable "PATH_APP_NPP": ' + str(PATH_APP_NPP))
	print('Value of variable "PATH_INSTALLERS": ' + str(PATH_INSTALLERS))


	define_file_npp()
	if not is_download_npp():
		download_npp()

	if not is_installed_npp():
		install_npp()

	# TODO: Disable 'security warning' and UAC
	#install_npp()

