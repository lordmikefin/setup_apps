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

from . import PATH_INSTALLERS
from . import util

import os
from setup_apps.base import Base
from setup_apps.tag import Tag


class Java(Base):

    def __init__(self):
        super().__init__()

        self.install_path_ok = False
        self.install_path = None
        self.install_path_full = None
        self.exe_file = None

    def generate_all(self, source: dict):
        self.generate_full_url_from_source(source)
        print('installer_full_url       : ' + str(self.installer_full_url))
    
        self.generate_installer_path()
        print('installer_path           : ' + str(self.installer_path))
        # TODO: get md5/sha256 file from the sourse
        #self.installer_path_md5 = None  # NOTE: this is set in Base class!
        self.installer_path_md5 = 'OpenJDK8U-jdk_x64_windows_hotspot_8u242b08.msi.sha256.txt'
        #self.installer_path = PATH_INSTALLERS + self.installer_file
        #self.installer_path_md5 = self.installer_path + '.md5'  # NOTE: this is set in Base class!
        self.installer_path_md5 = PATH_INSTALLERS + 'OpenJDK8U-jdk_x64_windows_hotspot_8u242b08.msi.sha256.txt'
        #self.installer_full_url_md5 = None  # NOTE: this is set in Base class!
        self.installer_full_url_md5 = self.sha256url

        self.generate_install_path()
        print('install_path_full        : ' + str(self.install_path_full))

    def generate_install_path(self):
        if self.install_path is None:
            # TODO: log error
            print('ERROR: Incorrect Java config: Missing tag "' + Tag.install_path + '"')
            return

        if self.version is None:
            # TODO: log error
            print('ERROR: Incorrect Java config: Missing tag "' + Tag.version + '"')
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

    def download(self):
        if not (self.url_ok and self.path_ok):
            # TODO: log error
            print('ERROR: Can not download Eclipse installer.')

        # TODO: refactor
        if util.is_file(self.installer_path):
            print('Java installer file exists.')
            print('Calculate sha256')
            sha = util.sha256(self.installer_path, show_progress=True)
            print('sha256: ' + str(sha))
            # TODO: get md5/sha256 file from the sourse
            if util.is_file(self.installer_path_md5):
                print('sha256 file exists')
                if util.is_md5_in_file(self.installer_path_md5, sha):
                    print('sha256 is in file')
                    self.is_downloaded = True
                    return  # file is downloaded
                else:
                    print('sha256 does not match')
                    print('download file again')

        print('Download Java installer.')
        util.download(self.installer_full_url, self.installer_path, show_progress=True)
        print('Download complete.')
        print('Download Java installer sha256 file.')
        util.download(self.installer_full_url_md5, self.installer_path_md5)
        print('Calculate sha256')
        sha = util.sha256(self.installer_path, show_progress=True)
        print('sha256: ' + str(sha))
        if util.is_file(self.installer_path_md5):
            print('sha256 file exists')
            if util.is_md5_in_file(self.installer_path_md5, sha):
                print('sha256 is in file')
                self.is_downloaded = True
            else:
                print('sha256 does not match')
                print('download failed !  TODO: interrupt the process?')
                self.is_downloaded = False

    def is_installed(self):
        # TODO: Test JDK and JRE
        # Test if JRE is installed.
        #java -version
        command = 'java -version'
        print(str(command))
        test = util.run_os_command(command)
        if test:
            print('Java NOT installed.')
            return False
    
        print('Java already installed.')
        return True

    def install(self):
        # TODO: install OracleJRE and OracleJDK other variants
        if not self.is_downloaded:
            # TODO: log error
            print('ERROR: Java installer not downloaded.')

        if self.is_installed():
            print('Java is already installed')
            return

        # TODO: implement :)
        # https://adoptopenjdk.net/installation.html#windows-msi
        
        #command = str(str(_installer_file_fullname) + ' /s')
        
        print('Start Java installer.')
        '''
        print(command)
        print('')
        print(' Installing ... wait ... wait ... ')
        print('')
        #test = util.run_os_command(command)
        print('')
        if test:
            # TODO: Installer may not throw error ?
            print('Java installation FAILED.')
            #sys.exit(1)
            return False
        else:
            print('Java installation done.')
            return True
        '''


_installer_file_fullname = ''
_file_name = ''

def is_installed_jre():
    # Test if JRE is installed.
    #java -version
    #command = str(PATH_APP_NPP) + 'java -version'
    command = 'java -version'
    print(str(command))
    test = util.run_os_command(command)
    if test:
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
        '''
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
        '''


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
    test = util.run_os_command(command)
    print('')
    if test:
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

