# -*- coding: UTF-8 -*-
"""
	git.py
	~~~~~~

	Install Putty and assosiated soft

	License of this script file:
	   MIT License

	License is available online:
	  https://github.com/lordmikefin/LMAutoSetBotWin/blob/master/LICENSE

	Latest version of this script file:
	  https://github.com/lordmikefin/LMAutoSetBotWin/blob/master/setup_apps/git.py


	:copyright: (c) 2019, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
	:license: MIT License
"""

from . import PATH_APP_GIT, PATH_INSTALLERS
from . import util


import os
import re
import subprocess


_git_ver = ''
_installer_file_fullname = ''
_file_name = ''

_git_cmd = '"' + str(PATH_APP_GIT) + '\\bin\\git"'

# TODO: parameterize user and email.
_user = 'Lord Mike'
_user_mail = 'lordmike@iki.fi'


def define_the_user():
	# TODO: parameterize user and email.
	command = _git_cmd + ' config --global user.name "' + _user + '"'
	print(str(command))
	''' NOTE: This will raise error: 'C:\Program' is not recognized as an internal or external command, operable program or batch file.
	res = int(os.system(command))
	if res > 0:
		print('Failed to set user for git!')
	'''

	try:
		test = subprocess.check_output(command, shell=True)
		#print(str(test))
		#print('TEST')
	except subprocess.CalledProcessError as err:
		print('Failed to set user for git!')
		print("Error: {0}".format(err))
	except:
		print('Failed to set user for git!')
		print("Unexpected error:", sys.exc_info()[0])
		print("Unexpected error:", sys.exc_info())

	command = _git_cmd + ' config --global user.email ' + _user_mail
	print(str(command))
	res = int(os.system(command))
	if res > 0:
		print('Failed to set user email for git!')


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
	# TODO: Improve this function. Contains too many thigs.
	# TODO: how to update if version is different
	# util.compare_version(ver_a: str, ver_b: str)

	command = _git_cmd + ' --version'
	print(str(command))
	# NOTE: os.system() just runs the process, it doesn't capture the output
	#   https://unix.stackexchange.com/questions/418616/python-how-to-print-value-that-comes-from-os-system
	res = int(os.system(command))
	if res > 0:
		print('git NOT installed.')
		return False

	print('git already installed.')
	# TODO: read more about 'subprocess'
	#   https://docs.python.org/3/library/subprocess.html
	#version_current = subprocess.check_output(command, shell=True);
	com_res = util.run_command(command)
	version_current = com_res.stdout
	res_err = com_res.errorlevel
	print(version_current)
	print(type(version_current))
	#print(str(version_current, 'utf-8'))
	#parsed_ver = parse_version(str(version_current, 'utf-8'))
	parsed_ver = parse_version(str(version_current))
	print(parsed_ver)
	test = util.compare_version(_git_ver, parsed_ver)
	print(test)
	if test == 1: # A is newer
		print('Current version is older.')
		print('Upgrading git to version' + _git_ver + '.')
		return False
	return True


def parse_version(git_ver: str) -> str:
	# https://docs.python.org/3/library/re.html
	res = re.search(r'[0-9]+\.[0-9]+\.[0-9]+', git_ver)
	print(res)
	print(res[0])
	#return git_ver
	return res[0]


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

	# https://github.com/git-for-windows/git/releases/download/v2.23.0.windows.1/Git-2.23.0-64-bit.exe
	# https://github.com/git-for-windows/git/releases/download/v2.24.1.windows.2/Git-2.24.1.2-64-bit.exe
	# https://github.com/git-for-windows/git/releases/tag/v2.24.1.windows.2
	print('Download git installer.')
	
	if _file_name:
		url = 'https://github.com/git-for-windows/git/releases/download/v2.24.1.windows.2/' + str(_file_name)
		util.download(url, _installer_file_fullname)


def install():
	# Install git

	# https://stackoverflow.com/questions/14894993/running-windows-shell-commands-with-python

	# READ MORE: Silent (unattended) install
	#   https://github.com/msysgit/msysgit/wiki/Silent-or-Unattended-Installation
	#   http://www.jrsoftware.org/ishelp/index.php?topic=setupcmdline

	# TODO: Generate the inf file.
	# TODO: Is there way to set all inf-file selections with command line?

	command = _installer_file_fullname + ' /SILENT '
	command = command + ' /LOADINF="git.inf" '
	command = command + ' /LOG="git-install.log" '
	command = command + ' /DIR="' + PATH_APP_GIT + '"'
	print('Start git installer.')
	print(command)
	print('')
	print(' Installing ... wait ... wait ... ')
	print('')
	res = int(os.system(command))
	print('')
	if res > 0:
		# TODO: Installer may not throw error ?
		print('git installation FAILED.')
		#sys.exit(1)
		return False
	else:
		print('git installation done.')
		return True


def define_file():
	global _git_ver
	global _installer_file_fullname
	global _file_name
	global _git_cmd

	# https://github.com/git-for-windows/git/releases/download/v2.23.0.windows.1/Git-2.23.0-64-bit.exe
	# https://github.com/git-for-windows/git/releases/download/v2.24.1.windows.2/Git-2.24.1.2-64-bit.exe
	# https://github.com/git-for-windows/git/releases/tag/v2.24.1.windows.2

	_git_ver = '2.24.1'
	installer_file = 'Git-' + _git_ver + '.2-64-bit.exe'
	_file_name = installer_file

	#installer_path = "W:/"
	installer_path = PATH_INSTALLERS
	_installer_file_fullname = str(installer_path) + str(installer_file)

	_git_cmd = '"' + str(PATH_APP_GIT) + '\\bin\\git"'

	print(str(_installer_file_fullname))


def run():
	# TODO: Download Putty

	# TODO: Install Putty

	print('')
	print('Test comment from "git.py"')

	print('Value of variable "PATH_APP_GIT": ' + str(PATH_APP_GIT))
	print('Value of variable "PATH_INSTALLERS": ' + str(PATH_INSTALLERS))

	define_file()
	if not is_download():
		download()

	if not is_installed():
		install()

	#set_env_var()

	if is_installed():
		define_the_user()

