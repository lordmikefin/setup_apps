# -*- coding: UTF-8 -*-
"""
    npp.py
    ~~~~~~

    Install Notepad++

    License of this script file:
       MIT License

    License is available online:
      https://github.com/lordmikefin/setup_apps/blob/master/LICENSE

    Latest version of this script file:
      https://github.com/lordmikefin/setup_apps/blob/master/npp.py


    :copyright: (c) 2019, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
    :license: MIT License
"""

from . import PATH_APP_NPP, PATH_INSTALLERS
from . import util

import os
from setup_apps.base import Base, Checksum
from setup_apps.util import logger
from setup_apps.tag import Tag

class Npp(Base):

    def __init__(self):
        super().__init__()

        self.install_path_ok = False
        self.install_path = None
        self.install_path_full = None
        self.exe_file = None

        # TODO: move 'self.is_downloaded' into Base 
        self.is_downloaded = False


    def generate_all(self, source: dict):
        super().generate_all(source)
        self.generate_install_path()
        logger.info('install_path_full        : ' + str(self.install_path_full))

        # TODO: this should be done in Base
        self.installer_path_md5 = PATH_INSTALLERS + self.checksum.file
        logger.info('installer_path_md5        : ' + str(self.installer_path_md5))

    def generate_install_path(self):
        if self.install_path is None:
            logger.error('Incorrect Npp config: Missing tag "' + Tag.install_path + '"')
            return

        if self.version is None:
            logger.error('Incorrect Npp config: Missing tag "' + Tag.version + '"')
            return

        if not '{version}' in self.install_path:
            self.install_path_full = str(self.install_path)
            self.install_path_ok = True
            return

        self.install_path_full = str(self.install_path).format(version=self.version)
        self.exe_file = self.install_path_full + '\\notepad++.exe'
        self.install_path_ok = True


    def is_installer_downloaded(self, checksum: Checksum):
        if not util.is_file(self.installer_path):
            return False

        installer_hashsum = checksum.create_hash(self.installer_path)
        if checksum.is_hash_correct(installer_hashsum, self.installer_path):
            logger.info('Hash check ok.')
            return True

        logger.info('Hash check failed.')
        return False


    def download(self) -> bool:
        # TODO: this is improved function -> copy this logic for other apps
        if not (self.url_ok and self.path_ok):
            logger.error('Can not download Notepad++ installer.')
            return False

        if not self.checksum:
            logger.error('Checksum data missing.')
            return False

        if self.is_installer_downloaded(self.checksum):
            self.is_downloaded = True
            return True

        logger.info('Download Notepad++ installer.')
        util.download(self.installer_full_url, self.installer_path, show_progress=True)
        logger.info('Download complete.')

        if self.is_installer_downloaded(self.checksum):
            logger.info('Download is verified.')
            self.is_downloaded = True
            return True

        logger.error('Download of Notepad++ installer failed.')
        return False

    def is_installed(self):
        logger.error('Notepad++ implement installation test.')
        # TODO: How to print version? Following command will show 'help' window.
        # > "C:\Program Files\Notepad++\notepad++.exe" --help
        file = 'C:\\Program Files\\Notepad++\\notepad++.exe'
        if util.is_file(file):
            return True
        return False

    def install(self) -> bool:
        if not self.is_downloaded:
            logger.error('Notepad++ installer not downloaded.')
            return False

        if not self.install_path_ok:
            logger.error('Installation path not defined.')
            return False

        if self.is_installed():
            logger.info('Notepad++ is already installed')
            return False

        logger.error('Notepad++ installation not yet implemented.')
        return False


_installer_file_fullname = ''
_file_name = ''

def is_installed_npp():
    # TODO: This will open help windows. Is there better way to test ?
    #command = str(PATH_APP_NPP) + '\\notepad++ --help'
    command = '"' + str(PATH_APP_NPP) + '\\notepad++" -quickPrint'
    print(str(command))
    test = util.run_os_command(command)
    if not test:
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
    test = util.run_os_command(command)
    print('')
    if not test:
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

