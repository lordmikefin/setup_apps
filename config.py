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
from setup_apps import util, __version__
from xml.etree.ElementTree import Element
from setup_apps.eclipse import Eclipse
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


class Tag():
    setup = 'setup'
    version = 'version'
    apps = 'apps'
    installer_file = 'installer_file'
    installer_url = 'installer_url'
    install_path = 'install_path'

    configure = 'configure'
    file = 'file'
    name = 'name'
    type = 'type'
    key = 'key'
    value = 'value'

    eclipse = 'eclipse'


def create_sample():
    print('create the sample config XML file')
    file = util.fix_path(CONFIG_PATH + '/' + CONFIG_FILE)
    root = ET.Element(Tag.setup)
    tree = ET.ElementTree(root)
    #tree._setroot(root)

    root.append(ET.Comment(' Supported version of "setup_apps" '))

    #root.set('version', __version__)
    version = ET.SubElement(root, Tag.version)
    version.text = __version__

    apps = ET.SubElement(root, Tag.apps)

    eclipse = ET.SubElement(apps, Tag.eclipse)
    version = ET.SubElement(eclipse, Tag.version)
    version.text = '2019-09'
    eclipse.append(ET.Comment(' {version} is replaced with value from tag "version" '))
    installer_file = ET.SubElement(eclipse, Tag.installer_file)
    installer_file.text = 'eclipse-javascript-{version}-R-win32-x86_64.zip'
    eclipse.append(ET.Comment(' {installer_file} is replaced with value from tag "installer_file" '))
    installer_url = ET.SubElement(eclipse, Tag.installer_url)
    installer_url.text = 'https://ftp.acc.umu.se/mirror/eclipse.org/technology/epp/downloads/release/2019-09/R/{installer_file}'
    eclipse.append(ET.Comment(' {version} is replaced with value from tag "version" '))
    install_path = ET.SubElement(eclipse, Tag.install_path)
    install_path.text = 'C:\\Program Files\\eclipse-{version}'

    configure = ET.SubElement(eclipse, Tag.configure)
    configure.append(ET.Comment(' "file" is realative path of "install_path" '))
    configure_file = ET.SubElement(configure, Tag.file)
    name = ET.SubElement(configure_file, Tag.name)
    name.text = '\eclipse.ini'
    file_type = ET.SubElement(configure_file, Tag.type)
    file_type.text = 'ini'
    key = ET.SubElement(configure_file, Tag.key)
    key.text = '-Dosgi.instance.area.default'
    value = ET.SubElement(configure_file, Tag.value)
    value.text = '@user.home/eclipse-workspace-2019-09'

    indent(root)
    util.mkdir(CONFIG_PATH)
    tree.write(file, encoding="UTF-8", xml_declaration=True)


def parse():
    print('parse the config XML file')
    file = util.fix_path(CONFIG_PATH + '/' + CONFIG_FILE)
    tree = ET.parse(file)
    root = tree.getroot()
    for elem in root:
        # TODO: check version
        if elem.tag == Tag.apps:
            parse_apps(elem)


def parse_apps(elem_apps: Element):
    global APPS

    # TODO: is there better way to fix auto complete within the for loop ?
    if False:  # for Eclipse auto complete only :)
        elem = Element()
    for elem in elem_apps:
        if elem.tag == Tag.eclipse:
            eclipse = Eclipse()
            elem_version = elem.find(Tag.version)
            if not elem_version is None:
                eclipse.version = elem_version.text
            elem_file = elem.find(Tag.installer_file)
            if not elem_file is None:
                eclipse.installer_file = elem_file.text
            elem_url = elem.find(Tag.installer_url)
            if not elem_url is None:
                eclipse.installer_url = elem_url.text
            elem_path = elem.find(Tag.install_path)
            if not elem_path is None:
                eclipse.install_path = elem_path.text

            print('version                  : ' + str(eclipse.version))
            print('installer_file           : ' + str(eclipse.installer_file))
            print('installer_url            : ' + str(eclipse.installer_url))
            print('installer_full_url       : ' + str(eclipse.installer_full_url))

            eclipse.generate_full_url()
            print('installer_full_url       : ' + str(eclipse.installer_full_url))

            eclipse.generate_installer_path()
            print('installer_path           : ' + str(eclipse.installer_path))

            eclipse.generate_install_path()
            print('install_path_full        : ' + str(eclipse.install_path_full))

            eclipse_list = list(APPS.get('eclipse', []))
            eclipse_list.append(eclipse)
            APPS['eclipse'] = eclipse_list

# TODO: should this be a class ?
APPS = {
    'eclipse': []
    }

def download():
    """ Download all app installers """
    eclipse_list = list(APPS.get('eclipse', []))
    for eclipse in eclipse_list:
        eclipse.download()


def install():
    """ install all app """
    eclipse_list = list(APPS.get('eclipse', []))
    for eclipse in eclipse_list:
        eclipse.install()


def configure():
    """ configure all app """
    eclipse_list = list(APPS.get('eclipse', []))
    for eclipse in eclipse_list:
        eclipse.configure()


def print_sample():
    print('print the sample config XML file')
    print()
    file = util.fix_path(CONFIG_PATH + '/' + CONFIG_FILE)
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
    items = ET.SubElement(root, 'items')
    #pretty_xml_as_string = root.toprettyxml()
    #pretty_xml_as_string = ET.tostring(root, pretty_print=True)
    #print('pretty_xml_as_string: ' + str(pretty_xml_as_string))
    print('write to file: ' + str(XML_CONFIG))
    indent(root)
    #tree.write(XML_CONFIG)
    tree.write(XML_CONFIG, encoding="UTF-8", xml_declaration=True)
    #tree.write(XML_CONFIG, encoding="UTF-8", xml_declaration=True, pretty_print=True)
