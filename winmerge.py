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

from . import PATH_INSTALLERS
from setup_apps import util


class Winmerge(Base):

    def __init__(self):
        super().__init__()

        self.install_path_ok = False
        self.install_path = None
        self.install_path_full = None
        self.exe_file = None

        self.config = None

    def generate_all(self, source: dict):
        super().generate_all(source)
        self.generate_install_path()
        logger.info('install_path_full        : ' + str(self.install_path_full))

        # TODO: this should be done in Base
        sum_obj = self.checksum #: :type sum_obj: Checksum
        self.installer_path_md5 = PATH_INSTALLERS + sum_obj.file
        logger.info('installer_path_md5        : ' + str(self.installer_path_md5))

    def generate_install_path(self):
        if self.install_path is None:
            logger.error('Incorrect WinMerge config: Missing tag "' + Tag.install_path + '"')
            return

        self.install_path_full = str(self.install_path)
        self.exe_file = self.install_path_full + '\\WinMergeU.exe'
        self.install_path_ok = True

    def download(self) -> bool:
        if not (self.url_ok and self.path_ok):
            logger.error('Can not download WinMerge installer.')
            return False

        if not self.checksum:
            logger.error('Checksum data missing.')
            return False

        if self.is_installer_downloaded(self.checksum):
            self.is_downloaded = True
            return True

        logger.info('Download WinMerge installer.')
        util.download(self.installer_full_url, self.installer_path, show_progress=True)
        logger.info('Download complete.')

        if self.is_installer_downloaded(self.checksum):
            logger.info('Download is verified.')
            self.is_downloaded = True
            return True

        logger.error('Download of WinMerge installer failed.')
        return False

    def is_installed(self):
        # TODO: how to update if version is different

        # NOTE: open command line guide
        # command = '"' + self.exe_file + '"' + ' /?'
        # TODO: how to check the version?

        if util.is_file(self.exe_file):
            logger.info('WinMerge already installed.')
            return True

        logger.info('WinMerge NOT installed.')
        return False

    def install(self) -> bool:
        if not self.is_downloaded:
            logger.error('WinMerge installer not downloaded.')
            return False

        if not self.install_path_ok:
            logger.error('Installation path not defined.')
            return False

        if self.is_installed():
            logger.info('WinMerge is already installed')
            return False

        logger.info('Start WinMerge installer.')
        logger.info('Installing ... wait ... wait ... ')

        # NOTE: auto install WinMerge
        # https://forums.winmerge.org/viewtopic.php?f=7&t=1743

        # READ MORE: Silent (unattended) install
        #   http://www.jrsoftware.org/ishelp/index.php?topic=setupcmdline

        command = self.installer_path + ' /SILENT '
        # TODO: Generate the inf file.
        #command = command + ' /LOADINF="...inf" '
        command = command + ' /LOG="winmerge-install.log" '
        command = command + ' /DIR="' + self.install_path_full + '"'
        test = util.run_os_command(command)
        if not test:
            logger.error('WinMerge installation FAILED.')
            return False

        logger.info('WinMerge installation done.')
        return True
