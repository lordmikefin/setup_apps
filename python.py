# -*- coding: UTF-8 -*-
"""
    python.py
    ~~~~~~~~~

    Install python

    License of this script file:
       MIT License

    License is available online:
      https://github.com/lordmikefin/setup_apps/blob/master/LICENSE

    Latest version of this script file:
      https://github.com/lordmikefin/setup_apps/blob/master/python.py


    :copyright: (c) 2020, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
    :license: MIT License
"""

# TODO: how to dynamically define the python folder version?
#from . import PATH_APP_PY37, PATH_INSTALLERS
from . import util

from setup_apps.base import Base
from setup_apps.util import logger
from setup_apps.tag import Tag
from setup_apps import SETUP


class Python(Base):

    def __init__(self):
        super().__init__()

        self.install_path_ok = False
        self.install_path = None
        self.install_path_full = None
        self.exe_file = None

    def generate_all(self, source: dict):
        super().generate_all(source)
        self.generate_install_path()
        logger.info('install_path_full        : ' + str(self.install_path_full))

        # TODO: this should be done in Base
        sum_obj = self.checksum #: :type sum_obj: Checksum
        self.installer_path_md5 = SETUP.path_installers + sum_obj.file
        logger.info('installer_path_md5        : ' + str(self.installer_path_md5))

    def generate_install_path(self):
        if self.install_path is None:
            logger.error('Incorrect Python config: Missing tag "' + Tag.install_path + '"')
            return

        if self.version is None:
            logger.error('Incorrect Python config: Missing tag "' + Tag.version + '"')
            return

        if not '{version}' in self.install_path:
            self.install_path_full = str(self.install_path)
            self.exe_file = self.install_path_full + '\\python.exe'
            self.install_path_ok = True
            return

        self.install_path_full = str(self.install_path).format(version=self.version)
        self.exe_file = self.install_path_full + '\\python.exe'
        self.install_path_ok = True

    def download(self) -> bool:
        if not (self.url_ok and self.path_ok):
            logger.error('Can not download Python installer.')
            return False

        if not self.checksum:
            logger.error('Checksum data missing.')
            return False

        if self.is_installer_downloaded(self.checksum):
            self.is_downloaded = True
            return True

        logger.info('Download Python installer.')
        down_ok = util.download(self.installer_full_url, self.installer_path, show_progress=True)
        if not down_ok:
            logger.error('Download of Python installer failed.')
            return False

        logger.info('Download complete.')

        if self.is_installer_downloaded(self.checksum):
            logger.info('Download is verified.')
            self.is_downloaded = True
            return True

        logger.error('Download of Python installer failed.')
        return False

    def is_installed(self):
        # TODO: how to update if version is different
        # util.compare_version(ver_a: str, ver_b: str)

        command = '"' + self.exe_file + '"' + ' --version'
        logger.info(str(command))
        com_res = util.run_command(command)
        res = com_res.errorlevel
        if res > 0:
            logger.info('Python NOT installed.')
            return False
    
        logger.info('Python already installed.')
        return True

    def install(self) -> bool:
        if not self.is_downloaded:
            logger.error('Python installer not downloaded.')
            return False

        if not self.install_path_ok:
            logger.error('Installation path not defined.')
            return False

        if self.is_installed():
            logger.info('Python is already installed')
            return False

        logger.info('Start Python installer.')
        logger.info('Installing ... wait ... wait ... ')
        # Install python
        # https://stackoverflow.com/questions/14894993/running-windows-shell-commands-with-python

        # TODO: Silent (unattended) install
        #   https://docs.python.org/3/using/windows.html#installing-without-ui

        # TODO: 'quiet' mode does not install Python if installer ask to select 'install', 'repair', etc
        command = self.installer_path + ' /quiet '
        command = command + ' InstallAllUsers=1 '
        command = command + ' TargetDir="' + self.install_path_full + '"'
        command = command + ' PrependPath=1 '
        '''
        test = util.run_os_command(command)
        if not test:
        '''
        com_res = util.run_command(command)
        res = com_res.errorlevel
        if res > 0:
            logger.error('Python installation FAILED.')
            return False

        logger.info('Python installation done.')
        return True

# TODO: remove obsolete code
'''
_ver = ''
_installer_file_fullname = ''
_file_name = ''

_cmd = '"' + str(PATH_APP_PY38) + '\\python.exe"'



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
    test = util.run_os_command(command)
    print('')
    if not test:
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
'''
