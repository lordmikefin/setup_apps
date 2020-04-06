# -*- coding: UTF-8 -*-
"""
    eclipse.py
    ~~~~~~~~~~

    Install Eclipse.

    License of this script file:
       MIT License

    License is available online:
      https://github.com/lordmikefin/setup_apps/blob/master/LICENSE

    Latest version of this script file:
      https://github.com/lordmikefin/setup_apps/blob/master/eclipse.py


    :copyright: (c) 2019, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
    :license: MIT License
"""

import os
import sys

from . import PATH_APP_ECLIPSE, PATH_INSTALLERS, PATH_APP_PYDEV
from . import util
from setup_apps.base import Base
from setup_apps.tag import Tag
import app_source_handler
from setup_apps.plugin import Plugin


class Eclipse(Base):

    def __init__(self):
        super().__init__()
        '''
        self.url_ok = False

        self.version = None
        self.installer_file = None
        self.installer_url = None
        self.installer_full_url = None
        self.installer_full_url_md5 = None
        '''

        # TODO: set PATH_INSTALLERS from config xml
        # self.installer_path = PATH_INSTALLERS
        # _installer_file_fullname = str(installer_path) + str(installer_file)
        '''
        self.path_ok = False
        self.installer_path = None
        self.installer_path_md5 = None
        '''

        self.install_path_ok = False
        self.install_path = None
        self.install_path_full = None
        self.exe_file = None
        self.config_eclipse_ini = None

        self.is_downloaded = False

        self.config = None
        self.plugins = None

    '''
    def _insert_file_into_url(self, file: str):
        self.installer_full_url = str(self.installer_url).format(installer_file=file)
        self.installer_full_url_md5 = self.installer_full_url + '.md5'
    '''
    '''
    def is_installer_file(self) -> bool:
        if self.installer_file:
            return True

        # TODO: log error
        print('ERROR: Incorrect Eclipse config: Missing tag "installer_file"')
        return False
    '''

    def generate_install_path(self):
        if self.install_path is None:
            # TODO: log error
            print('ERROR: Incorrect Eclipse config: Missing tag "' + Tag.install_path + '"')
            return

        if self.version is None:
            # TODO: log error
            print('ERROR: Incorrect Eclipse config: Missing tag "' + Tag.version + '"')
            return

        if not '{version}' in self.install_path:
            self.install_path_full = str(self.install_path)
            self.install_path_ok = True
            return

        self.install_path_full = str(self.install_path).format(version=self.version)
        # TODO: is there better solution? extract to temp?
        # NOTE: while extracting I got path too long error -> changed install path
        #self.unzipped = self.install_path_full + '\\eclipse'  # NOTE: zip file contains subfolder /eclipse/
        self.temp_path = 'C:\\temp'
        self.unzipped = self.temp_path + '\\eclipse'  # NOTE: zip file contains subfolder /eclipse/
        self.exe_file = self.install_path_full + '\\eclipse.exe'
        self.config_eclipse_ini = self.install_path_full + '\\eclipse.ini'
        self.install_path_ok = True

    def generate_all(self, source_eclipse: dict):
        #source_eclipse = app_source_handler.source.APPS.get('eclipse', {})
        self.generate_full_url_from_source(source_eclipse)
        print('installer_full_url       : ' + str(self.installer_full_url))
    
        self.generate_installer_path()
        print('installer_path           : ' + str(self.installer_path))
    
        self.generate_install_path()
        print('install_path_full        : ' + str(self.install_path_full))
        #self.init_plugins()

    def download(self):
        if not (self.url_ok and self.path_ok):
            # TODO: log error
            print('ERROR: Can not download Eclipse installer.')

        # TODO: refactor
        if util.is_file(self.installer_path):
            print('Eclipse installer file exists.')
            print('Calculate md5sum')
            md5 = util.md5sum(self.installer_path, show_progress=True)
            # md5 = util.md5sum(self.installer_path, callback=util.print_progress)
            # md5 = util.md5sum(self.installer_path)
            print('md5 hash: ' + str(md5))
            # TODO: get md5/sha256 file from the sourse
            if util.is_file(self.installer_path_md5):
                print('md5 file exists')
                if util.is_md5_in_file(self.installer_path_md5, md5):
                    print('md5 is in file')
                    self.is_downloaded = True
                    return  # file is downloaded
                else:
                    print('md5 does not match')
                    print('download file again')

        print('Download Eclipse installer.')
        # util.download(self.installer_full_url, self.installer_path)
        util.download(self.installer_full_url, self.installer_path, show_progress=True)
        print('Download complete.')
        print('Download Eclipse installer md5.')
        util.download(self.installer_full_url_md5, self.installer_path_md5)
        print('Calculate md5sum')
        md5 = util.md5sum(self.installer_path, show_progress=True)
        print('md5 hash: ' + str(md5))
        if util.is_file(self.installer_path_md5):
            print('md5 file exists')
            if util.is_md5_in_file(self.installer_path_md5, md5):
                print('md5 is in file')
                self.is_downloaded = True
            else:
                print('md5 does not match')
                print('download failed !  TODO: interrupt the process?')
                self.is_downloaded = False
        # self.is_downloaded = True

    def is_installed(self):
        # TODO: how to check Eclipse version?
        # For now just check if exec file exists.
        return util.is_file(self.exe_file)

    def install(self):
        if not self.is_downloaded:
            # TODO: log error
            print('ERROR: Eclipse installer not downloaded.')

        if not self.install_path_ok:
            # TODO: log error
            print('ERROR: Installation path not defined.')

        if self.is_installed():
            print('Eclipse is already installed')
            self.create_link()
            return

        print('Start Eclipse installer.')

        print('')
        print(' Installing ... wait ... wait ... ')
        print('')

        # NOTE: while extracting I got path too long error -> changed install path
        # NOTE: This is "offline installer" ;)
        #util.unzip(str(self.installer_path), str(self.install_path_full))
        #util.unzip_py(str(self.installer_path), str(self.install_path_full), show_progress=True)
        #self.temp_path
        util.unzip_py(str(self.installer_path), str(self.temp_path), show_progress=True)

        # NOTE: Eclipse is unzipped into subfolder /eclipse/ because zip file contains subfolder /eclipse/
        # TODO: Why python shutil.move() is throwing an error? How it should be used to mimic Win copy?
        #util.move(str(self.unzipped), str(self.install_path_full))  # shutil.Error: Destination path 'C:\Program Files\eclipse-2019-09\eclipse' already exists
        #util.move(str(self.unzipped) + '\\', str(self.install_path_full) + '\\') 
        #util.move_win(str(self.unzipped) + '\\*', str(self.install_path_full) + '\\')
        util.move_win(str(self.unzipped) + '', str(self.install_path_full) + '')

        if not self.is_installed():
            print('Eclipse is NOT installed!')
            return

        print('Eclipse is installed')
        print('Eclipse exe: ' + str(self.exe_file))

        # TODO: Change the default workspace folder (eclipse.ini)
        # -Dosgi.instance.area.default=@user.home/eclipse-workspace

        # NOTE: Shortcut is not created, because installer is not used.
        # TODO: Create shortcut for eclipse into Start Menu
        self.create_link()

    def create_link(self):
        # Create link into Desktop.
        dst_link_file = os.environ.get('USERPROFILE') + '\\Desktop\\Eclipse - ' + self.version + '.lnk'
        util.shortcut(exe_file=self.exe_file, dst_link_file=dst_link_file, ico='')

    def configure(self):
        print('Configure')
        if not self.config:
            print('No configures')
            return

        print('self.config ' + str(self.config))
        #self.config = None
        for file in self.config:
            name = file.get('name')
            f_type = file.get('type')
            print('name: ' + str(name) + ' type: ' + str(f_type))
            confs = file.get('confs', [])
            for conf in confs:
                key = conf.get('key')
                value = conf.get('value')
                # replase {version}
                if '{version}' in value:
                    value = value.format(version=self.version)
                
                print('key: ' + str(key) + ' value: ' + str(value))
                self.config_apply(self.install_path_full + name, key, value)

    def configure_hc(self):
        #self.config_eclipse_ini
        print('Configure hard coded test')
        key = '-Dosgi.instance.area.default'
        new_value = '@user.home/eclipse-workspace-2019-09'
        #self.config_eclipse_ini = self.install_path_full + '\\eclipse.ini'
        self.config_apply(self.config_eclipse_ini, key, new_value)

    def config_apply(self, file: str, key: str, value: str):
        print('Configure ' + str(file))
        new_key_value = key + '=' + value + '\n'
        has_key_value = False
        found_line = -1
        line_idx = -1
        lines = []
        with open(file, "r") as f:
            for line in f: 
                lines.append(line)
                line_idx += 1
                line_txt = line.lstrip()
                if util.startswith_comment(line_txt):
                    continue  # skip comment line

                has_key = line_txt.startswith(key)
                if has_key:
                    if line_txt == new_key_value:
                        print('value already set')
                        has_key_value = True
                        break  # do not set again
                    else:
                        found_line = line_idx

        if has_key_value:
            return  # do not set again

        if found_line > -1:
            print('Append line after: ' + str(found_line))
            #print('lines: ' + str(lines))
            lines.insert(found_line+1, new_key_value)
            lines[found_line] = '#' + lines[found_line]
        else:
            print('Append line at the end')
            lines.append(new_key_value)
        #print('lines: ' + str(lines))
        with open(file, 'w') as f:
            f.writelines(lines)

    def configure_test(self):
        # NOTE: this will repet the line for each run
        with open(self.config_eclipse_ini, "r") as f:
            eclipse_ini = f.read()
            # print(eclipse_ini)
        # -Dosgi.instance.area.default=@user.home/eclipse-workspace
        key = '-Dosgi.instance.area.default'
        key_idx = eclipse_ini.find(key)
        print('key_idx: ' + str(key_idx))
        ini_tmp = eclipse_ini[key_idx:]
        next_line_idx = ini_tmp.find('\n')
        old_key_value = ini_tmp[:next_line_idx]
        new_value = '@user.home/eclipse-workspace-2019-09'
        new_key_value = key + '=' + new_value 
        write_lines = True
        if old_key_value == new_key_value:
            print('value already set')
            write_lines = False

        if write_lines:
            new_data = '#' + old_key_value + '\n' + new_key_value
            new_eclipse_ini = eclipse_ini.replace(old_key_value, new_data, 1)
            print(new_eclipse_ini)
            with open(self.config_eclipse_ini, 'w') as f:
                f.write(new_eclipse_ini) 

    def init_plugins(self, source_eclipse: dict):
        print('Initialize plugins')
        print('self.plugins ' + str(self.plugins))
        if not self.plugins:
            print('No plugins')
            return

        if False:  # Definition only for Eclipse auto complete
            plug = Plugin()

        # TODO: how elegantly share names between 'setup_apps' and 'app_source'?
        # NOTE: for now just use hard coded name
        source_plugins = source_eclipse.get('plugins', {})
        for plug in self.plugins:
            print('plug.version: ' + str(plug.version))
            print('plug.installer_file: ' + str(plug.installer_file))
            print('plug.installer_url: ' + str(plug.installer_url))
            #print('plug.install_path: ' + str(plug.install_path))
            # TODO: get plugin by name form the source
            #source_plugin = source_plugins.get('pydev', {})
            plug.generate_all(self.install_path_full, source_plugins)

    def download_plugins(self):
        print('Download plugins')
        print('self.plugins ' + str(self.plugins))
        if not self.plugins:
            print('No plugins')
            return

        if False:  # Definition only for Eclipse auto complete
            plug = Plugin()

        for plug in self.plugins:
            plug.download()

    def install_plugins(self):
        print('Install plugins')
        print('self.plugins ' + str(self.plugins))
        if not self.plugins:
            print('No plugins')
            return

        if False:  # Definition only for Eclipse auto complete
            plug = Plugin()

        for plug in self.plugins:
            plug.install()


