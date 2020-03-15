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
from setup_apps import util, __version__, eclipse, PATH_INSTALLERS
from xml.etree.ElementTree import Element
from setup_apps.tag import Tag
import app_source_handler
import json
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


def indent(elem, level=0):
    ''' Indent the xml tree '''
    # TODO: this should be part of 'xml.etree.ElementTree'
    # TODO: Create common code base! And move this there.

    # NOTE: code copied from stackoverflow
    # https://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def create_sample():
    file = util.fix_path(CONFIG_PATH + '/' + CONFIG_FILE)
    print('create the sample config XML file: ' + str(file))
    root = ET.Element(Tag.setup)
    tree = ET.ElementTree(root)
    #tree._setroot(root)

    root.append(ET.Comment(' Supported version of "setup_apps" '))

    #root.set('version', __version__)
    version = ET.SubElement(root, Tag.version)
    version.text = __version__

    apps = ET.SubElement(root, Tag.apps)
    append_eclipse(apps)

    indent(root)
    util.mkdir(CONFIG_PATH)
    tree.write(file, encoding="UTF-8", xml_declaration=True)


def append_eclipse(apps: Element):
    ecli_elem = ET.SubElement(apps, Tag.eclipse)
    version = ET.SubElement(ecli_elem, Tag.version)
    version.text = '2019-09'
    ecli_elem.append(ET.Comment(' {version} is replaced with value from tag "version" '))
    installer_file = ET.SubElement(ecli_elem, Tag.installer_file)
    installer_file.text = 'eclipse-javascript-{version}-R-win32-x86_64.zip'
    ecli_elem.append(ET.Comment(' {installer_file} is replaced with value from tag "installer_file" '))
    installer_url = ET.SubElement(ecli_elem, Tag.installer_url)
    installer_url.text = 'https://ftp.acc.umu.se/mirror/eclipse.org/technology/epp/downloads/release/2019-09/R/{installer_file}'
    ecli_elem.append(ET.Comment(' {version} is replaced with value from tag "version" '))
    install_path = ET.SubElement(ecli_elem, Tag.install_path)
    install_path.text = 'C:\\Program Files\\eclipse-{version}'
    append_configure(ecli_elem)
    append_plugins(ecli_elem)


def append_configure(ecli_elem: Element):
    configure = ET.SubElement(ecli_elem, Tag.configure)
    configure.append(ET.Comment(' "file" is realative path of "install_path" '))
    configure_file = ET.SubElement(configure, Tag.file)
    name = ET.SubElement(configure_file, Tag.name)
    name.text = '\eclipse.ini'
    file_type = ET.SubElement(configure_file, Tag.type)
    file_type.text = 'ini'
    key_values = ET.SubElement(configure_file, Tag.key_values)
    key_value = ET.SubElement(key_values, Tag.key_value)
    key = ET.SubElement(key_value, Tag.key)
    key.text = '-Dosgi.instance.area.default'
    value = ET.SubElement(key_value, Tag.value)
    value.text = '@user.home/eclipse-workspace-2019-09'


def append_plugins(ecli_elem: Element):
    plugins = ET.SubElement(ecli_elem, Tag.plugins)
    plugin = ET.SubElement(plugins, Tag.plugin)
    #plugin_pydev = ET.SubElement(plugin, Tag.plugin_pydev)
    plugin_pydev = plugin  # TODO: is there realy need for separate tag for each plugin?
    name = ET.SubElement(plugin_pydev, Tag.name)
    name.text = 'pydev'
    version = ET.SubElement(plugin_pydev, Tag.version)
    version.text = '7.4.0'
    plugin_pydev.append(ET.Comment(' {version} is replaced with value from tag "version" '))
    installer_file = ET.SubElement(plugin_pydev, Tag.installer_file)
    #installer_file.text = 'PyDev%20{version}.zip'
    installer_file.text = 'PyDev {version}.zip'
    plugin_pydev.append(ET.Comment(' {installer_file} is replaced with value from tag "installer_file" '))
    installer_url = ET.SubElement(plugin_pydev, Tag.installer_url)
    installer_url.text = 'https://sourceforge.net/projects/pydev/files/pydev/PyDev%20{version}/{installer_file}/download'
    plugin_pydev.append(ET.Comment(' {version} is replaced with value from tag "version" '))
    #install_path = ET.SubElement(plugin_pydev, Tag.install_path)
    # TODO: get this path from eclipse
    #install_path.text = 'C:\\Program Files\\eclipse-{version}'
    #install_path.text = '\\eclipse-{version}'
    # TODO: Jar file location is needed for "is_instelled" check
    #_jar_file = _eclipse_path + '\\plugins\\org.python.pydev_7.4.0.201910251334\\pydev.jar'


