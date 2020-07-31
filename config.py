# -*- coding: UTF-8 -*-
"""
    config.py
    ~~~~~~~~~

    XML configuration file handler.

    License of this script file:
       MIT License

    License is available online:
      https://github.com/lordmikefin/setup_apps/blob/master/LICENSE

    Latest version of this script file:
      https://github.com/lordmikefin/setup_apps/blob/master/config.py


    :copyright: (c) 2020, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
    :license: MIT License
"""

import xml.etree.ElementTree as ET
from setup_apps import util, __version__, eclipse, PATH_INSTALLERS, java, npp,\
    putty, python, git, winmerge
from xml.etree.ElementTree import Element
from setup_apps.tag import Tag
import app_source_handler
import json
from .util import logger
from setup_apps.base import Base
import LMToyBoxPython
# NOTE: we need "unused" imports for Sphinx Documentation generator comment lines :)
from typing import List
from setup_apps.eclipse import Eclipse
from setup_apps.java import Java
from setup_apps.npp import Npp
from setup_apps.putty import Putty
from setup_apps.python import Python
import os
from LMToyBoxPython import LMetree, LMhashlib
from setup_apps.git import Git
from setup_apps.winmerge import Winmerge
#from lxml import etree as ET
#import lxml.etree as ET
# TODO: remove 'lxml' from requirements


CONFIG_PATH = util.fix_path(util.home_path() + '/LM_ToyBox/setup_apps')
CONFIG_FILE = 'setup_apps_config.xml'

XML_CONFIG = 'xml_config.xml'
XML_TEST = 'test.xml'

# https://stackabuse.com/reading-and-writing-xml-files-in-python/

# https://docs.python.org/3.7/library/xml.etree.elementtree.html

# https://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
# https://lxml.de/index.html
# https://pypi.org/project/lxml/


def create_sample():
    file = util.fix_path(CONFIG_PATH + '/' + CONFIG_FILE)
    logger.info('create the sample config XML file: ' + str(file))
    root = ET.Element(Tag.setup)
    tree = ET.ElementTree(root)

    root.append(ET.Comment(' Supported version of "setup_apps" '))
    LMetree.create_subelem(root, Tag.version, __version__)

    apps = ET.SubElement(root, Tag.apps)
    plugins = [
        {
            'name': 'pydev',
            'version': 'latest',
        }
    ]
    append_eclipse(apps, ver='latest', plugins=plugins)
    #append_eclipse(apps, '2019-09')

    plugins = [
        {
            'name': 'pydev',
            'version': '7.4.0',
        }
    ]

    append_eclipse(apps, ver='2019-09', plugins=plugins)

    #append_java(apps, ver='8u242b08')
    append_java(apps, ver='jdk-8.0.242.08-hotspot')

    # Notepad ++
    append_npp(apps, ver='7.7.1')

    # Putty
    append_putty(apps, ver='0.73')

    # Python
    append_python(apps, ver='3.8.1')

    # Git
    append_git(apps, ver='2.24.1')

    # WinMerge
    append_winmerge(apps, ver='2.16.6')

    LMetree.indent(root)
    util.mkdir(CONFIG_PATH)
    tree.write(file, encoding="UTF-8", xml_declaration=True)


def set_version(elem: Element, ver: str):
    LMetree.create_subelem(elem, Tag.version, ver)


def set_install_path(elem: Element, path: str):
    LMetree.create_subelem(elem, Tag.install_path, path)


def append_winmerge(apps: Element, ver: str):
    elem = ET.SubElement(apps, Tag.winmerge)
    set_version(elem, ver)
    set_install_path(elem, 'C:\\Program Files\\WinMerge')

def append_git(apps: Element, ver: str):
    elem = ET.SubElement(apps, Tag.git)
    set_version(elem, ver)
    set_install_path(elem, 'C:\\Program Files\\Git')
    append_console_configure(elem)

def append_console_configure(elem: Element):
    configure = ET.SubElement(elem, Tag.configure)
    configure_console = ET.SubElement(configure, Tag.console)
    configure_console.append(ET.Comment(' {git_exe_full_path} is replaced with value from tag "install_path" + hardcoded .\\bin\\git.exe '))
    #command = ET.SubElement(configure_console, Tag.command) #: :type command: Element
    #command.text = '{git_exe_full_path} config --global user.name "Lord Mike"'
    append_command_elem(configure_console, '{git_exe_full_path} config --global user.name "Lord Mike"')
    #command2 = ET.SubElement(configure_console, Tag.command) #: :type command2: Element
    #command2.text = '{git_exe_full_path} config --global user.email lordmike@iki.fi'
    append_command_elem(configure_console, '{git_exe_full_path} config --global user.email lordmike@iki.fi')

def append_command_elem(elem_parent: Element, command: str):
    LMetree.create_subelem(elem_parent, Tag.command, command)

def append_python(apps: Element, ver: str):
    elem = ET.SubElement(apps, Tag.python)
    set_version(elem, ver)
    # TODO: parse marjor and minor numbers from version
    marjor = '3'
    minor = '8'
    set_install_path(elem, 'C:\\Program Files\\Python' + marjor + minor)


def append_putty(apps: Element, ver: str):
    npp_elem = ET.SubElement(apps, Tag.putty)
    set_version(npp_elem, ver)
    set_install_path(npp_elem, 'C:\\Program Files\\PuTTY')
    append_env_configure(npp_elem)

def append_env_configure(elem: Element):
    configure = ET.SubElement(elem, Tag.configure)
    configure_enviroment = ET.SubElement(configure, Tag.enviroment)
    configure_enviroment.append(ET.Comment('"' + str(Tag.enviroment) + '" element content is set into windows environmet variables'))
    #configure_enviroment.append(ET.Comment(' {plink_exe_full_path}  is replaced with value from tag "install_path" + hardcoded .\\plink.exe '))
    #append_command_elem(configure_enviroment, 'GIT_SSH {plink_exe_full_path}')
    key_values = ET.SubElement(configure_enviroment, Tag.key_values)
    key_value = ET.SubElement(key_values, Tag.key_value)
    LMetree.create_subelem(key_value, Tag.key, 'GIT_SSH')
    key_value.append(ET.Comment(' {plink_exe_full_path}  is replaced with value from tag "install_path" + hardcoded .\\plink.exe '))
    LMetree.create_subelem(key_value, Tag.value, '{plink_exe_full_path}')


