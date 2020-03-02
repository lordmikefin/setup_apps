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

class Base:
    def __init__(self):
        self.__name__ = self.__class__.__name__
        self.url_ok = False

        self.version = None
        self.installer_file = None
        self.installer_url = None
        self.installer_full_url = None

    def generate_full_url(self):
        if self.installer_url is None:
            # TODO: log error
            #print('ERROR: Incorrect Eclipse config: Missing tag "installer_url"')
            #print('TEST : ' + str(self.__class__.__name__))
            #print('TEST : ' + str(self.__name__))
            print('ERROR: Incorrect ' + str(self.__name__) + ' config: Missing tag "installer_url"')
            return