def parse(source_file: str=''):
    download_source_xml()
    parse_source_xml(source_file)
    print('parse the config XML file')
    file = util.fix_path(CONFIG_PATH + '/' + CONFIG_FILE)
    tree = ET.parse(file)
    root = tree.getroot()
    for elem in root:
        # TODO: check version
        if elem.tag == Tag.apps:
            parse_apps(elem)


SOURCE_FILE = util.fix_path(PATH_INSTALLERS + '/' + 'app_source.xml')
SOURCE_FILE_OK = False
def download_source_xml():
    global SOURCE_FILE_OK
    print('download the source XML file')
    file = SOURCE_FILE
    url = 'https://raw.githubusercontent.com/lordmikefin/app_source/master/app_source.xml'
    util.download(url, file, show_progress=True)
    # TODO: create real verification with md5sum
    if util.is_file(file):
        SOURCE_FILE_OK = True


def parse_source_xml(source_file: str=''):
    print('parse the source XML file')
    # app_source_handler.source.parse(source_file)
    if SOURCE_FILE_OK:
        app_source_handler.source.parse(SOURCE_FILE)
        print('APPS: ' + json.dumps(app_source_handler.source.APPS,
                                     sort_keys=True, indent=2))
    else:
        print('parsing failed')


def parse_apps(elem_apps: Element):
    # TODO: is there better way to fix auto complete within the for loop ?
    if False:  # for Eclipse auto complete only :)
        elem = Element()
    for elem in elem_apps:
        if elem.tag == Tag.eclipse:
            parse_eclipse(elem)


def parse_eclipse(elem: Element):
    global APPS

    ecli = eclipse.Eclipse()
    elem_version = elem.find(Tag.version)
    if not elem_version is None:
        ecli.version = elem_version.text
    elem_file = elem.find(Tag.installer_file)
    if not elem_file is None:
        ecli.installer_file = elem_file.text
    elem_url = elem.find(Tag.installer_url)
    if not elem_url is None:
        ecli.installer_url = elem_url.text
    elem_path = elem.find(Tag.install_path)
    if not elem_path is None:
        ecli.install_path = elem_path.text

    print('version                  : ' + str(ecli.version))
    print('installer_file           : ' + str(ecli.installer_file))
    print('installer_url            : ' + str(ecli.installer_url))
    print('installer_full_url       : ' + str(ecli.installer_full_url))

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

    eclipse_list = list(APPS.get('eclipse', []))
    eclipse_list.append(ecli)
    APPS['eclipse'] = eclipse_list


def parse_plugins(plugins: Element, plugins_list: list):
    print('Has plugins')
    for elem in plugins:
        if elem.tag == Tag.plugin:
            print('Found plugin')
            plug = eclipse.Plugin()
            plugins_list.append(plug)
            elem_version = elem.find(Tag.version)
            if not elem_version is None:
                plug.version = elem_version.text
            elem_file = elem.find(Tag.installer_file)
            if not elem_file is None:
                plug.installer_file = elem_file.text
            elem_url = elem.find(Tag.installer_url)
            if not elem_url is None:
                plug.installer_url = elem_url.text
            '''
            elem_path = elem.find(Tag.install_path)
            if not elem_path is None:
                plug.install_path = elem_path.text
            '''