def append_npp(apps: Element, ver: str):
    npp_elem = ET.SubElement(apps, Tag.npp)
    set_version(npp_elem, ver)
    set_install_path(npp_elem, 'C:\\Program Files\\Notepad++')


def append_java(apps: Element, ver: str):
    java_elem = ET.SubElement(apps, Tag.java)
    #version_elem = ET.SubElement(java_elem, Tag.version)
    #version_elem.text = ver
    set_version(java_elem, ver)
    java_elem.append(ET.Comment(' {version} is replaced with value from tag "version" '))
    #install_path = ET.SubElement(java_elem, Tag.install_path)
    #install_path.text = 'C:\\Program Files\\AdoptOpenJDK\\{version}'
    set_install_path(java_elem, 'C:\\Program Files\\AdoptOpenJDK\\{version}')


def append_eclipse(apps: Element, ver: str, plugins: list):
    ecli_elem = ET.SubElement(apps, Tag.eclipse)
    #version_elem = ET.SubElement(ecli_elem, Tag.version)
    # NOTE: use latest version from the source
    #version_elem.text = '2019-09'
    #version_elem.text = 'latest'
    #version_elem.text = ver
    set_version(ecli_elem, ver)
    '''
    ecli_elem.append(ET.Comment(' {version} is replaced with value from tag "version" '))
    installer_file = ET.SubElement(ecli_elem, Tag.installer_file)
    installer_file.text = 'eclipse-javascript-{version}-R-win32-x86_64.zip'
    ecli_elem.append(ET.Comment(' {installer_file} is replaced with value from tag "installer_file" '))
    installer_url = ET.SubElement(ecli_elem, Tag.installer_url)
    installer_url.text = 'https://ftp.acc.umu.se/mirror/eclipse.org/technology/epp/downloads/release/2019-09/R/{installer_file}'
    '''
    # TODO: is there better solution? extract to temp?
    # NOTE: while extracting I got path too long error -> changed install path
    ecli_elem.append(ET.Comment(' {version} is replaced with value from tag "version" '))
    #install_path = ET.SubElement(ecli_elem, Tag.install_path)
    #install_path.text = 'C:\\Program Files\\eclipse-{version}'
    #install_path.text = 'C:\\Program Files\\e-{version}'
    set_install_path(ecli_elem, 'C:\\Program Files\\eclipse-{version}')
    append_configure(ecli_elem)
    for plugin in plugins:
        # TODO: get name and version
        name = plugin.get('name')
        version = plugin.get('version')
        #append_plugins(ecli_elem, name='pydev', ver='latest')
        append_plugins(ecli_elem, name, version)


