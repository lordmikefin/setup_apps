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
import LMToyBoxPython
import re
import getpass

# import urllib.request
PWS = 'powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile'

OS_WINDOWS = 'win32'
OS_LINUX = 'linux'


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

def is_os_linux() -> bool:
    return sys.platform == OS_LINUX

def linux_only():
    """ Raise error if OS is not Linux """
    if not is_os_linux():
        # TODO: create custom exception
        meg = 'util.' + print_caller_func_name() + '() Works only with Linux'
        logger.critical(meg)
        raise OSError(meg)

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


def not_implemented():
    """ Raise error 'not implemented' """
    # TODO: create custom exception
    meg = 'util.' + print_caller_func_name() + '() Is not implemented for ' + str(sys.platform)
    logger.critical(meg)
    raise OSError(meg)


def pause():
    '''
    Pause the console app.
    '''
    if is_os_windows():
        pause_win()
    elif is_os_linux():
        pause_linux()
    else:
        not_implemented()


def pause_linux():
    '''
    Pause the console app. Linux only!

    https://www.cyberciti.biz/tips/linux-unix-pause-command.html
    '''
    # TODO: Does this work for macOS and/or bsd?
    linux_only()
    # NOTE: sh: 1: read: Illegal option -s  -- Errorlevel: 512  <- sunnign 'sh' not 'bash'
    #run_os_command('read -s -n 1 -p "Press any key to continue . . ."')
    #run_command('read -p "Press any key to continue . . ."', shell=True)
    #run_command('read', shell=True)
    #command = ["read", "-p", "Press any key to continue . . ."]
    command = ["read", "-s", "-n", " 1", "-p", "Press any key to continue . . ."]
    #command = ["read"]
    #command = ['/bin/bash', '-c', command]
    #command = ['/bin/bash', '-c', "read", "-p", "Press any key to continue . . ."]
    # TODO: how to print this from 'read' command
    print("Press any key to continue . . .") # 'read' command will not print into console???
    run_command(command, shell=True)


def pause_win():
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
    if is_os_windows():
        unzip_win(zip_file, dst)
    elif is_os_linux():
        success = unzip_linux(zip_file, dst)
        return success


def unzip_linux(zip_file: str, dst: str):
    # https://linuxize.com/post/how-to-extract-unzip-tar-gz-file/
    linux_only()
    logger.error('No unzip method implemented')
    #tar -xf archive.tar.gz
    #--extract (-x)
    #--directory (-C)
    '''
    command = [
        'tar',
        #'--extract',
        '-x',
        #'--file="'+ zip_file +'"',
        '-f', zip_file,
        #'--directory="'+ dst +'"',
        '-C', dst,
        ]
    '''
    command = 'tar ' + ' -x ' + ' -f ' + zip_file +' -C ' + dst
    '''
    command = [
        'sudo',
        command
        ]
    '''
    #command = 'sudo ' + command
    test = run_command(command, shell=True)
    logger.info('Command result: ' + str(test))
    logger.info('Command succeeded: ' + str(test.errorlevel == 0))
    return test.errorlevel == 0


def unzip_win(zip_file: str, dst: str):
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


def parse_version(git_ver: str) -> str:
    mat = parse_version_alt1(git_ver)
    ret = ''
    if mat.endpos > 0:
        ret = mat[0]
    return ret

def parse_version_alt1(git_ver: str):# -> re.Match:  # TODO: unknown for py3.5
    # https://docs.python.org/3/library/re.html
    res = re.search(r'[0-9]+\.[0-9]+\.[0-9]+', git_ver) #: :type res: re.Match
    return res


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

def run_command_alt_1(command: Union[str, list], shell=False, root_password='') -> subprocess.CompletedProcess:
    # https://docs.python.org/3/library/subprocess.html#subprocess.run
    # https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess
    if isinstance(command, str):
        logger.debug('NOTE: It is safer to pass command as list of parameters.')

    if shell:
        # https://docs.python.org/3/library/subprocess.html#security-considerations
        logger.debug('TODO: avoid shell injection vulnerabilities')

    kwargs = {}
    if is_os_linux():
        # NOTE: It seems that subprocess in using '/bin/sh' not '/bin/bash' as default shell.
        # https://www.saltycrane.com/blog/2011/04/how-use-bash-shell-python-subprocess-instead-binsh/
        #command = ['/bin/bash', '-c', command]
        # Read more:
        # https://stackabuse.com/executing-shell-commands-with-python/
        # https://stackoverflow.com/questions/17435056/read-bash-variables-into-a-python-script
        kwargs['executable'] = '/bin/bash'

    logger.info('Run command: ' + str(command))
    if is_os_linux():
        # NOTE: Run command as root
        if root_password:
            command = 'echo ' + root_password + ' | sudo -S ' + command

    process = None
    try:
        #process = subprocess.Popen(
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=shell,
            #executable='/bin/bash',
            universal_newlines=True,
            **kwargs)
        #return_code = process.wait() # wait for process to finish so we can get the return code ".Popen()"
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

    if root_password:
        pass # NOTE: Do not print 'process' it contains the password!
    else:
        logger.debug(str(process))
    if process.returncode > 0 and process.stderr:
        logger.error(process.stderr)
    elif process.returncode == 0 and process.stderr:
        logger.info(process.stderr)
    return process