def parse_configure(configure: Element, conf_file_list: list):
    print('Has configure')
    for c_elem in configure:
        if c_elem.tag == Tag.file:
            file = {}
            conf_file_list.append(file)
            print('Found file')
            name = c_elem.find(Tag.name)
            file['name'] = name.text
            print('name: ' + str(name.text))
            file_type = c_elem.find(Tag.type)
            file['type'] = file_type.text
            print('type: ' + str(file_type.text))
            key_values = c_elem.find(Tag.key_values)
            key_vals = []
            file['confs'] = key_vals
            for kvs in key_values:
                if kvs.tag == Tag.key_value:
                    key_val = parse_key_value(kvs)
                    key_vals.append(key_val)


def parse_key_value(kvs: Element):
    key_val = {}
    key = kvs.find(Tag.key)
    key_val['key'] = key.text
    value = kvs.find(Tag.value)
    key_val['value'] = value.text
    print('key: ' + str(key.text) + ' value: ' + str(value.text))
    return key_val


# TODO: should this be a class ?
APPS = {
    'eclipse': []
    }

def init():
    """ Initialize all app objects """
    eclipse_list = list(APPS.get('eclipse', []))
    if False:  # Definition only for Eclipse auto complete
        ecli = eclipse.Eclipse()

    for ecli in eclipse_list:
        ecli.generate_all()
        # NOTE: for now just init plugins
        # TODO: move stuff from parse into this?
        ecli.init_plugins()


def download():
    """ Download all app installers """
    eclipse_list = list(APPS.get('eclipse', []))
    if False:  # Definition only for Eclipse auto complete
        ecli = eclipse.Eclipse()

    for ecli in eclipse_list:
        ecli.download()
        ecli.download_plugins()


def install():
    """ install all app """
    if False:  # Definition only for Eclipse auto complete
        ecli = eclipse.Eclipse()

    eclipse_list = list(APPS.get('eclipse', []))
    for ecli in eclipse_list:
        ecli.install()


def configure():
    """ configure all app """
    if False:  # Definition only for Eclipse auto complete
        ecli = eclipse.Eclipse()

    eclipse_list = list(APPS.get('eclipse', []))
    for ecli in eclipse_list:
        ecli.configure()
        #ecli.configure_hc()


def print_sample():
    file = util.fix_path(CONFIG_PATH + '/' + CONFIG_FILE)
    print('print the sample config XML file: ' + str(file))
    print()
    tree = ET.parse(file)
    #print(tree)
    print(str(ET.tostring(tree.getroot()), 'utf-8'))
    print()
    print('  NOTE: declaration and comments are not printed!')
    print()


def create_test_xml():
    # create the file structure
    print('create the XML file structure')
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
    print('create a new XML file with the results')
    indent(xml_config)
    tree.write(XML_CONFIG, encoding="UTF-8", xml_declaration=True)
    '''
    mydata = str(ET.tostring(xml_config),'utf-8')
    print('mydata type: ' + str(type(mydata)))
    myfile = open(XML_CONFIG, "w")
    myfile.write(mydata)
    myfile.close()
    '''

def read_write():
    print('read from file: ' + str(XML_TEST))
    tree = ET.parse(XML_TEST)
    root = tree.getroot()
    #root.
    #items = ET.SubElement(root, 'items')
    ET.SubElement(root, 'items')
    #pretty_xml_as_string = root.toprettyxml()
    #pretty_xml_as_string = ET.tostring(root, pretty_print=True)
    #print('pretty_xml_as_string: ' + str(pretty_xml_as_string))
    print('write to file: ' + str(XML_CONFIG))
    indent(root)
    #tree.write(XML_CONFIG)
    tree.write(XML_CONFIG, encoding="UTF-8", xml_declaration=True)
    #tree.write(XML_CONFIG, encoding="UTF-8", xml_declaration=True, pretty_print=True)
