# -*- coding: UTF-8 -*-
"""
	java.py
	~~~~~~~

	Install Java JDK/JRE.

	License of this script file:
	   MIT License

	License is available online:
	  https://github.com/lordmikefin/LMAutoSetBotWin/blob/master/LICENSE

	Latest version of this script file:
	  https://github.com/lordmikefin/LMAutoSetBotWin/blob/master/setup_apps/java.py


	:copyright: (c) 2019, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
	:license: MIT License
"""

from . import PATH_INSTALLERS
from . import util

import os


_installer_file_fullname = ''
_file_name = ''

def is_installed_jre():
    # Test if JRE is installed.
    #java -version
    #command = str(PATH_APP_NPP) + 'java -version'
    command = 'java -version'
    print(str(command))
    res = int(os.system(command))
    if res > 0:
        print('OracleJRE NOT installed.')
        return False

    print('OracleJRE already installed.')
    return True


def is_download_jre():
	# Check if we already have the installer
	print(str(_installer_file_fullname))
	return os.path.isfile(_installer_file_fullname)


def download_jre():
    # Download file from web
    # TODO: Verify downloaded file is what we were downloading.

    print('Download Java OracleJRE installer.')

    if _file_name:
        url = 'https://download.oracle.com/otn/java/jdk/8u221-b11/230deb18db3e4014bb8e3e8324f81b43/' + str(_file_name)
        # Download the file from `url` and save it locally under `file_name`
        #util.download(url, _installer_file_fullname)
        print('')
        print('Can not auto download Oracle JRE !!!')
        print('Download "' + str(_file_name) + '" manually into folder: ' + str(_installer_file_fullname))
        print('  https://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html')


def define_file_jre():
	global _installer_file_fullname
	global _file_name

	installer_file = "jre-8u221-windows-x64.exe"
	_file_name = installer_file

	installer_path = PATH_INSTALLERS
	_installer_file_fullname = str(installer_path) + str(installer_file)

	print(str(_installer_file_fullname))


def install_jre():
    '''
    TODO: download and install Java:  OracleJRE
    Oracle
    https://www.oracle.com/technetwork/java/index.html

    https://stackoverflow.com/questions/51403071/create-jre-from-openjdk-windows

    https://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html
    https://download.oracle.com/otn/java/jdk/8u221-b11/230deb18db3e4014bb8e3e8324f81b43/jre-8u221-windows-x64.exe
    '''
    # TODO: Install silently
    # TODO: Can I change java installation path?
    # TODO: how to install Java silently (unattended)
    # https://www.java.com/en/download/help/silent_install.xml
    #   /s, if used, indicates a silent installation.
    command = str(str(_installer_file_fullname) + ' /s')
    print('Start OracleJRE installer.')
    print(command)
    print('')
    print(' Installing ... wait ... wait ... ')
    print('')
    res = int(os.system(command))
    print('')
    if res > 0:
        # TODO: Installer may not throw error ?
        print('OracleJRE installation FAILED.')
        #sys.exit(1)
        return False
    else:
        print('OracleJRE installation done.')
        return True


def is_installed_jdk():
	False

	
def install_jdk():
	'''
	TODO: download and install Java:  OpenJDK or OracleJDK
	Oracle
	https://www.oracle.com/technetwork/java/index.html

	OpenJDK
	https://openjdk.java.net/
	https://openjdk.java.net/install/
	https://jdk.java.net/13/
	ZIP
	https://download.java.net/java/GA/jdk13/5b8a42f3905b406298b72d750b6919f6/33/GPL/openjdk-13_windows-x64_bin.zip
	SHA256
	https://download.java.net/java/GA/jdk13/5b8a42f3905b406298b72d750b6919f6/33/GPL/openjdk-13_windows-x64_bin.zip.sha256
	'''
	pass

def update_env_var_path():
    # TODO: Do we need to update environment variables? PATH?
    # C:\Program Files (x86)\Common Files\Oracle\Java\javapath;
    _javapath = 'C:\\Program Files (x86)\\Common Files\\Oracle\\Java\\javapath'
    #PATH=%PATH_APP_PY37%\;%PATH_APP_PY37%\Scripts\;%PATH%
    
    _path = str(os.environ.get('PATH'))
    #print('')
    #print('PATH : ' + _path)
    '''
    command = str('PATH=' + str(_javapath) + ';%PATH%')
    print(command)
    res = int(os.system(command))
    print('result : ' + str(res))
    '''
    os.environ['PATH'] = str(_javapath) + ';' + _path
    #print('PATH : ' + str(os.environ.get('PATH')))

def run():
	print('')
	print('Test comment from "java.py"')

	# TODO: Can default installation be changed?  (C:\Program Files\Java\jre1.8.0_221)
	#print('Value of variable "PATH_APP_NPP": ' + str(PATH_APP_NPP))
	print('Value of variable "PATH_INSTALLERS": ' + str(PATH_INSTALLERS))

	define_file_jre()
	if not is_download_jre():
		download_jre()

	if not is_installed_jre():
		if install_jre():
		    update_env_var_path()

