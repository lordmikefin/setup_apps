# -*- coding: UTF-8 -*-
"""
    putty.py
    ~~~~~~~~

    Install Putty and assosiated soft

    License of this script file:
       MIT License

    License is available online:
      https://github.com/lordmikefin/setup_apps/blob/master/LICENSE

    Latest version of this script file:
      https://github.com/lordmikefin/setup_apps/blob/master/putty.py


    :copyright: (c) 2019, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
    :license: MIT License
"""

from . import util

from setup_apps.base import Base
from setup_apps.util import logger
from setup_apps.tag import Tag
from setup_apps import SETUP

class Putty(Base):

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
        #self.installer_path_md5 = PATH_INSTALLERS + self.checksum.file #: :type self.checksum: Checksum
        #self.installer_path_md5 = PATH_INSTALLERS + self.checksum.file #: :type checksum: Checksum
        sum_obj = self.checksum #: :type sum_obj: Checksum
        self.installer_path_md5 = SETUP.path_installers + sum_obj.file
        logger.info('installer_path_md5        : ' + str(self.installer_path_md5))

    def generate_install_path(self):
        if self.install_path is None:
            logger.error('Incorrect Putty config: Missing tag "' + Tag.install_path + '"')
            return

        if self.version is None:
            logger.error('Incorrect Putty config: Missing tag "' + Tag.version + '"')
            return

        if not '{version}' in self.install_path:
            self.install_path_full = str(self.install_path)
            #self.exe_file = self.install_path_full + '\\putty.exe'
            self.exe_file = self.install_path_full + '\\plink.exe'
            self.install_path_ok = True
            return

        self.install_path_full = str(self.install_path).format(version=self.version)
        #self.exe_file = self.install_path_full + '\\putty.exe'
        self.exe_file = self.install_path_full + '\\plink.exe'
        self.install_path_ok = True

    def download(self) -> bool:
        if not (self.url_ok and self.path_ok):
            logger.error('Can not download Putty installer.')
            return False

        if not self.checksum:
            logger.error('Checksum data missing.')
            return False

        if self.is_installer_downloaded(self.checksum):
            self.is_downloaded = True
            return True

        logger.info('Download Putty installer.')
        down_ok = util.download(self.installer_full_url, self.installer_path, show_progress=True)
        if not down_ok:
            logger.error('Download of Putty installer failed.')
            return False

        logger.info('Download complete.')

        if self.is_installer_downloaded(self.checksum):
            logger.info('Download is verified.')
            self.is_downloaded = True
            return True

        logger.error('Download of Putty installer failed.')
        return False

    def is_installed(self):
        # TODO: how to test putty exists
        #   https://the.earth.li/~sgtatham/putty/0.73/htmldoc/Chapter3.html#using-cmdline
        #command = str(PATH_APP_PUTTY) + '\\putty'
        # NOTE: putty does not print version, but plink does
        #command = '"' + str(PATH_APP_PUTTY) + '\\plink' + '"' + ' -V '
        #command = '"' + str(_plink) + '"' + ' -V '
        command = '"' + self.exe_file + '"' + ' -V '
        '''
        print(str(command))
        test = util.run_os_command(command)
        if not test:
        '''
        com_res = util.run_command(command)
        res = com_res.errorlevel
        if res > 0:
            logger.info('Putty NOT installed.')
            return False
    
        logger.info('Putty already installed.')
        return True

    def install(self) -> bool:
        if not self.is_downloaded:
            logger.error('Putty installer not downloaded.')
            return False

        if not self.install_path_ok:
            logger.error('Installation path not defined.')
            return False

        if self.is_installed():
            logger.info('Putty is already installed')
            return False

        logger.info('Start Putty installer.')
        logger.info('Installing ... wait ... wait ... ')
        # Install Putty
        # https://stackoverflow.com/questions/14894993/running-windows-shell-commands-with-python
    
        # Silent (unattended) install
        # http://www.silentinstall.org/msiexec
        # http://mylittlespotinthebigunknown.blogspot.com/2018/04/automating-putty-07-msi-install.html
        properties = {
            'ACTION': 'INSTALL',
            'ADDLOCAL': 'FilesFeature,DesktopFeature,PathFeature,PPKFeature',
            }
        #util.msiexec(name, installer, properties, log_file, show_progress)
        test = util.msiexec("Putty Install", self.installer_path,
                            properties, log_file='PuttyInstall.log')
        
        # TODO: use 'run_command' -function instead inside 'msiexec' and return CommandRet
        #res_err = com_res.errorlevel
        #logger.debug('Install command error level: ' + str(res_err))
        #if res_err != 0:
        if not test:
            logger.error('Putty installation FAILED.')
            return False

        logger.info('Putty installation done.')
        return True

    def configure(self):
        logger.info('Configure Putty')
        if not self.config:
            logger.info('Putty No configures')
            return

        logger.info('self.config ' + str(self.config))
        for conf_list in self.config:
            commands_list = conf_list.get('enviroments')
            for command in commands_list:
                logger.info('command: ' + str(command))
                key = command.get('key', '')
                value = command.get('value', '')
                if '{plink_exe_full_path}' in value:
                    value = str(value).format(plink_exe_full_path=self.exe_file)
                util.log_env_var(key)
                util.set_env_var(key, value)
                util.log_env_var(key)
                '''
                # {plink_exe_full_path}  self.exe_file
                if '{plink_exe_full_path}' in command:
                    plink = '"' + self.exe_file + '"'
                    com = 'setx ' + str(command).format(plink_exe_full_path=plink)
                    logger.debug('com: ' + str(com))
                    util.run_command(com)
                '''