_installer_file_fullname = ''
_file_name = ''

_exe_file = ''

# TODO: 'Eclipse' is depended on Java.
# TODO: Define/test dependencies <-> when config file is used to define what will be installed.    


def is_installed():
    # TODO: Test if Eclipse is installed.

    # For now just check if exec file exists.
    # D:\apps\eclipse\pydev\2019-09\eclipse
    # return util.is_file(str(PATH_APP_PYDEV) + '\\2019-09\\eclipse\\eclipse.exe')
    # return util.is_file(str(PATH_APP_PYDEV) + '\\eclipse\\eclipse.exe')
    return util.is_file(_exe_file)


def is_download():
    # Check if we already have the installer
    # print(str(_installer_file_fullname))
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
        # url = 'https://www.eclipse.org/downloads/download.php?file=/oomph/epp/2019-09/R/' + str(_file_name) + '&mirror_id=1099'
        # url = 'https://www.eclipse.org/downloads/download.php?file=/oomph/epp/2019-09/R/' + str(_file_name)
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

    # installer_file = "eclipse-inst-win64.exe"
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

    # command = str(str(_installer_file_fullname))
    # command = str(str(_installer_file_fullname) + ' -vmargs -Doomph.setup.install.root=' + str(PATH_APP_PYDEV))
    # command = str(str(_installer_file_fullname) + ' -vm "C:\Program Files\Java\jre1.8.0_221" EclipsePyDevConfiguration.setup -vmargs -Doomph.setup.install.root=' + str(PATH_APP_PYDEV))
    print('Start Eclipse installer.')
    # print(command)
    print('')
    print(' Installing ... wait ... wait ... ')
    print('')
    # res = int(os.system(command))
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
    
    return True  # TODO: return error?

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