def append_configure(ecli_elem: Element):
    configure = ET.SubElement(ecli_elem, Tag.configure)
    configure.append(ET.Comment(' "file" is realative path of "install_path" '))
    configure_file = ET.SubElement(configure, Tag.file)
    LMetree.create_subelem(configure_file, Tag.name, '\\eclipse.ini')
    file_type = ET.SubElement(configure_file, Tag.type)
    file_type.text = 'ini'
    key_values = ET.SubElement(configure_file, Tag.key_values)
    key_value = ET.SubElement(key_values, Tag.key_value)
    key = ET.SubElement(key_value, Tag.key)
    key.text = '-Dosgi.instance.area.default'
    key_value.append(ET.Comment(' {version} is replaced with value from tag "version" '))
    value = ET.SubElement(key_value, Tag.value)
    #value.text = '@user.home/eclipse-workspace-2019-09'
    value.text = '@user.home/eclipse-workspace-{version}'

    #    <file>
    #      <name>C:\Users\lordmike\eclipse-workspace-2019-12\.metadata\.plugins\org.eclipse.core.runtime\.settings\org.eclipse.egit.core.prefs</name>
    #      <type>prefs</type>
    #      <key_values>
    #        <key_value>
    #          <key>core_defaultRepositoryDir</key>
    #          <value>${workspace_loc}</value>
    #        </key_value>
    #      </key_values>
    #    </file>
    configure_file_egit = ET.SubElement(configure, Tag.file)
    configure_file_egit.append(ET.Comment(' {version} is replaced with value from tag "version" '))
    configure_file_egit.append(ET.Comment(' {user_home} is replaced with path to current user home '))
    #name.text = 'C:\\Users\\lordmike\\eclipse-workspace-2019-12\\.metadata\\.plugins\\org.eclipse.core.runtime\\.settings\\org.eclipse.egit.core.prefs'
    #name.text = 'C:\\Users\\lordmike\\eclipse-workspace-{version}\\.metadata\\.plugins\\org.eclipse.core.runtime\\.settings\\org.eclipse.egit.core.prefs'
    LMetree.create_subelem(configure_file_egit, Tag.name,
                           '{user_home}\\eclipse-workspace-{version}\\.metadata\\.plugins\\org.eclipse.core.runtime\\.settings\\org.eclipse.egit.core.prefs')
    LMetree.create_subelem(configure_file_egit, Tag.type, 'prefs')
    key_values_egit = ET.SubElement(configure_file_egit, Tag.key_values)
    key_value_egit = ET.SubElement(key_values_egit, Tag.key_value)
    LMetree.create_subelem(key_value_egit, Tag.key, 'core_defaultRepositoryDir')
    key_value_egit.append(ET.Comment(' ${workspace_loc} is internal varable of Eclipse'))
    LMetree.create_subelem(key_value_egit, Tag.value, '${workspace_loc}')

    # auto load repo
    # TODO: how to use ssh? need to auto set ssh key, but how?
    # git@github.com:lordmikefin/testground_setup_apps.git
    configure_console = ET.SubElement(configure, Tag.console)
    configure_console.append(ET.Comment(' {git_exe} is replaced with value "git.exe" '))
    configure_console.append(ET.Comment(' {version} is replaced with value from tag "version" '))
    home = util.home_path()
    home_fixed = home.replace('\\', '\\\\').replace(':', '\\:')
    append_command_elem(configure_console, '{git_exe} clone https://github.com/lordmikefin/testground_setup_apps.git "' + home + '\\eclipse-workspace-{version}\\testground_setup_apps"')

    # load submodules of the repo
    configure_console.append(ET.Comment(' run submodule commands after "clone" command '))
    configure_console.append(ET.Comment(' {git_exe} is replaced with value "git.exe" '))
    #configure_console.append(ET.Comment(' {user_home_fixed} is replaced with path to current user home '))
    configure_console.append(ET.Comment(' {version} is replaced with value from tag "version" '))
    append_command_elem(configure_console, 'cd "' + home + '\\eclipse-workspace-{version}\\testground_setup_apps" && {git_exe} submodule init')
    append_command_elem(configure_console, 'cd "' + home + '\\eclipse-workspace-{version}\\testground_setup_apps" && {git_exe} submodule update')

    # TODO: use ssh
    # git remote set-url origin git@github.com:lordmikefin/setup_apps.git
    # git remote set-url origin git@github.com:lordmikefin/app_source_handler.git
    # git@github.com:lordmikefin/LMToyBoxPython.git

    # Define git repo locations
    # TODO: append the path to value - do not replace
    key_value_egit1 = ET.SubElement(key_values_egit, Tag.key_value)
    LMetree.create_subelem(key_value_egit1, Tag.key, 'GitRepositoriesView.GitDirectories')
    key_value_egit1.append(ET.Comment(' {version} is replaced with value from tag "version" '))
    #LMetree.create_subelem(key_value_egit1, Tag.value, 'C\\:\\\\Users\\\\lordmike\\\\eclipse-workspace-2019-09\\\\testground_setup_apps\\\\.git;')
    LMetree.create_subelem(key_value_egit1, Tag.value, '' + home_fixed + '\\\\eclipse-workspace-{version}\\\\testground_setup_apps\\\\.git;')

    key_value_egit2 = ET.SubElement(key_values_egit, Tag.key_value)
    LMetree.create_subelem(key_value_egit2, Tag.key, 'GitRepositoriesView.GitDirectories.relative')
    LMetree.create_subelem(key_value_egit2, Tag.value, 'testground_setup_apps\\\\.git;')

    # Define python interpreter
    configure_file_pydev = ET.SubElement(configure, Tag.file)
    configure_file_pydev.append(ET.Comment(' {version} is replaced with value from tag "version" '))
    configure_file_pydev.append(ET.Comment(' {user_home} is replaced with path to current user home '))
    LMetree.create_subelem(configure_file_pydev, Tag.name,
                       '{user_home}\\eclipse-workspace-{version}\\.metadata\\.plugins\\org.eclipse.core.runtime\\.settings\\org.python.pydev.prefs')
    LMetree.create_subelem(configure_file_pydev, Tag.type, 'prefs')
    key_values_pydev = ET.SubElement(configure_file_pydev, Tag.key_values)
    key_value_pydev = ET.SubElement(key_values_pydev, Tag.key_value)
    LMetree.create_subelem(key_value_pydev, Tag.key, 'INTERPRETER_PATH_NEW')
    #key_value_pydev.append(ET.Comment(' {user_home} is replaced with path to current user home '))
    #home = util.home_path()
    #home_fixed = home.replace('\\', '\\\\').replace(':', '\\:')
    LMetree.create_subelem(key_value_pydev, Tag.value,
         #'<xml>\n<name>python37_venv_setup_apps</name>\n<version>3.7</version>\n<executable>C\:\\Users\\lordmike\\Envs\\venv-LMAutoSetBotWin\\Scripts\\python.exe</executable>\n<lib>c\:\\program files\\python37\\DLLs</lib>\n<lib>c\:\\program files\\python37\\lib</lib>\n<lib>c\:\\program files\\python37</lib>\n<lib>C\:\\Users\\lordmike\\Envs\\venv-LMAutoSetBotWin</lib>\n<lib>C\:\\Users\\lordmike\\Envs\\venv-LMAutoSetBotWin\\lib\\site-packages</lib>\n<forced_lib>Image</forced_lib>\n<forced_lib>OpenGL</forced_lib>\n<forced_lib>_abc</forced_lib>\n<forced_lib>_ast</forced_lib>\n<forced_lib>_bisect</forced_lib>\n<forced_lib>_blake2</forced_lib>\n<forced_lib>_bytesio</forced_lib>\n<forced_lib>_codecs</forced_lib>\n<forced_lib>_codecs_cn</forced_lib>\n<forced_lib>_codecs_hk</forced_lib>\n<forced_lib>_codecs_iso2022</forced_lib>\n<forced_lib>_codecs_jp</forced_lib>\n<forced_lib>_codecs_kr</forced_lib>\n<forced_lib>_codecs_tw</forced_lib>\n<forced_lib>_collections</forced_lib>\n<forced_lib>_contextvars</forced_lib>\n<forced_lib>_csv</forced_lib>\n<forced_lib>_datetime</forced_lib>\n<forced_lib>_fileio</forced_lib>\n<forced_lib>_functools</forced_lib>\n<forced_lib>_heapq</forced_lib>\n<forced_lib>_hotshot</forced_lib>\n<forced_lib>_imp</forced_lib>\n<forced_lib>_io</forced_lib>\n<forced_lib>_json</forced_lib>\n<forced_lib>_locale</forced_lib>\n<forced_lib>_lsprof</forced_lib>\n<forced_lib>_md5</forced_lib>\n<forced_lib>_multibytecodec</forced_lib>\n<forced_lib>_opcode</forced_lib>\n<forced_lib>_operator</forced_lib>\n<forced_lib>_pickle</forced_lib>\n<forced_lib>_random</forced_lib>\n<forced_lib>_sha</forced_lib>\n<forced_lib>_sha1</forced_lib>\n<forced_lib>_sha256</forced_lib>\n<forced_lib>_sha3</forced_lib>\n<forced_lib>_sha512</forced_lib>\n<forced_lib>_signal</forced_lib>\n<forced_lib>_sre</forced_lib>\n<forced_lib>_stat</forced_lib>\n<forced_lib>_string</forced_lib>\n<forced_lib>_struct</forced_lib>\n<forced_lib>_subprocess</forced_lib>\n<forced_lib>_symtable</forced_lib>\n<forced_lib>_thread</forced_lib>\n<forced_lib>_tracemalloc</forced_lib>\n<forced_lib>_warnings</forced_lib>\n<forced_lib>_weakref</forced_lib>\n<forced_lib>_winapi</forced_lib>\n<forced_lib>_winreg</forced_lib>\n<forced_lib>array</forced_lib>\n<forced_lib>atexit</forced_lib>\n<forced_lib>audioop</forced_lib>\n<forced_lib>binascii</forced_lib>\n<forced_lib>builtins</forced_lib>\n<forced_lib>cPickle</forced_lib>\n<forced_lib>cStringIO</forced_lib>\n<forced_lib>cmath</forced_lib>\n<forced_lib>cv2</forced_lib>\n<forced_lib>datetime</forced_lib>\n<forced_lib>email</forced_lib>\n<forced_lib>errno</forced_lib>\n<forced_lib>exceptions</forced_lib>\n<forced_lib>faulthandler</forced_lib>\n<forced_lib>future_builtins</forced_lib>\n<forced_lib>gc</forced_lib>\n<forced_lib>gi</forced_lib>\n<forced_lib>hashlib</forced_lib>\n<forced_lib>imageop</forced_lib>\n<forced_lib>imp</forced_lib>\n<forced_lib>itertools</forced_lib>\n<forced_lib>marshal</forced_lib>\n<forced_lib>math</forced_lib>\n<forced_lib>mmap</forced_lib>\n<forced_lib>mock</forced_lib>\n<forced_lib>msvcrt</forced_lib>\n<forced_lib>multiprocessing</forced_lib>\n<forced_lib>mutagen</forced_lib>\n<forced_lib>nt</forced_lib>\n<forced_lib>numpy</forced_lib>\n<forced_lib>operator</forced_lib>\n<forced_lib>os</forced_lib>\n<forced_lib>os.path</forced_lib>\n<forced_lib>parser</forced_lib>\n<forced_lib>pytest</forced_lib>\n<forced_lib>scipy</forced_lib>\n<forced_lib>signal</forced_lib>\n<forced_lib>six</forced_lib>\n<forced_lib>socket</forced_lib>\n<forced_lib>ssl</forced_lib>\n<forced_lib>strop</forced_lib>\n<forced_lib>sys</forced_lib>\n<forced_lib>thread</forced_lib>\n<forced_lib>time</forced_lib>\n<forced_lib>winreg</forced_lib>\n<forced_lib>wx</forced_lib>\n<forced_lib>wxPython</forced_lib>\n<forced_lib>xxsubtype</forced_lib>\n<forced_lib>zipimport</forced_lib>\n<forced_lib>zlib</forced_lib>\n<string_substitution_var><key>PY</key><value>37</value></string_substitution_var>\n</xml>&&&&&')
         '<xml>\\n<name>python37_venv_setup_apps</name>\\n<version>3.7</version>\\n' +\
         '<executable>' + home_fixed + '\\\\Envs\\\\venv-LMAutoSetBotWin\\\\Scripts\\\\python.exe</executable>\\n' +\
         '<lib>c\\:\\\\program files\\\\python37\\\\DLLs</lib>\\n' +\
         '<lib>c\\:\\\\program files\\\\python37\\\\lib</lib>\\n' +\
         '<lib>c\\:\\\\program files\\\\python37</lib>\\n' +\
         '<lib>' + home_fixed + '\\\\Envs\\\\venv-LMAutoSetBotWin</lib>\\n' +\
         '<lib>' + home_fixed + '\\\\Envs\\\\venv-LMAutoSetBotWin\\\\lib\\\\site-packages</lib>\\n' +\
         '<forced_lib>Image</forced_lib>\\n<forced_lib>OpenGL</forced_lib>\\n<forced_lib>_abc</forced_lib>\\n<forced_lib>_ast</forced_lib>\\n<forced_lib>_bisect</forced_lib>\\n<forced_lib>_blake2</forced_lib>\\n<forced_lib>_bytesio</forced_lib>\\n<forced_lib>_codecs</forced_lib>\\n<forced_lib>_codecs_cn</forced_lib>\\n<forced_lib>_codecs_hk</forced_lib>\\n<forced_lib>_codecs_iso2022</forced_lib>\\n<forced_lib>_codecs_jp</forced_lib>\\n<forced_lib>_codecs_kr</forced_lib>\\n<forced_lib>_codecs_tw</forced_lib>\\n<forced_lib>_collections</forced_lib>\\n<forced_lib>_contextvars</forced_lib>\\n<forced_lib>_csv</forced_lib>\\n<forced_lib>_datetime</forced_lib>\\n<forced_lib>_fileio</forced_lib>\\n<forced_lib>_functools</forced_lib>\\n<forced_lib>_heapq</forced_lib>\\n<forced_lib>_hotshot</forced_lib>\\n<forced_lib>_imp</forced_lib>\\n<forced_lib>_io</forced_lib>\\n<forced_lib>_json</forced_lib>\\n<forced_lib>_locale</forced_lib>\\n<forced_lib>_lsprof</forced_lib>\\n<forced_lib>_md5</forced_lib>\\n<forced_lib>_multibytecodec</forced_lib>\\n<forced_lib>_opcode</forced_lib>\\n<forced_lib>_operator</forced_lib>\\n<forced_lib>_pickle</forced_lib>\\n<forced_lib>_random</forced_lib>\\n<forced_lib>_sha</forced_lib>\\n<forced_lib>_sha1</forced_lib>\\n<forced_lib>_sha256</forced_lib>\\n<forced_lib>_sha3</forced_lib>\\n<forced_lib>_sha512</forced_lib>\\n<forced_lib>_signal</forced_lib>\\n<forced_lib>_sre</forced_lib>\\n<forced_lib>_stat</forced_lib>\\n<forced_lib>_string</forced_lib>\\n<forced_lib>_struct</forced_lib>\\n<forced_lib>_subprocess</forced_lib>\\n<forced_lib>_symtable</forced_lib>\\n<forced_lib>_thread</forced_lib>\\n<forced_lib>_tracemalloc</forced_lib>\\n<forced_lib>_warnings</forced_lib>\\n<forced_lib>_weakref</forced_lib>\\n<forced_lib>_winapi</forced_lib>\\n<forced_lib>_winreg</forced_lib>\\n<forced_lib>array</forced_lib>\\n<forced_lib>atexit</forced_lib>\\n<forced_lib>audioop</forced_lib>\\n<forced_lib>binascii</forced_lib>\\n<forced_lib>builtins</forced_lib>\\n<forced_lib>cPickle</forced_lib>\\n<forced_lib>cStringIO</forced_lib>\\n<forced_lib>cmath</forced_lib>\\n<forced_lib>cv2</forced_lib>\\n<forced_lib>datetime</forced_lib>\\n<forced_lib>email</forced_lib>\\n<forced_lib>errno</forced_lib>\\n<forced_lib>exceptions</forced_lib>\\n<forced_lib>faulthandler</forced_lib>\\n<forced_lib>future_builtins</forced_lib>\\n<forced_lib>gc</forced_lib>\\n<forced_lib>gi</forced_lib>\\n<forced_lib>hashlib</forced_lib>\\n<forced_lib>imageop</forced_lib>\\n<forced_lib>imp</forced_lib>\\n<forced_lib>itertools</forced_lib>\\n<forced_lib>marshal</forced_lib>\\n<forced_lib>math</forced_lib>\\n<forced_lib>mmap</forced_lib>\\n<forced_lib>mock</forced_lib>\\n<forced_lib>msvcrt</forced_lib>\\n<forced_lib>multiprocessing</forced_lib>\\n<forced_lib>mutagen</forced_lib>\\n<forced_lib>nt</forced_lib>\\n<forced_lib>numpy</forced_lib>\\n<forced_lib>operator</forced_lib>\\n<forced_lib>os</forced_lib>\\n<forced_lib>os.path</forced_lib>\\n<forced_lib>parser</forced_lib>\\n<forced_lib>pytest</forced_lib>\\n<forced_lib>scipy</forced_lib>\\n<forced_lib>signal</forced_lib>\\n<forced_lib>six</forced_lib>\\n<forced_lib>socket</forced_lib>\\n<forced_lib>ssl</forced_lib>\\n<forced_lib>strop</forced_lib>\\n<forced_lib>sys</forced_lib>\\n<forced_lib>thread</forced_lib>\\n<forced_lib>time</forced_lib>\\n<forced_lib>winreg</forced_lib>\\n<forced_lib>wx</forced_lib>\\n<forced_lib>wxPython</forced_lib>\\n<forced_lib>xxsubtype</forced_lib>\\n<forced_lib>zipimport</forced_lib>\\n<forced_lib>zlib</forced_lib>\\n' +\
         '<string_substitution_var><key>PY</key><value>37</value></string_substitution_var>\\n</xml>&&&&&')



