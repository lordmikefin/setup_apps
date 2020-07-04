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
import logging
import inspect

# import urllib.request
PWS = 'powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile'

OS_WINDOWS = 'win32'


def create_logger():
    # https://www.toptal.com/python/in-depth-python-logging
    log = logging.getLogger('setup_apps')
    # Do not propagate the log up to parent
    log.propagate = False
    return log

def stop_urllib3_logger():
    # NOTE: stop 'urllib3' logger
    # DEBUG:urllib3.connectionpool:Starting new HTTPS connection ...
    log = logging.getLogger('urllib3')
    log.propagate = False

logger = create_logger()


def logging_test():
    # https://docs.python.org/3/library/logging.html
    # https://docs.python.org/3/howto/logging.html
    # https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
    # https://www.loggly.com/ultimate-guide/python-logging-basics/
    # https://docs.python.org/3/library/logging.handlers.html#logging.StreamHandler
    # https://www.toptal.com/python/in-depth-python-logging
    print('setup_apps.util.logging_test()')
    logging.info('INFO log from "root" logging from setup_apps.util')
    logging.error('ERROR log from "root" logging from setup_apps.util')
    logging.getLogger('setup_apps').info('INFO log from setup_apps.util')
    logging.getLogger('setup_apps').error('ERROR log from setup_apps.util')
    logger.info('INFO log from setup_apps.util')
    logger.error('ERROR log from setup_apps.util')

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

def windows_only():
    """ Raise error if OS is not Windows """
    if not is_os_windows():
        # TODO: create custom exception
        #raise OSError('util.move_win() Works only with Windows')
        #meg = 'util.' + print_this_func_name() + '() Works only with Windows'
        meg = 'util.' + print_caller_func_name() + '() Works only with Windows'
        logger.critical(meg)
        raise OSError(meg)


def print_caller_func_name():
    return print_this_func_name(caller_in_stack=3)

def print_this_func_name(caller_in_stack=1):
    # TODO: Optimize. 'inspect' is processing all kind of info!
    # TODO: 'timeit' before and after optimization :)
    # https://stackoverflow.com/questions/900392/getting-the-caller-function-name-inside-another-function-in-python
    #caller = inspect.stack()[1]
    caller = inspect.stack()[caller_in_stack]
    '''
    logger.debug('caller.frame       : ' + str(caller.frame))
    logger.debug('caller.filename    : ' + str(caller.filename))
    logger.debug('caller.lineno      : ' + str(caller.lineno))
    logger.debug('caller.function    : ' + str(caller.function))
    logger.debug('caller.code_context: ' + str(caller.code_context))
    logger.debug('caller.index       : ' + str(caller.index))
    '''
    return caller.function


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

    logger.info('Downloading from "' + str(url) + '"')
    logger.info('Downloading into "' + str(dst) + '"')
    with open(dst, "wb") as f:
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:
            logger.info('no content length header')
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
    windows_only()
    run_os_command("pause")


def is_file(file: str) -> bool:
    '''
    Is given string pointing to file.
    '''
    return os.path.isfile(file)


def power_shell(command: str) -> int:
    windows_only()
    if command.__contains__('"'):
        # TODO: create custom exception
        msg = 'For now PowerShell command can not contain character "'
        logger.critical(msg)
        raise OSError(msg)

    # TODO: PowerShell will not return the errorlevel !?!?!?
    #   PowerShell -Command "Expand-Archive 'W:\spacesniffer_1_3_0_2.zip' 'C:\temp\spacesniffer_1_3_0_2'"
    # TODO: test PowerShell command with try-catch
    # https://stackoverflow.com/questions/36943318/how-to-get-the-error-code-errorlevel-from-powershell-into-windows-command-prom 

    #command = 'PowerShell -Command "' + command + '"'
    command = 'PowerShell -Command "try { ' + command + ' -ErrorAction stop } catch {$_; exit 123 }"'
    ret = run_os_command(command)
    logger.debug('success: ' + str(ret))
    return ret

def unzip(zip_file: str, dst: str):
    windows_only()
    logger.info('Unzip the file')
    logger.info('Unzip to  ' + str(dst))

    # TODO: PowerShell will not return the errorlevel !?!?!?
    #   PowerShell -Command "Expand-Archive 'W:\spacesniffer_1_3_0_2.zip' 'C:\temp\spacesniffer_1_3_0_2'"
    # TODO: test PowerShell command with try-catch
    # https://stackoverflow.com/questions/36943318/how-to-get-the-error-code-errorlevel-from-powershell-into-windows-command-prom 

    #command = 'PowerShell -Command "Expand-Archive \'' + str(zip_file) + '\' \'' + str(dst) + '\'"'
    #res = run_os_command(command)
    command = 'Expand-Archive \'' + str(zip_file) + '\' \'' + str(dst) + '\''
    res = power_shell(command)
    # TODO: How to handle possible errors?


