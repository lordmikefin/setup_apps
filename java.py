# -*- coding: UTF-8 -*-
"""
    java.py
    ~~~~~~~

    Install Java JDK/JRE.

    License of this script file:
       MIT License

    License is available online:
      https://github.com/lordmikefin/setup_apps/blob/master/LICENSE

    Latest version of this script file:
      https://github.com/lordmikefin/setup_apps/blob/master/java.py


    :copyright: (c) 2019, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
    :license: MIT License
"""

from . import util

import os
from setup_apps.base import Base
from setup_apps.tag import Tag
from setup_apps.util import logger
from setup_apps import SETUP


class Java(Base):

    def __init__(self):
        super().__init__()

        self.install_path_ok = False
        self.install_path = None
        self.install_path_full = None
        self.exe_file = None


    def generate_all(self, source: dict):
        super().generate_all(source)
        #self.log_init()
        #self.generate_full_url_from_source(source)
        #logger.info('installer_full_url       : ' + str(self.installer_full_url))
    
        #self.generate_installer_path()
        #logger.info('installer_path           : ' + str(self.installer_path))
        # TODO: get md5/sha256 file from the sourse
        #self.installer_path_md5 = None  # NOTE: this is set in Base class!
        #self.installer_path_md5 = 'OpenJDK8U-jdk_x64_windows_hotspot_8u242b08.msi.sha256.txt'
        #self.installer_path = PATH_INSTALLERS + self.installer_file
        #self.installer_path_md5 = self.installer_path + '.md5'  # NOTE: this is set in Base class!
        #self.installer_path_md5 = PATH_INSTALLERS + 'OpenJDK8U-jdk_x64_windows_hotspot_8u242b08.msi.sha256.txt'
        self.installer_path_md5 = SETUP.path_installers + self.checksum.file
        #self.installer_full_url_md5 = None  # NOTE: this is set in Base class!
        #self.installer_full_url_md5 = self.sha256url

        self.generate_install_path()
        logger.info('install_path_full        : ' + str(self.install_path_full))

    def generate_install_path(self):
        if self.install_path is None:
            logger.error('Incorrect Java config: Missing tag "' + Tag.install_path + '"')
            return

        if self.version is None:
            logger.error('Incorrect Java config: Missing tag "' + Tag.version + '"')
            return

        if not '{version}' in self.install_path:
            self.install_path_full = str(self.install_path)
            self.install_path_ok = True
            return

        self.install_path_full = str(self.install_path).format(version=self.version)
        self.exe_file = self.install_path_full + '\\bin\\java.exe'
        self.install_path_ok = True
        '''
        # TODO: is there better solution? extract to temp?
        # NOTE: while extracting I got path too long error -> changed install path
        #self.unzipped = self.install_path_full + '\\eclipse'  # NOTE: zip file contains subfolder /eclipse/
        self.temp_path = 'C:\\temp'
        self.unzipped = self.temp_path + '\\eclipse'  # NOTE: zip file contains subfolder /eclipse/
        self.config_eclipse_ini = self.install_path_full + '\\eclipse.ini'
        '''

    def download(self) -> bool:
        if not (self.url_ok and self.path_ok):
            logger.error('Can not download Java installer.')
            return False

        if not self.checksum:
            logger.error('Checksum data missing.')
            return False

        if self.is_installer_downloaded(self.checksum):
            self.is_downloaded = True
            return True

        logger.info('Download Java installer.')
        down_ok = util.download(self.installer_full_url, self.installer_path, show_progress=True)
        if not down_ok:
            logger.error('Download of Java installer failed.')
            return False

        logger.info('Download complete.')

        if self.is_installer_downloaded(self.checksum):
            logger.info('Download is verified.')
            self.is_downloaded = True
            return True

        logger.error('Download of Java installer failed.')
        return False
        '''
        # TODO: refactor
        if util.is_file(self.installer_path):
            logger.info('Java installer file exists.')
            logger.info('Calculate sha256')
            sha = util.sha256(self.installer_path, show_progress=True)
            logger.info('sha256: ' + str(sha))
            # TODO: get md5/sha256 file from the sourse
            if util.is_file(self.installer_path_md5):
                logger.info('sha256 file exists')
                if util.is_md5_in_file(self.installer_path_md5, sha, self.installer_path):
                    logger.info('sha256 is in file')
                    self.is_downloaded = True
                    return  # file is downloaded
                else:
                    logger.info('sha256 does not match')
                    logger.info('download file again')

        logger.info('Download Java installer.')
        util.download(self.installer_full_url, self.installer_path, show_progress=True)
        logger.info('Download complete.')
        logger.info('Download Java installer sha256 file.')
        #util.download(self.installer_full_url_md5, self.installer_path_md5)
        util.download(self.checksum.url, self.installer_path_md5)
        logger.info('Calculate sha256')
        sha = util.sha256(self.installer_path, show_progress=True)
        logger.info('sha256: ' + str(sha))
        if util.is_file(self.installer_path_md5):
            logger.info('sha256 file exists')
            if util.is_md5_in_file(self.installer_path_md5, sha, self.installer_path):
                logger.info('sha256 is in file')
                self.is_downloaded = True
            else:
                logger.info('sha256 does not match')
                logger.error('download failed !?  TODO: interrupt the process?')
                self.is_downloaded = False
        '''

    def is_installed(self):
        # TODO: Test JDK and JRE
        # Test if JRE is installed.
        #java -version
        command = 'java -version'
        logger.info(str(command))
        '''
        test = util.run_os_command(command)
        if not test:
        '''
        com_res = util.run_command(command)
        res = com_res.errorlevel
        if res > 0:
            logger.info('Java NOT installed.')
            return False
    
        logger.info('Java already installed.')
        return True

    def install(self) -> bool:
        # TODO: install OracleJRE and OracleJDK other variants
        if not self.is_downloaded:
            logger.error('Java installer not downloaded.')
            return False

        if not self.install_path_ok:
            logger.error('Installation path not defined.')
            return False

        if self.is_installed():
            logger.info('Java is already installed')
            return False

        # https://adoptopenjdk.net/installation.html#windows-msi
        logger.info('Start Java installer.')
        logger.info(' Installing ... wait ... wait ... ')
        test = util.msiexec(
            name = 'Java installer',
            installer = self.installer_path,
            properties = {
                'INSTALLDIR': self.install_path_full,
                'ADDLOCAL': 'FeatureMain,FeatureEnvironment,FeatureJarFileRunWith,FeatureJavaHome',
                },
            # TODO: log installation messages
            log_file = None,
            show_progress = True
        )

        if test:
            logger.error('Java installation FAILED.')
            #sys.exit(1)
            return False

        logger.info('Java installation done.')
        return True

    def configure(self):
        logger.info('Configure Java')
        self.update_env_var_path()

    def update_env_var_path(self):
        # TODO: Do we need to update environment variables? PATH?
        # TODO: PATH is updated in req -> so just update local PATH from req
        #  -> util.log_env_var(key)

        # C:\Program Files (x86)\Common Files\Oracle\Java\javapath;
        javapath = 'C:\\Program Files (x86)\\Common Files\\Oracle\\Java\\javapath'
        # self.install_path_full
        path = str(os.environ.get('PATH'))
        logger.debug('PATH: ' + str(path))
        '''
        command = str('PATH=' + str(_javapath) + ';%PATH%')
        res = int(os.system(command))
        os.environ['PATH'] = str(_javapath) + ';' + _path
        '''

