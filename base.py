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
from setup_apps.tag import Tag

class Base:
    def __init__(self):
        self.__name__ = self.__class__.__name__
        self.url_ok = False

        self.version = None
        self.installer_file = None
        self.installer_url = None
        self.installer_full_url = None

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