def append_plugins(ecli_elem: Element, name: str, ver: str):
    plugins = ET.SubElement(ecli_elem, Tag.plugins)
    plugin = ET.SubElement(plugins, Tag.plugin)
    #plugin_pydev = ET.SubElement(plugin, Tag.plugin_pydev)
    plugin_pydev = plugin  # TODO: is there realy need for separate tag for each plugin?
    # TODO: how to share plugin names elegantly between 'setup_apps' and 'app_source'?
    # NOTE: for now it is hard code :(
    #name_elem.text = 'pydev'
    LMetree.create_subelem(plugin_pydev, Tag.name, name)
    # NOTE: use latest version from the source
    #version.text = '7.4.0'
    #version.text = 'latest'
    LMetree.create_subelem(plugin_pydev, Tag.version, ver)
    '''
    plugin_pydev.append(ET.Comment(' {version} is replaced with value from tag "version" '))
    installer_file = ET.SubElement(plugin_pydev, Tag.installer_file)
    #installer_file.text = 'PyDev%20{version}.zip'
    installer_file.text = 'PyDev {version}.zip'
    plugin_pydev.append(ET.Comment(' {installer_file} is replaced with value from tag "installer_file" '))
    installer_url = ET.SubElement(plugin_pydev, Tag.installer_url)
    installer_url.text = 'https://sourceforge.net/projects/pydev/files/pydev/PyDev%20{version}/{installer_file}/download'
    '''
    #plugin_pydev.append(ET.Comment(' {version} is replaced with value from tag "version" '))
    #install_path = ET.SubElement(plugin_pydev, Tag.install_path)
    # TODO: get this path from eclipse
    #install_path.text = 'C:\\Program Files\\eclipse-{version}'
    #install_path.text = '\\eclipse-{version}'
    # TODO: Jar file location is needed for "is_instelled" check
    #_jar_file = _eclipse_path + '\\plugins\\org.python.pydev_7.4.0.201910251334\\pydev.jar'


