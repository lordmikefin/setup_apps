# -*- coding: UTF-8 -*-
"""
    base.py
    ~~~~~~~

    Base class for apps.

    License of this script file:
       MIT License

    License is available online:
      https://github.com/lordmikefin/setup_apps/blob/master/LICENSE

    Latest version of this script file:
      https://github.com/lordmikefin/setup_apps/blob/master/base.py


    :copyright: (c) 2020, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
    :license: MIT License
"""
from . import PATH_INSTALLERS  # TODO: improve how installer path is defined
from setup_apps.tag import Tag

class Base:
    def __init__(self):
        self.__name__ = self.__class__.__name__
        self.url_ok = False

        self.version = None
        self.installer_file = None
        self.installer_url = None
        self.installer_full_url = None
        self.installer_full_url_md5 = None

        self.path_ok = False
        self.installer_path = None
        self.installer_path_md5 = None

    def generate_installer_path(self):
        if not self.is_installer_file():
            return

        # file = str(self.installer_file).format(version=self.version)
        self.installer_path = PATH_INSTALLERS + self.installer_file
        self.installer_path_md5 = self.installer_path + '.md5'
        self.path_ok = True

    def _insert_file_into_url(self, file: str):
        self.installer_full_url = str(self.installer_url).format(installer_file=file)
        self.installer_full_url_md5 = self.installer_full_url + '.md5'

    def is_installer_file(self) -> bool:
        if self.installer_file:
            return True

        # TODO: log error
        #print('ERROR: Incorrect Eclipse config: Missing tag "installer_file"')
        print('ERROR: Incorrect ' + str(self.__name__) + ' config: Missing tag "' + Tag.installer_file + '"')
        return False

    def generate_full_url(self):
        if self.installer_url is None:
            # TODO: log error
            #print('ERROR: Incorrect Eclipse config: Missing tag "installer_url"')
            #print('TEST : ' + str(self.__class__.__name__))
            #print('TEST : ' + str(self.__name__))
            #print('ERROR: Incorrect ' + str(self.__name__) + ' config: Missing tag "installer_url"')
            print('ERROR: Incorrect ' + str(self.__name__) + ' config: Missing tag "' + Tag.installer_url + '"')
            return

        if not '{installer_file}' in self.installer_url:
            self.installer_full_url = self.installer_url
            self.url_ok = True
            return

        if not self.is_installer_file():
            return

        if not '{version}' in self.installer_file:
            self._insert_file_into_url(file=self.installer_file)
            self.url_ok = True
            return

        if self.version is None:
            # TODO: log error
            print('ERROR: Incorrect ' + str(self.__name__) + ' config: Missing tag "' + Tag.version + '"')
            return

        self.installer_file = str(self.installer_file).format(version=self.version)
        self._insert_file_into_url(file=self.installer_file)
        self.url_ok = True
        return
