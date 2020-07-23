# -*- coding: UTF-8 -*-
"""
    winmerge.py
    ~~~~~~~~~~~

    Install WinMerge

    License of this script file:
       MIT License

    License is available online:
      https://github.com/lordmikefin/setup_apps/blob/master/LICENSE

    Latest version of this script file:
      https://github.com/lordmikefin/setup_apps/blob/master/WinMerge.py


    :copyright: (c) 2020, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
    :license: MIT License
"""

from setup_apps.base import Base
from setup_apps.util import logger
from setup_apps.tag import Tag



# TODO: add WinMerge   https://winmerge.org/
# https://winmerge.org/downloads/
# https://downloads.sourceforge.net/winmerge/WinMerge-2.16.6-Setup.exe
# SHA-256 Checksums
# WinMerge-2.16.6-Setup.exe
#    b55de4fc99487e99ecb271a62e13ed6808b9ba3a96bf7d6b65cbee707b16fff1



class Winmerge(Base):

    def __init__(self):
        super().__init__()

        self.install_path_ok = False
        self.install_path = None
        self.install_path_full = None
        self.exe_file = None

        self.config = None