def parse(source_file: str=''):
    download_source_xml()
    parse_source_xml(source_file)
    logger.info('parse the config XML file')
    file = util.fix_path(CONFIG_PATH + '/' + CONFIG_FILE)
    tree = ET.parse(file)
    root = tree.getroot()
    for elem in root: #: :type elem: Element
        # TODO: check version
        if elem.tag == Tag.apps:
            parse_apps(elem)


SOURCE_FILE = util.fix_path(PATH_INSTALLERS + '/' + 'app_source.xml')
SOURCE_FILE_OK = False
def download_source_xml():
    global SOURCE_FILE_OK
    logger.info('download the source XML file')
    file = SOURCE_FILE
    url = 'https://raw.githubusercontent.com/lordmikefin/app_source/master/app_source.xml'
    util.download(url, file, show_progress=True)
    # TODO: download app_source.xml.sha256 file
    file_sha = util.fix_path(PATH_INSTALLERS + '/' + 'app_source.xml.sha256')
    url_sha = 'https://raw.githubusercontent.com/lordmikefin/app_source/master/app_source.xml.sha256'
    util.download(url_sha, file_sha)
    hashsum = LMhashlib.sha256(file, show_progress=True)

    # verification with md5sum
    if util.is_md5_in_file(file_sha, hashsum, SOURCE_FILE):
        SOURCE_FILE_OK = True


