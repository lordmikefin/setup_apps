# -*- coding: UTF-8 -*-
"""
	python.py
	~~~~~~~~~

	Install python

	License of this script file:
	   MIT License

	License is available online:
	  https://github.com/lordmikefin/LMAutoSetBotWin/blob/master/LICENSE

	Latest version of this script file:
	  https://github.com/lordmikefin/LMAutoSetBotWin/blob/master/setup_apps/python.py


	:copyright: (c) 2020, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
	:license: MIT License
"""

# TODO: how to dynamically define the python folder version?
#from . import PATH_APP_PY37, PATH_INSTALLERS
from . import PATH_APP_PY38, PATH_INSTALLERS
from . import util


import os
import re
import subprocess


_ver = ''
_installer_file_fullname = ''
_file_name = ''

_cmd = '"' + str(PATH_APP_PY38) + '\\python.exe"'


def set_env_var():
	# TODO: make util from this
	#   https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/setx
	'''
	command = 'setx GIT_SSH ' + '"' + str(_plink) + '"'
	print(str(command))
	res = int(os.system(command))
	if res > 0:
		print('GIT_SSH is not set.')
		return False

	print('GIT_SSH is set.')
	return True
	'''
	pass


def is_installed():
	# TODO: how to update if version is different
	# util.compare_version(ver_a: str, ver_b: str)

	command = _cmd + ' --version'
	print(str(command))
	# NOTE: os.system() just runs the process, it doesn't capture the output
	#   https://unix.stackexchange.com/questions/418616/python-how-to-print-value-that-comes-from-os-system

	#res = int(os.system(command))
	com_res = util.run_command(command)
	res = com_res.errorlevel
	if res > 0:
		print('python NOT installed.')
		return False

	print('python already installed.')
	return True


def is_download():
	# \\192.168.122.1\sambashare\windows\putty-0.73.tar.gz
	# By now \\192.168.122.1\sambashare\windows\ should be bind to W: drive
	#print(str(_installer_file_fullname))

	# https://stackabuse.com/python-check-if-a-file-or-directory-exists/
	return os.path.isfile(_installer_file_fullname)


def download():
	# https://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3
	# TODO: download file from web
	#   Verify downloaded file is what we were downloading.

	# https://www.python.org/ftp/python/3.8.1/python-3.8.1-amd64.exe
	print('Download python installer.')
	
	if _file_name:
		url = 'https://www.python.org/ftp/python/' + _ver + '/' + str(_file_name)
		util.download(url, _installer_file_fullname)


def install():
	# Install python

	# https://stackoverflow.com/questions/14894993/running-windows-shell-commands-with-python

	# TODO: Silent (unattended) install
	#   https://docs.python.org/3/using/windows.html#installing-without-ui

	# TODO: 'quiet' mode does not install Python if installer ask to select 'install', 'repair', etc

	command = _installer_file_fullname + ' /quiet '
	command = command + ' InstallAllUsers=1 '
	command = command + ' TargetDir="' + PATH_APP_PY38 + '"'
	command = command + ' PrependPath=1 '
	print('Start python installer.')
	print(command)
	print('')
	print(' Installing ... wait ... wait ... ')
	print('')
	res = int(os.system(command))
	print('')
	if res > 0:
		# TODO: Installer may not throw error ?
		print('python installation FAILED.')
		#sys.exit(1)
		return False
	else:
		print('python installation done.')
		return True


def define_file():
	global _ver
	global _installer_file_fullname
	global _file_name
	global _cmd

	# https://www.python.org/ftp/python/3.8.1/python-3.8.1-amd64.exe

	_ver = '3.8.1'
	installer_file = 'python-' + _ver + '-amd64.exe'
	_file_name = installer_file

	#installer_path = "W:/"
	installer_path = PATH_INSTALLERS
	_installer_file_fullname = str(installer_path) + str(installer_file)

	_cmd = '"' + str(PATH_APP_PY38) + '\\python.exe"'

	print(str(_installer_file_fullname))


def run():
	print('')
	print('Test comment from "python.py"')

	print('Value of variable "PATH_APP_PY38": ' + str(PATH_APP_PY38))
	print('Value of variable "PATH_INSTALLERS": ' + str(PATH_INSTALLERS))

	define_file()
	if not is_download():
		download()

	if not is_installed():
		install()

	#set_env_var()

