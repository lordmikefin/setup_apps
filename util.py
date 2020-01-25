# -*- coding: UTF-8 -*-
"""
    util.py
    ~~~~~~~

    Usefull tools.

    License of this script file:
       MIT License

    License is available online:
      https://github.com/lordmikefin/setup_apps/blob/master/LICENSE

    Latest version of this script file:
      https://github.com/lordmikefin/setup_apps/blob/master/util.py


    :copyright: (c) 2019, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
    :license: MIT License
"""

from distutils.version import StrictVersion
import hashlib
import io
import os
from pathlib import Path
import subprocess
import sys
import traceback
from zipfile import ZipFile

import requests
from tqdm import tqdm

from .namedtuples import CommandRet

# import urllib.request
PWS = 'powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile'


def download(url: str, dst: str, length: int=io.DEFAULT_BUFFER_SIZE, show_progress: bool=False):
    '''
    Download the file from `url` and save it locally under `file_name`

    Python:
    https://docs.python.org/3.4/library/urllib.request.html?highlight=urllib#urllib.request.urlretrieve

    Bash:
    https://sourceforge.net/p/forge/documentation/Downloading%20files%20via%20the%20command%20line/

    TODO: Test more ways.
    https://dzone.com/articles/simple-examples-of-downloading-files-using-python
    '''
    # data = requests.get(url)
    # open(dst, 'wb').write(data.content)

    with open(dst, "wb") as f:
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:
            print('no content length header')
            f.write(response.content)
        else:
            pbar = None
            if show_progress:
                total_length = int(total_length)
                pbar = tqdm(total=total_length)
            for data in response.iter_content(chunk_size=length):
                f.write(data)
                if pbar:
                    pbar.update(len(data))

    # file_name, headers = urllib.request.urlretrieve(url, filename=dst)
    # print('file_name : ' + str(file_name))
    # print('headers   : ' + str(headers))


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
    print('Unzip to  ' + str(dst))
    command = 'PowerShell -Command "Expand-Archive \'' + str(zip_file) + '\' \'' + str(dst) + '\'"'
    res = int(os.system(command))
    # TODO: How to handle possible errors?


def unzip_py(zip_file: str, dst: str, show_progress: bool=False):
    '''
    Unzip pythonic way.

    https://docs.python.org/3.7/library/zipfile.html
    https://stackoverflow.com/questions/3451111/unzipping-files-in-python
    https://thispointer.com/python-how-to-unzip-a-file-extract-single-multiple-or-all-files-from-a-zip-archive/
    https://stackoverflow.com/questions/4341584/extract-zipfile-using-python-display-progress-percentage
    '''
    print('Unzip the file. Pythonic way.')
    print('Unzip to  ' + str(dst))
    # ZipFile
    with ZipFile(zip_file, 'r') as zip_obj:
        if not show_progress:
            # Extract all the contents of zip file in different directory
            zip_obj.extractall(dst)
        else:
            # Show progress during unzip
            for member in tqdm(zip_obj.infolist(), desc='Extracting '):
                zip_obj.extract(member, dst)


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
    # command += '$s.IconLocation = \'' + ico + '\'; '
    # command += '$s.Description = \'' + desc + '\'; '
    # command += '$s.WorkingDirectory = \'' + dir + '\'; '
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
        return -1  # A is older

    if StrictVersion(ver_a) > StrictVersion(ver_b):
        return 1  # A is newer

    return 0


def run_command(command: str) -> CommandRet:
    # TODO: read more about 'subprocess'
    #   https://docs.python.org/3/library/subprocess.html
    #   https://docs.python.org/3/library/subprocess.html#subprocess.check_output
    test = ''
    try:
        # test = subprocess.check_output(command, shell=True)
        test = subprocess.check_output(command, shell=False)
        # print('Stored output: ' + str(test))
        print('Stored output type: ' + str(type(test)))
        print('Stored output: ' + str(test, 'utf-8'))
    except subprocess.CalledProcessError as err:
        print('Command failed')
        print("Error: {0}".format(err))
        # TODO: get error code from 'subprocess'
        # return 1
        return CommandRet(errorlevel=1)
    except FileNotFoundError as err:
        print('Command failed')
        print("Error: {0}".format(err))
        # TODO: get error code from 'subprocess'
        # return 1
        return CommandRet(errorlevel=1)
    except:
        print('Command failed')
        print("Unexpected error:", sys.exc_info()[0])
        print("Unexpected error:", sys.exc_info())
        # exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exc()
        # TODO: get error code from 'subprocess'
        # return 1 # what is default error code ?
        return CommandRet(errorlevel=1)

    # TODO: get error code from 'subprocess'
    # return 0
    return CommandRet(errorlevel=0, stdout=str(test, 'utf-8'))


def home_path() -> str:
    ''' User home path '''
    # https://stackoverflow.com/questions/4028904/how-to-get-the-home-directory-in-python
    # https://docs.python.org/3.7/library/pathlib.html#pathlib.Path.home
    return str(Path.home())


def fix_path(path: str) -> str:
    ''' Fix the path separators '''
    return str(Path(path))


def mkdir(path: str):
    ''' Create the path '''
    Path(path).mkdir(parents=True, exist_ok=True)


def md5sum(src: str, length: int=io.DEFAULT_BUFFER_SIZE, callback=None, show_progress: bool=False) -> str:
    '''
    Calculate md5 checksum.

    https://www.geeksforgeeks.org/md5-hash-python/
    https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
      NOTE: "The underlying MD5 algorithm is no longer deemed secure"
      TODO: Use SHA-2 or SHA-3 instead. For serucity.

    https://stackoverflow.com/questions/1131220/get-md5-hash-of-big-files-in-python/40961519#40961519
    '''
    file_len = Path(src).stat().st_size
    pbar = None
    if show_progress:
        pbar = tqdm(total=file_len)
    calculated = 0
    md5 = hashlib.md5()
    with io.open(src, mode="rb") as fd:
        for chunk in iter(lambda: fd.read(length), b''):
            md5.update(chunk)
            if not callback is None:
                calculated += len(chunk)
                callback(calculated, file_len)
            elif pbar:
                pbar.update(len(chunk))

    if pbar:
        pbar.close()
    # return md5
    return md5.hexdigest()


def print_progress(calculated, file_len):
    # TODO: create console progress bar
    # https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    # https://stackoverflow.com/questions/3160699/python-progress-bar/3162864
    return print('Progress ' + str(calculated) + ' / ' + str(file_len))


def is_md5_in_file(file: str, md5: str) -> bool:
    '''
    Match file md5 sum to the md5sum file.

    TODO: Get md5sum file from the download site.
    TODO: If not available then generate it.
          It should be stored with code base
          or common loacation (separate github project).
    '''
    f = open(file, "r")
    first_line = str(f.readline())
    # print(first_line)
    f.close()
    test = first_line.split(sep=' ', maxsplit=1)
    md5_from_file = test[0]
    # print(md5_from_file)

    if md5 == md5_from_file:
        return True
    return False