def parse_source_xml(source_file: str=''):
    logger.info('parse the source XML file')
    # app_source_handler.source.parse(source_file)
    if SOURCE_FILE_OK:
        app_source_handler.source.parse(SOURCE_FILE)
        logger.debug('APPS: \n' + json.dumps(app_source_handler.source.APPS,
                                     sort_keys=True, indent=2))
    else:
        logger.error('parsing failed')


def parse_apps(elem_apps: Element):
    for elem in elem_apps: #: :type elem: Element
        if elem.tag == Tag.eclipse:
            parse_eclipse(elem)
        if elem.tag == Tag.java:
            parse_java(elem)
        if elem.tag == Tag.npp:
            parse_npp(elem)
        if elem.tag == Tag.putty:
            parse_putty(elem)
        if elem.tag == Tag.python:
            parse_python(elem)
        if elem.tag == Tag.git:
            parse_git(elem)
        if elem.tag == Tag.winmerge:
            parse_winmerge(elem)


def parse_version(elem: Element, base_obj: Base):
    elem_version = elem.find(Tag.version)
    if not elem_version is None:
        base_obj.version = elem_version.text

def parse_install_path(elem: Element, base_obj: Base):
    elem_path = elem.find(Tag.install_path)
    if not elem_path is None:
        base_obj.install_path = elem_path.text


def append_app(app_name: str, app_obj: Base):
    global APPS
    obj_list = list(APPS.get(app_name, []))
    obj_list.append(app_obj)
    APPS[app_name] = obj_list


def parse_winmerge(elem: Element):
    global APPS

    obj = winmerge.Winmerge()
    logger.info('parse git             : ' + str(obj.__name__))
    parse_version(elem, obj)
    parse_install_path(elem, obj)
    logger.info('version                  : ' + str(obj.version))
    logger.info('install_path             : ' + str(obj.install_path))
    append_app('winmerge', obj)


def parse_git(elem: Element):
    global APPS

    obj = git.Git()
    logger.info('parse git             : ' + str(obj.__name__))
    parse_version(elem, obj)
    parse_install_path(elem, obj)
    logger.info('version                  : ' + str(obj.version))
    logger.info('install_path             : ' + str(obj.install_path))

    configure = elem.find(Tag.configure)
    if not configure is None:
        conf_file_list = []
        obj.config = conf_file_list
        parse_configure(configure, conf_file_list)

    append_app('git', obj)


def parse_python(elem: Element):
    global APPS

    obj = python.Python()
    logger.info('parse python             : ' + str(obj.__name__))
    parse_version(elem, obj)
    parse_install_path(elem, obj)
    logger.info('version                  : ' + str(obj.version))
    logger.info('install_path             : ' + str(obj.install_path))
    append_app('python', obj)


def parse_putty(elem: Element):
    global APPS

    obj = putty.Putty()
    logger.info('parse putty              : ' + str(obj.__name__))
    parse_version(elem, obj)
    parse_install_path(elem, obj)
    logger.info('version                  : ' + str(obj.version))
    logger.info('install_path             : ' + str(obj.install_path))

    configure = elem.find(Tag.configure)
    if not configure is None:
        conf_file_list = []
        obj.config = conf_file_list
        parse_configure(configure, conf_file_list)

    append_app('putty', obj)


def parse_npp(elem: Element):
    global APPS

    npp_obj = npp.Npp()
    logger.info('parse app                : ' + str(npp_obj.__name__))
    parse_version(elem, npp_obj)
    parse_install_path(elem, npp_obj)
    logger.info('version                  : ' + str(npp_obj.version))
    logger.info('install_path             : ' + str(npp_obj.install_path))
    append_app('npp', npp_obj)


def parse_java(elem: Element):
    global APPS

    java_obj = java.Java()
    logger.info('parse app                : ' + str(java_obj.__name__))
    #elem_version = elem.find(Tag.version)
    #if not elem_version is None:
    #    java_obj.version = elem_version.text
    parse_version(elem, java_obj)

    #elem_path = elem.find(Tag.install_path)
    #if not elem_path is None:
    #    java_obj.install_path = elem_path.text
    parse_install_path(elem, java_obj)

    logger.info('version                  : ' + str(java_obj.version))
    logger.info('install_path             : ' + str(java_obj.install_path))

    #java_list = list(APPS.get('java', []))
    #java_list.append(java_obj)
    #APPS['java'] = java_list
    append_app('java', java_obj)


