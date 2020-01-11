# -*- coding: UTF-8 -*-
"""
	setup_apps
	~~~~~~~~~~

	Module for installing windows applictions.

	License of this script file:
	   MIT License

	License is available online:
	  https://github.com/lordmikefin/LMAutoSetBotWin/blob/master/LICENSE

	Latest version of this script file:
	  https://github.com/lordmikefin/LMAutoSetBotWin/blob/master/setup_apps/__init__.py


	:copyright: (c) 2019, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
	:license: MIT License
"""

__license__ = "MIT License"
__version__ = "0.0.24"
__revision__ = "setup_apps (module)  v" + __version__ + " (2020-01-06)"


'''
These lines are copied from init.bat (2019-09-30)

:: Create directory for Installer and install path.
::   C:\LM_ToyBox\temp
::   C:\LM_ToyBox\apps
::   C:\LM_ToyBox\apps\Git
::   C:\LM_ToyBox\apps\Python\Python37
SET PATH_TOY_BOX=C:\LM_ToyBox\
SET PATH_INSTALLERS=%PATH_TOY_BOX%temp
SET PATH_APPS=%PATH_TOY_BOX%apps
SET PATH_APP_GIT=%PATH_APPS%\Git
SET PATH_APP_PY37=%PATH_APPS%\Python37
'''

# TODO: Remove this venv testing.
# Testing venv
#import babel


# https://docs.python.org/3.7/howto/logging.html
import logging

import sys
import os

# Listing initialiazion (init.bat) phase paths.
# TODO: Are these needed?
INIT_PATH_TOY_BOX = 'C:\\LM_ToyBox\\'
INIT_PATH_INSTALLERS = INIT_PATH_TOY_BOX + 'temp'
# TODO: parameterize the destination installation path
#INIT_PATH_APPS = INIT_PATH_TOY_BOX + 'apps'
INIT_PATH_APPS = 'C:\Program Files'
INIT_PATH_APP_GIT = INIT_PATH_APPS + '\\Git'
INIT_PATH_APP_PY37 = INIT_PATH_APPS + '\\Python37'


# TODO: Get paths from config file.

# Using default paths for downloading and installing apps.
PATH_ROOT = 'D:\\'
PATH_TOY_BOX = PATH_ROOT + 'LM_ToyBox\\'
#PATH_INSTALLERS = PATH_TOY_BOX + 'temp'
#PATH_INSTALLERS = PATH_TOY_BOX + 'download'
DRIVE_INSTALLER = 'W:'
PATH_INSTALLERS = DRIVE_INSTALLER + '\\'
# TODO: parameterize the destination installation path
#PATH_APPS = PATH_TOY_BOX + 'apps'
#PATH_APPS = PATH_ROOT + 'apps'
PATH_APPS = INIT_PATH_APPS

PATH_APP_GIT = PATH_APPS + '\\Git'
# TODO: how to dynamically define the python folder version?
PATH_APP_PY37 = PATH_APPS + '\\Python37'
PATH_APP_PY38 = PATH_APPS + '\\Python38'
PATH_APP_NPP = PATH_APPS + '\\Notepad++'
PATH_APP_ECLIPSE = PATH_APPS + '\\eclipse'
PATH_APP_PYDEV = PATH_APPS + '\\eclipse\\pydev'
PATH_APP_PUTTY = PATH_APPS + '\\putty'


def connect_samba_share():
	""" Connect samba share. """
	# TODO: Test if drive exists.
	
	# TODO: Get samba share address from config.
	#command = 'net use W: \\192.168.122.1\sambashare\windows'
	command = 'net use ' + DRIVE_INSTALLER + ' \\192.168.122.1\sambashare\windows'
	res = int(os.system(command))
	print('')
	if res > 0:
		print('Samba connection  FAILED.')
		#sys.exit(1)
		return False
	else:
		print('Samba share connected.')
		return True


#connect_samba_share()

from . import config

# TODO: Import at top of this script.
# TODO: Activat 'npp' with function call !
from . import npp
from . import java
from . import eclipse
from . import pydev
from . import putty
from . import git
from . import python