def unzip_py(zip_file: str, dst: str, show_progress: bool=False):
    '''
    Unzip pythonic way.

    https://docs.python.org/3.7/library/zipfile.html
    https://stackoverflow.com/questions/3451111/unzipping-files-in-python
    https://thispointer.com/python-how-to-unzip-a-file-extract-single-multiple-or-all-files-from-a-zip-archive/
    https://stackoverflow.com/questions/4341584/extract-zipfile-using-python-display-progress-percentage
    '''
    logger.info('Unzip the file. Pythonic way.')
    logger.info('Unzip to  ' + str(dst))
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
    windows_only()
    logger.info('Creating the shortcut file')
    logger.info('Exec file: ' + str(exe_file))
    logger.info('Link file: ' + str(dst_link_file))
    command = '$ws = New-Object -ComObject WScript.Shell; '
    command += '$s = $ws.CreateShortcut(\'' + dst_link_file + '\'); '
    command += '$s.TargetPath = \'' + exe_file + '\'; '
    # command += '$s.IconLocation = \'' + ico + '\'; '
    # command += '$s.Description = \'' + desc + '\'; '
    # command += '$s.WorkingDirectory = \'' + dir + '\'; '
    command += '$s.Save(); '
    command = PWS + ' -Command "' + command + '"'
    logger.info(command)
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

    # TODO: PowerShell will not return the errorlevel !?!?!?
    #   PowerShell -Command "Expand-Archive 'W:\spacesniffer_1_3_0_2.zip' 'C:\temp\spacesniffer_1_3_0_2'"
    # TODO: test PowerShell command with try-catch
    # https://stackoverflow.com/questions/36943318/how-to-get-the-error-code-errorlevel-from-powershell-into-windows-command-prom 

    logger.debug('TODO: use run_command(...) instead of this.')
    logger.debug('print out from the command is not captured and can not be redirected!')
    # TODO: use 'subprocess' module
    # https://docs.python.org/3/library/subprocess.html#module-subprocess
    logger.info('Run command: ' + command)
    res = int(os.system(command))
    logger.debug('Errorlevel: ' + str(res))
    if res != 0:
        logger.error('Command failed. [' + command + ']')
        return False

    return True

def run_command_alt_1(command: Union[str, list], shell=False) -> subprocess.CompletedProcess:
    # https://docs.python.org/3/library/subprocess.html#subprocess.run
    # https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess
    if isinstance(command, str):
        logger.debug('NOTE: It is safer to pass command as list of parameters.')

    if shell:
        # https://docs.python.org/3/library/subprocess.html#security-considerations
        logger.debug('TODO: avoid shell injection vulnerabilities')

    logger.info('Run command: ' + str(command))
    process = None
    try:
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=shell,
            universal_newlines=True)
    except FileNotFoundError as err:
        logger.error('Command failed')
        logger.error("{0}".format(err))
        # https://ss64.com/nt/errorlevel.html
        # https://shapeshed.com/unix-exit-codes/
        # NOTE: error code 1 = "the operation was not successful"
        #return subprocess.CompletedProcess(args=command, returncode=1, stderr=str(err))
        process = subprocess.CompletedProcess(args=command, returncode=1, stderr=str(err))
        logger.error(process)
        #raise err
    except Exception as err:
        logger.error('Command failed')
        logger.error("Unexpected error: " + str(type(err)))
        logger.error("Unexpected error: " + str(err))
        #print("Unexpected error:", sys.exc_info()[0])
        #print("Unexpected error:", sys.exc_info())
        # exc_type, exc_value, exc_traceback = sys.exc_info()
        #traceback.print_exc()
        #process = subprocess.CompletedProcess(args=command, returncode=1, stderr=str(sys.exc_info()[0]))
        #logger.error(process)
        raise err

    logger.debug(str(process))
    return process


