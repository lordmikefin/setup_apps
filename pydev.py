# -*- coding: UTF-8 -*-
"""
    pydev.py
    ~~~~~~~~

    Install PyDev a Python IDE for Eclipse.

    License of this script file:
       MIT License

    License is available online:
      https://github.com/lordmikefin/LMAutoSetBotWin/blob/master/LICENSE

    Latest version of this script file:
      https://github.com/lordmikefin/LMAutoSetBotWin/blob/master/setup_apps/pydev.py


    :copyright: (c) 2019, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
    :license: MIT License
"""

from . import PATH_APP_PYDEV, PATH_INSTALLERS
from . import util

import os
import sys


_installer_file_fullname = ''
_file_name = ''

_eclipse_path = ''
_jar_file = ''

# TODO: 'PyDev' is depended on Eclipse.
# TODO: Define/test dependencies <-> when config file is used to define what will be installed.    


def is_installed():
    # TODO: Test if PyDev is installed.
    #print(_jar_file)
    return util.is_file(_jar_file)


def is_download():
    # TODO: Improver verification. Size or hash compare.
    # Check if we already have the installer
    #print(str(_installer_file_fullname))
    return util.is_file(_installer_file_fullname)


def download():
    '''
    https://sourceforge.net/p/forge/documentation/Downloading%20files%20via%20the%20command%20line/
    
    Installing with the zip file

    The available locations for the zip files are:

        SourceForge download
        https://sourceforge.net/projects/pydev/files/pydev/PyDev%207.4.0/
        https://sourceforge.net/projects/pydev/files/pydev/PyDev%207.4.0/PyDev%207.4.0.zip/download
        https://sourceforge.net/projects/pydev/files/pydev/PyDev%207.4.0/PyDev%207.4.0.zip/download?use_mirror=netcologne
        https://downloads.sourceforge.net/project/pydev/pydev/PyDev%207.4.0/PyDev%207.4.0.zip?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fpydev%2Ffiles%2Flatest%2Fdownload&ts=1575289277
    '''
    print('Download PyDev installer.')
    
    if _file_name:
        url = 'https://sourceforge.net/projects/pydev/files/pydev/PyDev%207.4.0/PyDev%207.4.0.zip/download'
        util.download(url, _installer_file_fullname)


def install():
    '''
    TODO: download pydev and extract into Eclipse
    https://www.pydev.org/
    https://www.pydev.org/manual_101_root.html
    https://www.pydev.org/manual_101_install.html
    https://www.pydev.org/manual_101_interpreter.html

    After downloading the zip file:

    Extract the contents of the zip file in the eclipse/dropins folder and restart Eclipse.

    If it doesn't work, try restarting Eclipse with the -clean flag 
    (if you're a regular user and installing with admin, make sure you call -clean logged in as admin, so that Eclipse finds out about it).

    If it's still not found, double check the requisites (such as the Java vm version).
    Checking the installation

    You can verify if it is correctly installed going to the menu 'window > preferences' and checking if there is a PyDev item under that.
    '''
    print('Start pydev installer.')
    print('')
    print(' Installing ... wait ... wait ... ')
    print('')

    # NOTE: This is "offline installer" ;)
    #print(str(_installer_file_fullname) + ' :: ' + str(_eclipse_path))
    util.unzip(str(_installer_file_fullname), str(_eclipse_path))

    return True # TODO: return error?


def define_file():
    global _installer_file_fullname
    global _file_name
    global _eclipse_path
    global _jar_file

    installer_file = "PyDev 7.4.0.zip"
    _file_name = installer_file

    installer_path = PATH_INSTALLERS
    _installer_file_fullname = str(installer_path) + str(installer_file)

    #_exe_file = str(PATH_APP_PYDEV) + '\\eclipse\\eclipse.exe'
    _eclipse_path = str(PATH_APP_PYDEV) + '\\eclipse'

    #W:\PyDev 7.4.0.zip\plugins\org.python.pydev_7.4.0.201910251334\pydev.jar
    _jar_file = _eclipse_path + '\\plugins\\org.python.pydev_7.4.0.201910251334\\pydev.jar'
    print(str(_installer_file_fullname))


def run():
	print('')
	print('Test comment from "pydev.py"')

	print('Value of variable "PATH_APP_PYDEV": ' + str(PATH_APP_PYDEV))
	print('Value of variable "PATH_INSTALLERS": ' + str(PATH_INSTALLERS))

	define_file()
	if not is_download():
		download()

	if not is_download():
		# TODO: How we should handle error?
		print('')
		print('Installer is still missing!?')
		print('I will now exit with error :(')
		util.pause()
		sys.exit(1)

	if not is_installed():
		if install():
		    pass

	if not is_installed():
		# TODO: How we should handle error?
		print('')
		print('pydev was not installed!?')
		print('I will now exit with error :(')
		util.pause()
		sys.exit(1)

