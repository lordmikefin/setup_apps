# -*- coding: UTF-8 -*-
"""
    util.py
    ~~~~~~~

    Usefull tools.

    License of this script file:
       MIT License

    License is available online:
      https://github.com/lordmikefin/LMAutoSetBotWin/blob/master/LICENSE

    Latest version of this script file:
      https://github.com/lordmikefin/LMAutoSetBotWin/blob/master/setup_apps/util.py


    :copyright: (c) 2019, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
    :license: MIT License
"""

import os
import sys
import urllib.request
import requests
import subprocess
import traceback

from distutils.version import StrictVersion
from .namedtuples import CommandRet

PWS='powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile'


def download(url: str, dst: str):
    '''
    Download the file from `url` and save it locally under `file_name`

    Python:
    https://docs.python.org/3.4/library/urllib.request.html?highlight=urllib#urllib.request.urlretrieve

    Bash:
    https://sourceforge.net/p/forge/documentation/Downloading%20files%20via%20the%20command%20line/

    TODO: Test more ways.
    https://dzone.com/articles/simple-examples-of-downloading-files-using-python
    '''
    data = requests.get(url)
    open(dst, 'wb').write(data.content)

    #file_name, headers = urllib.request.urlretrieve(url, filename=dst)
    #print('file_name : ' + str(file_name))
    #print('headers   : ' + str(headers))

    #command = ''
    #res = int(os.system(command))
    # TODO: How to show the progress?


def pause():
    '''
    Pause the console app. Windows only!

    https://stackoverflow.com/questions/11552320/correct-way-to-pause-python-program
    '''
    os.system("pause")


def is_file(file: str) -> bool:
    '''
    Is given string pointing to file.
    '''
    return os.path.isfile(file)


def unzip(zip_file: str, dst: str):
    print('Unzip the file')
    command = 'PowerShell -Command "Expand-Archive \'' + str(zip_file) + '\' \'' + str(dst) + '\'"'
    res = int(os.system(command))
    # TODO: How to handle possible errors?

def shortcut(exe_file: str, dst_link_file: str, ico: str=''):
    '''
    Create shortcut file
    
    https://stackoverflow.com/questions/30028709/how-do-i-create-a-shortcut-via-command-line-in-windows
    https://superuser.com/questions/392061/how-to-make-a-shortcut-from-cmd/392066
    https://stackoverflow.com/questions/346107/creating-a-shortcut-for-a-exe-from-a-batch-file
    '''
    print('Creating the shortcut file')
    command = '$ws = New-Object -ComObject WScript.Shell; '
    command += '$s = $ws.CreateShortcut(\'' + dst_link_file + '\'); '
    command += '$s.TargetPath = \'' + exe_file + '\'; '
    #command += '$s.IconLocation = \'' + ico + '\'; '
    #command += '$s.Description = \'' + desc + '\'; '
    #command += '$s.WorkingDirectory = \'' + dir + '\'; '
    command += '$s.Save(); '
    command = PWS + ' -Command "' + command + '"'
    print(command)
    res = int(os.system(command))
    # TODO: How to handle possible errors?


def compare_version(ver_a: str, ver_b: str) -> int:
    '''
    Compare version numbers


    Return -1 if version A is older than version B
    Return 0 if version A and B are equivalent
    Return 1 if version A is newer than version B

    https://stackoverflow.com/questions/11887762/how-do-i-compare-version-numbers-in-python/21065570
    https://stackoverflow.com/questions/1714027/version-number-comparison-in-python
    '''
    if StrictVersion(ver_a) < StrictVersion(ver_b):
        return -1 # A is older

    if StrictVersion(ver_a) > StrictVersion(ver_b):
        return 1 # A is newer

    return 0


def run_command(command: str) -> CommandRet:
    # TODO: read more about 'subprocess'
    #   https://docs.python.org/3/library/subprocess.html
    #   https://docs.python.org/3/library/subprocess.html#subprocess.check_output
    test = ''
    try:
        #test = subprocess.check_output(command, shell=True)
        test = subprocess.check_output(command, shell=False)
        #print('Stored output: ' + str(test))
        print('Stored output type: ' + str(type(test)))
        print('Stored output: ' + str(test, 'utf-8'))
    except subprocess.CalledProcessError as err:
        print('Command failed')
        print("Error: {0}".format(err))
        # TODO: get error code from 'subprocess'
        #return 1
        return CommandRet(errorlevel=1)
    except FileNotFoundError as err:
        print('Command failed')
        print("Error: {0}".format(err))
        # TODO: get error code from 'subprocess'
        #return 1
        return CommandRet(errorlevel=1)
    except:
        print('Command failed')
        print("Unexpected error:", sys.exc_info()[0])
        print("Unexpected error:", sys.exc_info())
        #exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exc()
        # TODO: get error code from 'subprocess'
        #return 1 # what is default error code ?
        return CommandRet(errorlevel=1)

    # TODO: get error code from 'subprocess'
    #return 0
    return CommandRet(errorlevel=0, stdout=str(test, 'utf-8'))