# TODO: remove obsolete code
'''
_putty_ver = ''
_installer_file_fullname = ''
_file_name = ''
_plink = ''


def set_env_var():
    # TODO: make util from this
    #   https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/setx
    command = 'setx GIT_SSH ' + '"' + str(_plink) + '"'
    print(str(command))
    test = util.run_os_command(command)
    if not test:
        print('GIT_SSH is not set.')
        return False

    print('GIT_SSH is set.')
    return True


def is_installed():
    # TODO: how to test putty exists
    #   https://the.earth.li/~sgtatham/putty/0.73/htmldoc/Chapter3.html#using-cmdline
    #command = str(PATH_APP_PUTTY) + '\\putty'
    # NOTE: putty does not print version, but plink does
    #command = '"' + str(PATH_APP_PUTTY) + '\\plink' + '"' + ' -V '
    command = '"' + str(_plink) + '"' + ' -V '
    print(str(command))
    test = util.run_os_command(command)
    if not test:
        print('Putty NOT installed.')
        return False

    print('Putty already installed.')
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

    # https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
    # https://the.earth.li/~sgtatham/putty/latest/w64/putty-64bit-0.73-installer.msi
    print('Download Putty installer.')
    
    if _file_name:
        url = 'https://the.earth.li/~sgtatham/putty/latest/w64/' + str(_file_name)
        ## Download the file from `url` and save it locally under `file_name`
        #file_name, headers = urllib.request.urlretrieve(url, _installer_file_fullname)
        #print('file_name : ' + str(file_name))
        #print('headers   : ' + str(headers))
        util.download(url, _installer_file_fullname)


def install():
    # Install Putty

    # https://stackoverflow.com/questions/14894993/running-windows-shell-commands-with-python

    # Silent (unattended) install
    # http://www.silentinstall.org/msiexec
    # http://mylittlespotinthebigunknown.blogspot.com/2018/04/automating-putty-07-msi-install.html

    # TODO: use util 'msiexec' -function
    command = 'START "Putty Install" /WAIT msiexec /qb '
    command = command + ' /L*V PuttyInstall.log '
    command = command + ' /i ' + str(_installer_file_fullname)
    #command = command + ' INSTALLDIR="C:\Program Files\PuTTY\" '
    command = command + ' ACTION=INSTALL '
    command = command + ' ADDLOCAL=FilesFeature,DesktopFeature,PathFeature,PPKFeature '
    print('Start Putty installer.')
    print(command)
    print('')
    print(' Installing ... wait ... wait ... ')
    print('')
    test = util.run_os_command(command)
    print('')
    if not test:
        # TODO: Installer may not throw error ?
        print('Putty installation FAILED.')
        #sys.exit(1)
        return False
    else:
        print('Putty installation done.')
        return True


def define_file():
    global _putty_ver
    global _installer_file_fullname
    global _file_name
    global _plink

    _plink = str(PATH_APP_PUTTY) + '\\plink'

    _putty_ver = '0.73'
    installer_file = 'putty-64bit-' + _putty_ver + '-installer.msi'
    _file_name = installer_file

    #installer_path = "W:/"
    installer_path = PATH_INSTALLERS
    _installer_file_fullname = str(installer_path) + str(installer_file)

    print(str(_installer_file_fullname))


def run():
    # TODO: Download Putty

    # TODO: Install Putty

    print('')
    print('Test comment from "putty.py"')

    print('Value of variable "PATH_APP_PUTTY": ' + str(PATH_APP_PUTTY))
    print('Value of variable "PATH_INSTALLERS": ' + str(PATH_INSTALLERS))

    define_file()
    if not is_download():
        download()

    if not is_installed():
        install()

    set_env_var()
'''