def parse_eclipse(elem: Element):
    global APPS

    ecli = eclipse.Eclipse()
    logger.info('parse app                : ' + str(ecli.__name__))
    #elem_version = elem.find(Tag.version)
    #if not elem_version is None:
    #    ecli.version = elem_version.text
    parse_version(elem, ecli)

    elem_file = elem.find(Tag.installer_file)
    if not elem_file is None:
        ecli.installer_file = elem_file.text
    elem_url = elem.find(Tag.installer_url)
    if not elem_url is None:
        ecli.installer_url = elem_url.text
    #elem_path = elem.find(Tag.install_path)
    #if not elem_path is None:
    #    ecli.install_path = elem_path.text
    parse_install_path(elem, ecli)

    logger.info('version                  : ' + str(ecli.version))
    logger.info('installer_file           : ' + str(ecli.installer_file))
    logger.info('installer_url            : ' + str(ecli.installer_url))
    logger.info('installer_full_url       : ' + str(ecli.installer_full_url))

    #ecli.generate_all()

    configure = elem.find(Tag.configure)
    if not configure is None:
        conf_file_list = []
        ecli.config = conf_file_list
        parse_configure(configure, conf_file_list)

    plugins = elem.find(Tag.plugins)
    if not plugins is None:
        plugins_list = []
        ecli.plugins = plugins_list
        parse_plugins(plugins, plugins_list)
        #ecli.init_plugins()

    #eclipse_list = list(APPS.get('eclipse', []))
    #eclipse_list.append(ecli)
    #APPS['eclipse'] = eclipse_list
    append_app('eclipse', ecli)


def parse_plugins(plugins: Element, plugins_list: list):
    logger.info('Has plugins')
    for elem in plugins:
        if elem.tag == Tag.plugin:
            logger.info('Found plugin')
            plug = eclipse.Plugin()
            plugins_list.append(plug)
            #elem_version = elem.find(Tag.version)
            #if not elem_version is None:
            #    plug.version = elem_version.text
            parse_version(elem, plug)

            elem_file = elem.find(Tag.installer_file)
            if not elem_file is None:
                plug.installer_file = elem_file.text
            elem_url = elem.find(Tag.installer_url)
            if not elem_url is None:
                plug.installer_url = elem_url.text
            #Tag.name
            elem_name = elem.find(Tag.name)
            if not elem_name is None:
                plug.name = elem_name.text
            '''
            elem_path = elem.find(Tag.install_path)
            if not elem_path is None:
                plug.install_path = elem_path.text
            '''


def parse_configure(configure: Element, conf_file_list: list):
    logger.info('Has configure')
    for c_elem in configure:
        if c_elem.tag == Tag.file:
            file = {}
            conf_file_list.append(file)
            logger.info('Found file')
            name = c_elem.find(Tag.name)
            file['name'] = name.text
            logger.info('name: ' + str(name.text))
            file_type = c_elem.find(Tag.type)
            file['type'] = file_type.text
            logger.info('type: ' + str(file_type.text))
            key_values = c_elem.find(Tag.key_values)
            key_vals = []
            file['confs'] = key_vals
            for kvs in key_values:
                if kvs.tag == Tag.key_value:
                    key_val = parse_key_value(kvs)
                    key_vals.append(key_val)
        if c_elem.tag == Tag.console:
            temp = {}
            command_list = []
            temp['commands'] = command_list
            conf_file_list.append(temp)
            #command_list.append('spam')
            #command_list.append('eggs')
            for com_elem in c_elem:
                if com_elem.tag == Tag.command:
                    command_list.append(com_elem.text)
        if c_elem.tag == Tag.enviroment:
            temp = {}
            conf_file_list.append(temp)

            key_values = c_elem.find(Tag.key_values)
            key_vals = []
            temp['enviroments'] = key_vals
            for kvs in key_values:
                if kvs.tag == Tag.key_value:
                    key_val = parse_key_value(kvs)
                    key_vals.append(key_val)
            '''
            command_list = []
            temp['enviroments'] = command_list
            for com_elem in c_elem:
                if com_elem.tag == Tag.command:
                    command_list.append(com_elem.text)
            '''


def parse_key_value(kvs: Element):
    key_val = {}
    key = kvs.find(Tag.key)
    key_val['key'] = key.text
    value = kvs.find(Tag.value)
    key_val['value'] = value.text
    logger.info('key: ' + str(key.text) + ' value: ' + str(value.text))
    return key_val


# TODO: should this be a class ?
APPS = {
    'eclipse': [],
    'java': [],
    'npp': [],
    'putty': [],
    'python': [],
    'git': [],
    }

# NOTE: guide for Python hints:
# https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html

# NOTE: docstring hinting works for Eclipse
# https://www.pydev.org/manual_adv_type_hints.html
# https://www.sphinx-doc.org/en/master/

# NOTE: Eclipse's autocomplete does not work with hint object 'List'  :(
#def get_app_objects(app_name: str) -> List[Eclipse]:
def get_app_objects(app_name: str) -> list:
    ':rtype list'
    return list(APPS.get(app_name, []))

def init():
    logger.info('Initialize all applications objects')

    #eclipse_list = list(APPS.get('eclipse', []))
    eclipse_list = get_app_objects('eclipse')

    '''
    if False:  # Definition only for Eclipse auto complete
        ecli = eclipse.Eclipse()
    '''

    for ecli in eclipse_list: #: :type ecli: Eclipse
        source_eclipse = app_source_handler.source.APPS.get('eclipse', {})
        logger.debug('source_eclipse: ' + str(source_eclipse))
        ecli.generate_all(source_eclipse)
        # NOTE: for now just init plugins
        # TODO: move stuff from parse into this?
        ecli.init_plugins(source_eclipse)

    java_list = list(APPS.get('java', []))
    for java_obj in java_list: #: :type java_obj: Java
        source_java = app_source_handler.source.APPS.get('java', {})
        logger.debug('source_java: ' + str(source_java))
        java_obj.generate_all(source_java)

    npp_list = list(APPS.get('npp', []))
    for npp_obj in npp_list: #: :type npp_obj: Npp
        source_npp = app_source_handler.source.APPS.get('npp', {})
        logger.debug('source_npp: ' + str(source_npp))
        npp_obj.generate_all(source_npp)

    putty_list = list(APPS.get('putty', []))
    for putty_obj in putty_list: #: :type putty_obj: Putty
        source_putty = app_source_handler.source.APPS.get('putty', {})
        logger.debug('source_putty: ' + str(source_putty))
        putty_obj.generate_all(source_putty)

    python_list = list(APPS.get('python', []))
    for python_obj in python_list: #: :type python_obj: Python
        source_python = app_source_handler.source.APPS.get('python', {})
        logger.debug('source_python: ' + str(source_python))
        python_obj.generate_all(source_python)

    git_list = list(APPS.get('git', []))
    for git_obj in git_list: #: :type git_obj: Git
        source_git = app_source_handler.source.APPS.get('git', {})
        logger.debug('source_git: ' + str(source_git))
        git_obj.generate_all(source_git)

    winmerge_list = list(APPS.get('winmerge', []))
    for winmerge_obj in winmerge_list: #: :type winmerge_obj: Winmerge
        source_winmerge = app_source_handler.source.APPS.get('winmerge', {})
        logger.debug('source_winmerge: ' + str(source_winmerge))
        winmerge_obj.generate_all(source_winmerge)


