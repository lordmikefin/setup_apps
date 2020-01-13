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


def create_sample():
    print('create the sample config XML file')
    file = util.fix_path(CONFIG_PATH + '/' + CONFIG_FILE)
    root = ET.Element('setup')
    tree = ET.ElementTree(root)
    #tree._setroot(root)

    root.append(ET.Comment(' Supported version of "setup_apps" '))

    #root.set('version', __version__)
    version = ET.SubElement(root, 'version')
    version.text = __version__

    apps = ET.SubElement(root, 'apps')

    eclipse = ET.SubElement(apps, 'eclipse')
    version = ET.SubElement(eclipse, 'version')
    version.text = '2019-09'
    eclipse.append(ET.Comment(' {version} is replaced with value from tag "version" '))
    installer_file = ET.SubElement(eclipse, 'installer_file')
    installer_file.text = 'eclipse-javascript-{version}-R-win32-x86_64.zip'
    eclipse.append(ET.Comment(' {installer_file} is replaced with value from tag "installer_file" '))
    installer_url = ET.SubElement(eclipse, 'installer_url')
    installer_url.text = 'https://ftp.acc.umu.se/mirror/eclipse.org/technology/epp/downloads/release/2019-09/R/{installer_file}'

    indent(root)
    util.mkdir(CONFIG_PATH)
    tree.write(file, encoding="UTF-8", xml_declaration=True)


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
