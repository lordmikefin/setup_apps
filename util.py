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
import shutil
from typing import Union

# import urllib.request
PWS = 'powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile'

OS_WINDOWS = 'win32'

def python_version_str() -> str:
    return sys.version

def python_version() -> tuple:
    return sys.version_info

def hint_test(test: str) -> bool:
    return isinstance(test, str)

def hint_test_complex(test: Union[str, int]) -> bool:
    # https://stackoverflow.com/questions/33945261/how-to-specify-multiple-return-types-using-type-hints
    return isinstance(test, str) or isinstance(test, int)

def is_os_windows() -> bool:
    return sys.platform == OS_WINDOWS


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
    if not is_os_windows():
        raise OSError('util.pause() Works only with Windows')
    run_os_command("pause")


def is_file(file: str) -> bool:
    '''
    Is given string pointing to file.
    '''
    return os.path.isfile(file)


def unzip(zip_file: str, dst: str):
    if not is_os_windows():
        raise OSError('util.unzip() Works only with Windows')
    print('Unzip the file')
    print('Unzip to  ' + str(dst))
    command = 'PowerShell -Command "Expand-Archive \'' + str(zip_file) + '\' \'' + str(dst) + '\'"'
    res = run_os_command(command)
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
    if not is_os_windows():
        # TODO: create custom exception
        raise OSError('util.shortcut() Works only with Windows')
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
    test = run_os_command(command)
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


def run_os_command(command: str) -> bool:
    # https://docs.python.org/3/library/os.html#os.system
    # Usage:
    #   from . import util
    #   test = util.run_os_command(command)
    # TODO: use 'run_command' -function instead

    # TODO: use 'subprocess' module
    # https://docs.python.org/3/library/subprocess.html#module-subprocess
    print('Run command: ' + command)
    res = int(os.system(command))
    if res != 0:
        # TODO: log the error
        print('Command failed. [' + command + ']')
        return False

    return True

def run_command_alt_1(command: Union[str, list], shell=False) -> subprocess.CompletedProcess:
    # https://docs.python.org/3/library/subprocess.html#subprocess.run
    # https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess
    if isinstance(command, str):
        print('NOTE: It is safer to pass command as list of parameters.')

    if shell:
        # https://docs.python.org/3/library/subprocess.html#security-considerations
        print('TODO: avoid shell injection vulnerabilities')

    try:
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            shell=shell,
            universal_newlines=True)
    except FileNotFoundError as err:
        print('Command failed')
        print("Error: {0}".format(err))
        # https://ss64.com/nt/errorlevel.html
        # https://shapeshed.com/unix-exit-codes/
        # NOTE: error code 1 = "the operation was not successful"
        return subprocess.CompletedProcess(args=command, returncode=1)

    print('' + str(process))


def run_command(command: Union[str, list], shell=False) -> CommandRet:
    # TODO: look samples about 'subprocess' from the 'git.py' module
    # TODO: read more about 'subprocess'
    #   https://docs.python.org/3/library/subprocess.html
    #   https://docs.python.org/3/library/subprocess.html#subprocess.check_output
    #   https://janakiev.com/blog/python-shell-commands/
    if isinstance(command, str):
        print('NOTE: It is safer to pass command as list of parameters.')

    if shell:
        # https://docs.python.org/3/library/subprocess.html#security-considerations
        print('TODO: avoid shell injection vulnerabilities')

    print('Run command: ' + str(command))
    test = ''
    try:
        # test = subprocess.check_output(command, shell=True)
        test = subprocess.check_output(command, shell=shell)
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


def sha256(src: str, length: int=io.DEFAULT_BUFFER_SIZE, callback=None, show_progress: bool=False) -> str:
    '''
    Calculate sha256

    based on md5sum(...) -function
    https://docs.python.org/2/library/hashlib.html
    '''
    file_len = Path(src).stat().st_size
    pbar = None
    if show_progress:
        pbar = tqdm(total=file_len)
    calculated = 0
    md5 = hashlib.sha256()
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

    return md5.hexdigest()


def is_md5_in_file(file: str, md5: str) -> bool:
    '''
    Match file md5 sum to the md5sum file.
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
    return is_md5_equal(md5, md5_from_file)

def is_md5_equal(md5_1: str, md5_2: str) -> bool:
    if md5_1 == md5_2:
        return True
    return False


def move(src: str, dst: str):
    # https://docs.python.org/3.8/library/shutil.html#shutil.move
    shutil.move(src, dst)


def move_win(src: str, dst: str):
    if not is_os_windows():
        # TODO: create custom exception
        raise OSError('util.move_win() Works only with Windows')

    #command = 'move "' + str(src) + '" "' + str(dst) + '"'
    # NOTE: xcopy does not move !?
    #command = 'xcopy /E /Q /H "' + str(src) + '" "' + str(dst) + '"'
    # /E           Copies directories and subdirectories, including empty ones.
    # /H           Copies hidden and system files also.
    # /Q           Does not display file names while copying.
    # TODO: try 'robocopy'
    command = 'robocopy "' + str(src) + '" "' + str(dst) + '" *.* /MOVE /E /NFL /NDL'
    # /MOVE :: MOVE files AND dirs (delete from source after copying).
    # /E :: copy subdirectories, including Empty ones.
    # /NFL : No File List - don't log file names.
    # /NDL : No Directory List - don't log directory names.
    print(command)
    res = run_os_command(command)

def startswith_comment(line: str):
    ''' Is line a comment line of INI file. '''
    return line.startswith('#') or line.startswith(';')

def msiexec(name: str, installer: str, properties: dict=None, log_file: str=None,
            show_progress=False) -> bool:
    # https://www.advancedinstaller.com/user-guide/msiexec.html
    # # http://www.silentinstall.org/msiexec

    if not is_os_windows():
        # TODO: create custom exception
        raise OSError('util.msiexec() Works only with Windows')

    command = 'START "' + name + '" /WAIT msiexec'
    # Install Options
    #   /i - normal installation
    command = command + ' /i ' + installer
    # Display Options
    #   /passive - unattended mode (the installation shows only a progress bar)
    #   /q - set the UI level:
    #      n - no UI
    if show_progress:
        command = command + ' /passive '
    else:
        command = command + ' /qn '
    # Logging Options
    #   /L - enable logging
    #      v - verbose output
    #      x - include extra debugging information
    #      * - log all information, except for v and x options
    if log_file:
        command = command + ' /L*V ' + log_file
    # Set public properties
    for key, value in properties.items():
        command = command + ' ' + key + '="' + value + '"'
    print(command)
    test = run_os_command(command)
    #print('')
    if not test:
        # TODO: Installer may not throw error ?
        #print('XXX installation FAILED.')
        return False
    
    #print('XXX installation done.')
    return True
