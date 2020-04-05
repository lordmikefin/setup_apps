# -*- coding: UTF-8 -*-
"""
    plugin.py
    ~~~~~~~~~

    Install app plugins.

    License of this script file:
       MIT License

    License is available online:
      https://github.com/lordmikefin/setup_apps/blob/master/LICENSE

    Latest version of this script file:
      https://github.com/lordmikefin/setup_apps/blob/master/plugin.py


    :copyright: (c) 2020, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
    :license: MIT License
"""

from . import util
from setup_apps.base import Base
import app_source_handler


class Plugin(Base):

    def __init__(self):
        super().__init__()
        self.name = None

        self.install_path_ok = False

        self.install_path = None
        self.install_path_full = None

    def generate_all(self, install_path: str, source_plugins: dict):
        # TODO: how to get source data?
        #source_eclipse = app_source_handler.source.APPS.get('eclipse', {})
        # NOTE: using the name set in config xml
        # TODO: how to share plugin names elegantly between 'setup_apps' and 'app_source'?
        #Tag.name
        if not self.name:
            print('"name" tag missing ?!')
        # TODO: plugins are under the app -> how to get them?
        source = source_plugins.get(self.name, {})

        self.install_path = install_path
        #self.generate_full_url()
        self.generate_full_url_from_source(source)
        print('installer_full_url       : ' + str(self.installer_full_url))
    
        self.generate_installer_path()
        print('installer_path           : ' + str(self.installer_path))
    
        self.generate_install_path()
        print('install_path_full        : ' + str(self.install_path_full))

    def generate_install_path(self):
        if self.install_path is None:
            print('ERROR: Incorrect Eclipse plugin config: "install_path" is not defined')
            return

        #self.install_path = self.install_path + '\\plugins\\org.python.pydev_7.4.0.201910251334\\pydev.jar'
        # Define 'plugins' install folder
        # NOTE: zip file contains the 'plugins' folder.
        #self.install_path = self.install_path + '\\plugins'
        self.install_path = self.install_path

        # TODO: is there need to set version ?
        '''
        if self.version is None:
            print('ERROR: Incorrect Eclipse plugin config: Missing tag "' + Tag.version + '"')
            return

        if not '{version}' in self.install_path:
            self.install_path_full = str(self.install_path)
            self.install_path_ok = True
            return

        self.install_path_full = str(self.install_path).format(version=self.version)
        '''
        self.install_path_full = str(self.install_path)
        self.install_path_ok = True

    def download(self):
        if not (self.url_ok and self.path_ok):
            # TODO: log plugin name?
            print('ERROR: Can not download Eclipse plugin installer.')

        '''
        NOTE: There is no ms5 file for PyDev plugin.
        For now hard code the md5sum: 
          722dfe4a9bf1f50a2766c4d58eb6dd4d
        TODO: Calculate own list of md5sums.
        '''
        #hard_code_md5_for_pydev = '722dfe4a9bf1f50a2766c4d58eb6dd4d'
        hard_code_md5_for_pydev = self.md5sum

        if util.is_file(self.installer_path):
            print('Eclipse plugin installer file exists.')
            print('Calculate md5sum')
            md5 = util.md5sum(self.installer_path, show_progress=True)
            # md5 = util.md5sum(self.installer_path, callback=util.print_progress)
            # md5 = util.md5sum(self.installer_path)
            print('md5 hash: ' + str(md5))
            '''
            if util.is_file(self.installer_path_md5):
                print('md5 file exists')
                if util.is_md5_in_file(self.installer_path_md5, md5):
            '''
            if True:
                if util.is_md5_equal(hard_code_md5_for_pydev, md5):
                    print('md5 is in file')
                    self.is_downloaded = True
                    return  # file is downloaded
                else:
                    print('md5 does not match')
                    print('download file again')

        print('Download Eclipse plugin installer.')
        util.download(self.installer_full_url, self.installer_path, show_progress=True)
        print('Download complete.')
        '''
        print('Download Eclipse plugin installer md5.')
        util.download(self.installer_full_url_md5, self.installer_path_md5)
        '''
        print('Calculate md5sum')
        md5 = util.md5sum(self.installer_path, show_progress=True)
        print('md5 hash: ' + str(md5))
        '''
        if util.is_file(self.installer_path_md5):
            print('md5 file exists')
            if util.is_md5_in_file(self.installer_path_md5, md5):
        '''
        if True:
            if util.is_md5_equal(hard_code_md5_for_pydev, md5):
                print('md5 is in file')
                self.is_downloaded = True
            else:
                print('md5 does not match')
                print('download failed !  TODO: interrupt the process?')
                self.is_downloaded = False

    def install(self):
        print('Start pydev installer.')
        print('Start ' + str(self.__name__) + ' ' + str(self.name) + ' installer.')
        print('')
        print(' Installing ... wait ... wait ... ')
        print('')
        # NOTE: This is "offline installer" ;)
        #print(str(_installer_file_fullname) + ' :: ' + str(_eclipse_path))
        #util.unzip(str(self.installer_path), str(self.install_path))
        util.unzip_py(str(self.installer_path), str(self.install_path))

        return True # TODO: return error?