def download():
    """ Download all app installers """
    eclipse_list = list(APPS.get('eclipse', []))
    for ecli in eclipse_list: #: :type ecli: Eclipse
        ecli.download()
        ecli.download_plugins()

    java_list = list(APPS.get('java', [])) #: :type java_obj: Java
    for java_obj in java_list:
        java_obj.download()

    npp_list = list(APPS.get('npp', []))
    for npp_obj in npp_list: #: :type npp_obj: Npp
        npp_obj.download()

    putty_list = list(APPS.get('putty', []))
    for putty_obj in putty_list: #: :type putty_obj: Putty
        putty_obj.download()

    python_list = list(APPS.get('python', []))
    for python_obj in python_list: #: :type putty_obj: Python
        python_obj.download()

    git_list = list(APPS.get('git', []))
    for git_obj in git_list: #: :type git_obj: Git
        git_obj.download()

    winmerge_list = list(APPS.get('winmerge', []))
    for winmerge_obj in winmerge_list: #: :type winmerge_obj: Winmerge
        winmerge_obj.download()


def install():
    """ install all app """
    # TODO: Is 'PATH' changed. Is there need to modify it manually?
    logger.debug("os.environ.get('PATH'): " + str(os.environ.get('PATH')))
    util.log_env_var('PATH')

    eclipse_list = list(APPS.get('eclipse', []))
    for ecli in eclipse_list: #: :type ecli: Eclipse
        ecli.install()
        ecli.install_plugins()

    java_list = list(APPS.get('java', []))
    for java_obj in java_list: #: :type java_obj: Java
        java_obj.install()

    npp_list = list(APPS.get('npp', []))
    for npp_obj in npp_list: #: :type npp_obj: Npp
        npp_obj.install()

    putty_list = list(APPS.get('putty', []))
    for putty_obj in putty_list: #: :type putty_obj: Putty
        putty_obj.install()

    python_list = list(APPS.get('python', []))
    for python_obj in python_list: #: :type python_obj: Python
        python_obj.install()

    git_list = list(APPS.get('git', []))
    for git_obj in git_list: #: :type git_obj: Git
        git_obj.install()

    winmerge_list = list(APPS.get('winmerge', []))
    for winmerge_obj in winmerge_list: #: :type winmerge_obj: Winmerge
        winmerge_obj.install()

    # TODO: Is 'PATH' changed. Is there need to modify it manually?
    logger.debug("os.environ.get('PATH'): " + str(os.environ.get('PATH')))
    util.log_env_var('PATH')


def configure():
    """ configure all app """
    eclipse_list = list(APPS.get('eclipse', []))
    for ecli in eclipse_list: #: :type ecli: Eclipse
        ecli.configure()

    git_list = list(APPS.get('git', []))
    for git_obj in git_list: #: :type git_obj: Git
        git_obj.configure()

    putty_list = list(APPS.get('putty', []))
    for putty_obj in putty_list: #: :type putty_obj: Putty
        putty_obj.configure()

    java_list = list(APPS.get('java', []))
    for java_obj in java_list: #: :type java_obj: Java
        java_obj.configure()


def print_sample():
    file = util.fix_path(CONFIG_PATH + '/' + CONFIG_FILE)
    logger.info('print the sample config XML file: ' + str(file))
    tree = ET.parse(file)
    logger.debug(CONFIG_FILE + ' content:\n' + str(ET.tostring(tree.getroot()), 'utf-8'))
    logger.debug('  NOTE: declaration and comments are not printed!')


def create_test_xml():
    # create the file structure
    logger.info('create the XML file structure')
    tree = ET.ElementTree()
    xml_config = ET.Element('test_element')
    tree._setroot(xml_config)
    items = ET.SubElement(xml_config, 'items')
    item1 = ET.SubElement(items, 'item')
    item2 = ET.SubElement(items, 'item')
    item1.set('name','item1')
    item2.set('name','item2')
    item1.text = 'item1abc'
    item2.text = 'item2abc'

    # create a new XML file with the results
    logger.info('create a new XML file with the results')
    LMetree.indent(xml_config)
    tree.write(XML_CONFIG, encoding="UTF-8", xml_declaration=True)
    '''
    mydata = str(ET.tostring(xml_config),'utf-8')
    logger.info('mydata type: ' + str(type(mydata)))
    myfile = open(XML_CONFIG, "w")
    myfile.write(mydata)
    myfile.close()
    '''

def read_write():
    logger.info('read from file: ' + str(XML_TEST))
    tree = ET.parse(XML_TEST)
    root = tree.getroot()
    #root.
    #items = ET.SubElement(root, 'items')
    ET.SubElement(root, 'items')
    #pretty_xml_as_string = root.toprettyxml()
    #pretty_xml_as_string = ET.tostring(root, pretty_print=True)
    #logger.info('pretty_xml_as_string: ' + str(pretty_xml_as_string))
    logger.info('write to file: ' + str(XML_CONFIG))
    LMetree.indent(root)
    #tree.write(XML_CONFIG)
    tree.write(XML_CONFIG, encoding="UTF-8", xml_declaration=True)
    #tree.write(XML_CONFIG, encoding="UTF-8", xml_declaration=True, pretty_print=True)
