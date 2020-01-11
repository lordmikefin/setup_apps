# -*- coding: UTF-8 -*-
"""
    eclipse.py
    ~~~~~~~~~~

    Install Eclipse.

    License of this script file:
       MIT License

    License is available online:
      https://github.com/lordmikefin/LMAutoSetBotWin/blob/master/LICENSE

    Latest version of this script file:
      https://github.com/lordmikefin/LMAutoSetBotWin/blob/master/setup_apps/eclipse.py


    :copyright: (c) 2019, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
    :license: MIT License
"""

from . import PATH_APP_ECLIPSE, PATH_INSTALLERS, PATH_APP_PYDEV
from . import util

import os
import sys

_installer_file_fullname = ''
_file_name = ''

_exe_file = ''

# TODO: 'Eclipse' is depended on Java.
# TODO: Define/test dependencies <-> when config file is used to define what will be installed.    


def is_installed():
    # TODO: Test if Eclipse is installed.

    # For now just check if exec file exists.
    # D:\apps\eclipse\pydev\2019-09\eclipse
    #return util.is_file(str(PATH_APP_PYDEV) + '\\2019-09\\eclipse\\eclipse.exe')
    #return util.is_file(str(PATH_APP_PYDEV) + '\\eclipse\\eclipse.exe')
    return util.is_file(_exe_file)


def is_download():
    # Check if we already have the installer
    #print(str(_installer_file_fullname))
    return util.is_file(_installer_file_fullname)


def download():
    '''
    # TODO: Is there offline installer?
    # https://www.eclipse.org/downloads/packages/
    https://www.eclipse.org/downloads/download.php?file=/technology/epp/downloads/release/2019-09/R/eclipse-javascript-2019-09-R-win32-x86_64.zip
    https://www.eclipse.org/downloads/download.php?file=/technology/epp/downloads/release/2019-09/R/eclipse-javascript-2019-09-R-win32-x86_64.zip&mirror_id=1156
    https://ftp.acc.umu.se/mirror/eclipse.org/technology/epp/downloads/release/2019-09/R/eclipse-javascript-2019-09-R-win32-x86_64.zip

    TODO: download and install Eclipse
    https://www.eclipse.org/downloads/
    https://www.eclipse.org/downloads/download.php?file=/oomph/epp/2019-09/R/eclipse-inst-win64.exe
    https://www.eclipse.org/downloads/download.php?file=/oomph/epp/2019-09/R/eclipse-inst-win64.exe&mirror_id=1099
    '''
    print('Download Eclipse installer.')
    
    if _file_name:
        #url = 'https://www.eclipse.org/downloads/download.php?file=/oomph/epp/2019-09/R/' + str(_file_name) + '&mirror_id=1099'
        #url = 'https://www.eclipse.org/downloads/download.php?file=/oomph/epp/2019-09/R/' + str(_file_name)
        url = 'https://ftp.acc.umu.se/mirror/eclipse.org/technology/epp/downloads/release/2019-09/R/' + str(_file_name)
        # Download the file from `url` and save it locally under `file_name`
        util.download(url, _installer_file_fullname)
        '''
        print('')
        print('I can not download the file :(')
        print('You need to manually download it into destination: ' + str(_installer_file_fullname))
        print('  ' + str(url))
        print('')
        print('Continue when downloaded.')
        # TODO: Who installer can be downloaded? Use "Robot Framework"?
        util.pause()
        '''


def define_file():
    global _installer_file_fullname
    global _file_name
    global _exe_file

    #installer_file = "eclipse-inst-win64.exe"
    installer_file = "eclipse-javascript-2019-09-R-win32-x86_64.zip"
    _file_name = installer_file

    installer_path = PATH_INSTALLERS
    _installer_file_fullname = str(installer_path) + str(installer_file)

    _exe_file = str(PATH_APP_PYDEV) + '\\eclipse\\eclipse.exe'
    print(str(_installer_file_fullname))


def install():
    # TODO: Is there offline installer?
    # https://www.eclipse.org/downloads/packages/

    # PATH_APP_PYDEV
    # PATH_APP_ECLIPSE
    # TODO: Is there way to define installation path.
    # TODO: Eclipse should have separate instance for Python development.

    # Installer from the command line
    #   https://www.eclipse.org/forums/index.php/t/1091113/
    #   https://www.eclipse.org/forums/index.php/t/1086000/
    #   https://www.eclipse.org/forums/index.php/t/1073078/
    #   https://wiki.eclipse.org/Eclipse_Oomph_Authoring#Automation_and_Specialization_with_Configurations

    # eclipse-inst-win64.exe -vm c:\apps\jdk8 configuration.setup -vmargs -Doomph.setup.install.root=C:\directory
    # EclipseCurrentConfiguration.setup

    #command = str(str(_installer_file_fullname))
    #command = str(str(_installer_file_fullname) + ' -vmargs -Doomph.setup.install.root=' + str(PATH_APP_PYDEV))
    #command = str(str(_installer_file_fullname) + ' -vm "C:\Program Files\Java\jre1.8.0_221" EclipsePyDevConfiguration.setup -vmargs -Doomph.setup.install.root=' + str(PATH_APP_PYDEV))
    print('Start Eclipse installer.')
    #print(command)
    print('')
    print(' Installing ... wait ... wait ... ')
    print('')
    #res = int(os.system(command))
    # TODO: How to halt command line until installation is completed?

    # NOTE: This is "offline installer" ;)
    util.unzip(str(_installer_file_fullname), str(PATH_APP_PYDEV))
    
    # TODO: Change the default workspace folder (eclipse.ini)
    # -Dosgi.instance.area.default=@user.home/eclipse-workspace
    
    # NOTE: Shortcut is not created, because installer is not used.
    # TODO: Create shortcut for eclipse into Start Menu
    
    # Create link into Desktop.
    dst_link_file = os.environ.get('USERPROFILE') + '\\Desktop\\Eclipse pydev.lnk'
    util.shortcut(exe_file=_exe_file, dst_link_file=dst_link_file, ico='')
    
    return True # TODO: return error?

    '''
    print('Eclipse installer will not halt command line :(')
    print('Please let me know when installation is completed.')
    util.pause()
    print('')
    if res > 0:
        # TODO: Installer may not throw error ?
        print('Eclipse installation FAILED.')
        #sys.exit(1)
        return False
    else:
        print('Eclipse installation done.')
        return True
    '''


def run():
	print('')
	print('Test comment from "eclipse.py"')

	print('Value of variable "PATH_APP_ECLIPSE": ' + str(PATH_APP_ECLIPSE))
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
		print('Eclipse was not installed!?')
		print('I will now exit with error :(')
		util.pause()
		sys.exit(1)