# TODO: remove obsolete code
'''
_installer_file_fullname = ''
_file_name = ''

def is_installed_jre():
    # Test if JRE is installed.
    #java -version
    #command = str(PATH_APP_NPP) + 'java -version'
    command = 'java -version'
    logger.info(str(command))
    test = util.run_os_command(command)
    if not test:
        logger.error('OracleJRE NOT installed.')
        return False

    logger.info('OracleJRE already installed.')
    return True


def is_download_jre():
    # Check if we already have the installer
    logger.info(str(_installer_file_fullname))
    return os.path.isfile(_installer_file_fullname)


def download_jre():
    # Download file from web
    # TODO: Verify downloaded file is what we were downloading.

    logger.info('Download Java OracleJRE installer.')

    if _file_name:
        url = 'https://download.oracle.com/otn/java/jdk/8u221-b11/230deb18db3e4014bb8e3e8324f81b43/' + str(_file_name)
        # Download the file from `url` and save it locally under `file_name`
        #util.download(url, _installer_file_fullname)
        logger.info('Can not auto download Oracle JRE !!!')
        logger.info('Download "' + str(_file_name) + '" manually into folder: ' + str(_installer_file_fullname))
        logger.info('  https://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html')
        '
        # TODO: Use OpenJDK
        https://openjdk.java.net/
        https://openjdk.java.net/install/index.html
        https://en.wikipedia.org/wiki/OpenJDK
        https://developers.redhat.com/blog/2016/06/27/openjdk-now-available-for-windows/
        https://developers.redhat.com/products/openjdk
        https://developers.redhat.com/products/openjdk/download
        https://developers.redhat.com/download-manager/file/java-1.8.0-openjdk-1.8.0.242-3.b08.redhat.windows.x86_64.msi
        https://adoptopenjdk.net/installation.html#x64_win-jdk
        https://github.com/AdoptOpenJDK/openjdk8-binaries/releases/download/jdk8u242-b08/OpenJDK8U-jdk_x64_windows_hotspot_8u242b08.zip
        https://github.com/AdoptOpenJDK/openjdk8-binaries/releases/download/jdk8u242-b08/OpenJDK8U-jdk_x64_windows_hotspot_8u242b08.msi
        https://adoptopenjdk.net/installation.html#windows-msi
        '


def define_file_jre():
    global _installer_file_fullname
    global _file_name

    installer_file = "jre-8u221-windows-x64.exe"
    _file_name = installer_file

    installer_path = PATH_INSTALLERS
    _installer_file_fullname = str(installer_path) + str(installer_file)

    logger.info(str(_installer_file_fullname))


def install_jre():
    '
    TODO: download and install Java:  OracleJRE
    Oracle
    https://www.oracle.com/technetwork/java/index.html

    https://stackoverflow.com/questions/51403071/create-jre-from-openjdk-windows

    https://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html
    https://download.oracle.com/otn/java/jdk/8u221-b11/230deb18db3e4014bb8e3e8324f81b43/jre-8u221-windows-x64.exe
    '
    # TODO: Install silently
    # TODO: Can I change java installation path?
    # TODO: how to install Java silently (unattended)
    # https://www.java.com/en/download/help/silent_install.xml
    #   /s, if used, indicates a silent installation.
    command = str(str(_installer_file_fullname) + ' /s')
    logger.info('Start OracleJRE installer.')
    logger.info(command)
    logger.info(' Installing ... wait ... wait ... ')
    test = util.run_os_command(command)
    if not test:
        # TODO: Installer may not throw error ?
        logger.error('OracleJRE installation FAILED.')
        #sys.exit(1)
        return False
    else:
        logger.info('OracleJRE installation done.')
        return True


def is_installed_jdk():
    False


def install_jdk():
    '
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
    '
    pass

def update_env_var_path():
    # TODO: Do we need to update environment variables? PATH?
    # C:\Program Files (x86)\Common Files\Oracle\Java\javapath;
    _javapath = 'C:\\Program Files (x86)\\Common Files\\Oracle\\Java\\javapath'
    #PATH=%PATH_APP_PY37%\;%PATH_APP_PY37%\Scripts\;%PATH%
    
    _path = str(os.environ.get('PATH'))
    #print('')
    #print('PATH : ' + _path)
    '
    command = str('PATH=' + str(_javapath) + ';%PATH%')
    #print(command)
    res = int(os.system(command))
    #print('result : ' + str(res))
    '
    os.environ['PATH'] = str(_javapath) + ';' + _path
    #print('PATH : ' + str(os.environ.get('PATH')))

def run():
    logger.info('Test comment from "java.py"')

    # TODO: Can default installation be changed?  (C:\Program Files\Java\jre1.8.0_221)
    #print('Value of variable "PATH_APP_NPP": ' + str(PATH_APP_NPP))
    logger.info('Value of variable "PATH_INSTALLERS": ' + str(PATH_INSTALLERS))

    define_file_jre()
    if not is_download_jre():
        download_jre()

    if not is_installed_jre():
        if install_jre():
            update_env_var_path()
'''