def run_command_sudo(command: Union[str, list]) -> CommandRet:
    ''' Run given command as root '''
    logger.info('Run command: ' + str(command))
    stderr = ''
    stdout = ''
    errorlevel = 0

    # NOTE: Windows should already be in elevated mode.
    root_password = ''
    if is_os_linux():
        # NOTE: Eclipse console will echo the password, but bash console does not.
        root_password = getpass.getpass()

    c_proc = run_command_alt_1(command=command, shell=True, root_password=root_password)
    if c_proc.stdout:
        stdout = c_proc.stdout
    if c_proc.returncode:
        errorlevel = c_proc.returncode
    if c_proc.stderr:
        stderr = c_proc.stderr

    ret = CommandRet(errorlevel=errorlevel, stdout=str(stdout), stderr=str(stderr))
    logger.debug(str(ret))
    return ret


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


def create_missing_file(file: str):
    # TODO: Failure will raise an exception. Should this return false?
    logger.info('file missing: ' + str(file))
    path_file = Path(file)
    #parents = path_file.parents
    parent = path_file.parent
    logger.info('Create path:  ' + str(parent))
    mkdir(parent)
    logger.info('Create file')
    with open(file, 'w') as temp:
        pass


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
    logger.debug('command: ' + str(command))
    #res = run_os_command(command)
    res = run_command(command)
    #logger.debug('res: ' + str(res))
    logger.info('robocopy message:\n' + str(res.stdout))
    logger.debug('errorlevel: ' + str(res.errorlevel))
    if res.errorlevel == 1:
        # NOTE: errorlevel 1 is not error
        # https://ss64.com/nt/robocopy-exit.html
        logger.debug('0x01   1       One or more files were copied successfully')
        #res.errorlevel = 0
        res = CommandRet(errorlevel=0, stdout=res.stdout, stderr=res.stderr)

    if res.errorlevel > 0:
        logger.error('robocopy failed:\n' + str(res.stderr))


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
    # TODO: Test if destination drive exists.
    if not dst_drive:
        logger.error('Drive not defined')
        return False
    if not src_samba:
        logger.error('Samba server not defined')
        return False
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


def log_env_var(var_name: str, system_wide: bool=True):
    windows_only()
    if not var_name:
        logger.error('Environment variable name is empty')
        return
    key = 'HKCU\Environment'
    if system_wide:
        key = 'HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
    com = 'reg query "' + key + '" /v ' + var_name
    test = run_command(com)
    logger.debug('test: ' + str(test))
    if test.errorlevel > 0:
        logger.info(test.stderr.replace('\n', '') + ' (' + var_name + ')')
    else:
        #logger.info(test.stdout)
        row_split = test.stdout.split(var_name, maxsplit=1)
        var_row = row_split[1]
        # REG_EXPAND_SZ
        if 'REG_EXPAND_SZ' in var_row:
            cur_val = str(var_row).split('REG_EXPAND_SZ    ', maxsplit=1)
        else:
            cur_val = str(var_row).split('REG_SZ    ', maxsplit=1)
        logger.info('cur_val: ' + str(cur_val[1]).replace('\n', '') + ' (' + var_name + ')')


def set_env_var(var_name: str, var_val: str, system_wide: bool=True):
    windows_only()
    if not var_name:
        logger.error('Environment variable name is empty')
        return
    if not var_name:
        logger.error('Environment variable value is empty')
        return
    '''
     https://superuser.com/questions/1179433/how-to-list-global-environment-variables-separately-from-user-specific-environme
    list all vars:
     > set

    set test val into env vars 
     > setx testvar testval
    print value of var 'testvar'. NOTE: this will not print correct result untill launching new cmd.exe
     > echo %testvar%
    This will print all env var values without relaunching cmd.exe
     > reg query HKCU\Environment

    set test val into system wide env vars 
     > setx /m testvar testval
    list system wide env vars
     > reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
     > reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v testvar
    '''
    params = ''
    if system_wide:
        params = ' /M '
    com = 'SETX ' + params + var_name + ' "' + var_val + '"'
    logger.debug('com: ' + str(com))
    run_command(com)


def convert_multiline_to_singleline(string: str):
    return string.replace('\n', '\t')


def is_root():
    return os.getuid() == 0
