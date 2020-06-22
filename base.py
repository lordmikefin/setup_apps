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
import app_source_handler
from setup_apps.util import logger
from setup_apps import util


class Checksum:

    class Type:
        NOT_SET = 0
        MD5SUM = 1
        SHA256SUM = 2

    def __init__(self):
        self.type = Checksum.Type.NOT_SET
        self.url = None
        self.file = None
        self.sum = None
        self.ok = False
        self.has_sum = False

    def set(self, url: str=None, file: str=None, summ: str=None,
            sum_type: int=None):
        if url and file:
            self.ok = True
        if summ:
            self.ok = True
            self.has_sum = True
        if sum_type:
            self.type = sum_type
        self.url = url
        self.file = file
        self.sum = summ

    def download(self):
        # TODO: was download successfull ?
        logger.info('Download hash file.')
        util.download(self.url, self.file)

    def is_hash_correct(self, hashsum: str) -> bool:
        # TODO: refactor
        if self.type == Checksum.Type.MD5SUM:
            if self.has_sum:
                if util.is_md5_equal(self.sum, hashsum):
                    return True
            self.download()
            if util.is_md5_in_file(self.file, hashsum):
                return True
        if self.type == Checksum.Type.SHA256SUM:
            if self.has_sum:
                if util.is_md5_equal(self.sum, hashsum):
                    return True
            self.download()
            if util.is_md5_in_file(self.file, hashsum):
                return True
        return False

    def create_hash(self, file_installer: str) -> str:
        hashsum = None
        if self.type == Checksum.Type.MD5SUM:
            logger.info('Calculate md5')
            hashsum = util.md5sum(file_installer, show_progress=True)
        if self.type == Checksum.Type.SHA256SUM:
            logger.info('Calculate sha256')
            hashsum = util.sha256(file_installer, show_progress=True)
        else:
            logger.error('Checksum type is not set.')
        return hashsum

class Base:
    def __init__(self):
        self.__name__ = self.__class__.__name__
        self.url_ok = False

        self.version = None
        self.installer_file = None
        self.installer_url = None
        self.installer_full_url = None

        # TODO: get md5/sha256 file from the sourse
        #self.installer_full_url_md5 = None
        #self.md5sum = None
        #self.sha256url = None
        self.checksum = None

        self.path_ok = False
        self.installer_path = None
        # TODO: get md5/sha256 file from the sourse
        self.installer_path_md5 = None

    def generate_all(self, source: dict):
        self.log_init()
        self.generate_full_url_from_source(source)
        logger.info('installer_full_url       : ' + str(self.installer_full_url))

        self.generate_installer_path()
        logger.info('installer_path           : ' + str(self.installer_path))

    def log_init(self):
        logger.info('Initialize application object: ' + self.__name__)

    def generate_installer_path(self):
        if not self.is_installer_file():
            return

        # file = str(self.installer_file).format(version=self.version)
        self.installer_path = PATH_INSTALLERS + self.installer_file

        # TODO: get md5/sha256 file from the sourse
        self.installer_path_md5 = self.installer_path + '.md5'
        self.path_ok = True

    def _insert_file_into_url(self, file: str):
        if '{version}' in self.installer_url:
            if self.version is None:
                logger.error('Incorrect ' + str(self.__name__) + ' config: Missing tag "' + Tag.version + '"')
                return
            self.installer_full_url = str(self.installer_url).format(
                installer_file=file, version=self.version)
        else:
            self.installer_full_url = str(self.installer_url).format(installer_file=file)

        # TODO: Is there always md5 file? Optional? REMOVE
        #self.installer_full_url_md5 = self.installer_full_url + '.md5'
        self.url_ok = True

    def is_installer_file(self) -> bool:
        if self.installer_file:
            return True

        logger.error('Incorrect ' + str(self.__name__) + ' config: Missing tag "' + Tag.installer_file + '"')
        return False

    def generate_full_url(self):
        if self.installer_url is None:
            logger.error('Incorrect ' + str(self.__name__) + ' config: Missing tag "' + Tag.installer_url + '"')
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
            logger.error('Incorrect ' + str(self.__name__) + ' config: Missing tag "' + Tag.version + '"')
            return

        self.installer_file = str(self.installer_file).format(version=self.version)
        self._insert_file_into_url(file=self.installer_file)
        #self.url_ok = True
        return

    def generate_full_url_from_source(self, source: dict):
        #app_source_handler.source.APPS
        #source = app_source_handler.source.APPS.get('eclipse', {})
        if not source:
            logger.error('the source xml failed.')
            logger.error('Get ' + str(self.__name__) + ' data from config xml.')
            self.generate_full_url()
            return
        #self.generate_full_url_from_source(source)

        #self.generate_full_url()
        if self.version is None:
            logger.error('Incorrect ' + str(self.__name__) + ' config: Missing tag "' + Tag.version + '"')
            return

        # TODO: if version is 'latest' then get ver from source
        if self.version == 'latest':
            latest = source.get('latest', {})
            self.version = latest
            logger.info('Latest version:  self.version: ' + str(self.version))
        vers = source.get('versions', {})
        ver = vers.get(self.version, {})
        url = ver.get('url', '')
        file = ver.get('file', '')

        md5url = ver.get('md5url', '')
        md5file = ver.get('md5file', '')
        md5sum = ver.get('md5sum', '')
        sha256url = ver.get('sha256url', '')
        sha256file = ver.get('sha256file', '')

        logger.info('url: ' + str(url))
        logger.info('file: ' + str(file))
        logger.info('md5url: ' + str(md5url))
        logger.info('md5file: ' + str(md5file))
        logger.info('md5sum: ' + str(md5sum))
        logger.info('sha256url: ' + str(sha256url))
        logger.info('sha256file: ' + str(sha256file))

        self.installer_full_url = url
        self.installer_file = file

        # TODO: set check sum in class with type
        #self.installer_full_url_md5 = md5url
        #self.md5sum = md5sum
        #self.sha256url = sha256url
        new_checksum = Checksum()
        if md5url or md5sum:
            new_checksum.set(url=md5url, file=md5file, summ=md5sum, sum_type=Checksum.Type.MD5SUM)
        if sha256url:
            new_checksum.set(url=sha256url, file=sha256file, sum_type=Checksum.Type.SHA256SUM)
        self.checksum = new_checksum

        self.set_url_ok()
        #self.url_ok = True
        return

    def set_url_ok(self):
        if not self.installer_file:
            logger.error('"installer_file" must be defined')
            return
        if not self.installer_full_url:
            logger.error('"installer_full_url" must be defined')
            return
        if not self.is_md5():
            logger.error('"installer_full_url_md5" or "md5sum" must be defined')
            return
        self.url_ok = True

    def is_md5(self):
        # TODO: is  'sha256url'
        if self.checksum:
            if self.checksum.ok:
                return True
        '''
        if self.installer_full_url_md5:
            return True
        if self.md5sum:
            return True
        if self.sha256url:
            return True
        '''
        return False