def run_command(command: Union[str, list], shell=False) -> CommandRet:
    # TODO: look samples about 'subprocess' from the 'git.py' module
    # TODO: read more about 'subprocess'
    #   https://docs.python.org/3/library/subprocess.html
    #   https://docs.python.org/3/library/subprocess.html#subprocess.check_output
    #   https://janakiev.com/blog/python-shell-commands/
    if isinstance(command, str):
        logger.debug('NOTE: It is safer to pass command as list of parameters.')

    if shell:
        # https://docs.python.org/3/library/subprocess.html#security-considerations
        logger.debug('TODO: avoid shell injection vulnerabilities')

    logger.info('Run command: ' + str(command))
    stderr = ''
    stdout = ''
    errorlevel = 0
    try:
        # test = subprocess.check_output(command, shell=True)
        #test = subprocess.check_output(command, shell=shell)
        #stdout = str(test, 'utf-8')
        # print('Stored output: ' + str(test))
        c_proc = run_command_alt_1(command=command, shell=shell)
        if c_proc.stdout:
            stdout = c_proc.stdout
        if c_proc.returncode:
            errorlevel = c_proc.returncode
        if c_proc.stderr:
            stderr = c_proc.stderr
        #logger.info('Stored output type: ' + str(type(stdout)))
        #logger.info('Stored output: ' + str(stdout))
        '''
    except subprocess.CalledProcessError as err:
        logger.error('Command failed')
        logger.error("{0}".format(err))
        # TODO: get error code from 'subprocess'
        # return 1
        ret = CommandRet(errorlevel=1, stderr=str(err))
        logger.error(ret)
        return ret
        '''
    except FileNotFoundError as err:
        logger.error('Command failed')
        logger.error("{0}".format(err))
        # TODO: get error code from 'subprocess'
        # return 1
        ret = CommandRet(errorlevel=1, stderr=str(err))
        logger.error(ret)
        return ret
    except Exception as err:
        logger.error('Command failed')
        logger.error("Unexpected error: " + str(type(err)))
        logger.error("Unexpected error: " + str(err))
        raise err
        '''
    except:
        logger.error('Command failed')
        logger.error("Unexpected error: " + str(sys.exc_info()[0]))
        logger.error("Unexpected error: " + str(sys.exc_info()))
        #print("Unexpected error:", sys.exc_info()[0])
        #print("Unexpected error:", sys.exc_info())
        # exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exc()
        # TODO: get error code from 'subprocess'
        # return 1 # what is default error code ?
        #return CommandRet(errorlevel=1)
        ret = CommandRet(errorlevel=1, stderr=str(sys.exc_info()[0]))
        logger.error(ret)
        return ret
        '''

    # TODO: get error code from 'subprocess'
    # return 0
    #return CommandRet(errorlevel=0, stdout=str(test, 'utf-8'))
    ret = CommandRet(errorlevel=errorlevel, stdout=str(stdout), stderr=str(stderr))
    logger.debug(str(ret))
    return ret


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


def is_md5_in_file(file: str, md5: str, file_installer: str) -> bool:
    '''
    Match file md5 sum to the md5sum file.
    '''
    file_src = Path(file)
    file_inst = Path(file_installer)
    logger.debug('is_file : ' + str(file_inst.is_file()))
    logger.debug('name    : ' + str(file_inst.name))
    file_name_installer = file_inst.name

    # TODO: can I use  file_inst.read_bytes() ... will it close file with break ?

    md5_from_file = ''
    with open(file_src, 'r') as lines:
        for line in lines:
            #logger.debug('Line :: ' + str(line))
            test = line.split(sep=' ', maxsplit=1)
            if len(test) > 1:
                if str(test[1]).strip() == file_name_installer:
                    md5_from_file = test[0]
                    logger.debug('md5 from file : ' + str(md5_from_file))
                    break

    return is_md5_equal(md5, md5_from_file)


def is_md5_equal(md5_1: str, md5_2: str) -> bool:
    if not md5_1:
        return False
    if not md5_2:
        return False
    if md5_1 == md5_2:
        return True
    return False


def move(src: str, dst: str):
    # https://docs.python.org/3.8/library/shutil.html#shutil.move
    shutil.move(src, dst)


def move_win(src: str, dst: str):
    windows_only()

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
    #print(command)
    res = run_os_command(command)

def startswith_comment(line: str):
    ''' Is line a comment line of INI file. '''
    return line.startswith('#') or line.startswith(';')

def msiexec(name: str, installer: str, properties: dict=None, log_file: str=None,
            show_progress=False) -> bool:
    # https://www.advancedinstaller.com/user-guide/msiexec.html
    # # http://www.silentinstall.org/msiexec
    windows_only()

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
    #print(command)
    test = run_os_command(command)
    #print('')
    if not test:
        # TODO: Installer may not throw error ?
        #print('XXX installation FAILED.')
        return False
    
    #print('XXX installation done.')
    return True


def connect_samba_share(src_samba: str, dst_drive: str) -> bool:
    """ Connect samba share. """
    windows_only()
    logger.debug('TODO: Test if drive exists')
    logger.debug('TODO: Get samba share address from config')
    #command = 'net use W: \\192.168.122.1\sambashare\windows'
    #command = 'net use ' + DRIVE_INSTALLER + ' \\192.168.122.1\sambashare\windows'
    command = 'net use ' + str(dst_drive) + ' ' + str(src_samba)
    #test = run_os_command(command)
    ret = run_command(command)
    test = ret.errorlevel == 0
    if not test:
        logger.info('Samba connection  FAILED.')
        logger.error(ret.stderr)
        #sys.exit(1)
        return False
    else:
        logger.info('Samba share connected.')
        logger.info(ret.stdout)
        return True
