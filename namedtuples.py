# -*- coding: UTF-8 -*-
"""
    namedtuples.py
    ~~~~~~~~~~~~~~

    Collection of named tuples.

    License of this script file:
       MIT License

    License is available online:
      /LICENSE

    Latest version of this script file:
      https://github.com/lordmikefin/setup_apps/blob/master/namedtuples.py

    Read more:
      https://docs.python.org/3/library/collections.html#collections.namedtuple
      https://docs.python.org/3/library/typing.html#typing.NamedTuple

    :copyright: (c) 2020, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
    :license: MIT License
"""

from typing import NamedTuple

# TODO: modernize?

#Point = namedtuple('Point', ['x', 'y'])
#Employee = NamedTuple('Employee', [('name', str), ('id', int)])

#CommandRet = namedtuple('CommandRet', ['errorlevel', 'stdout'])

#Backward-compatible usage:
#CommandRet = NamedTuple('CommandRet', [('errorlevel', int), ('stdout', str)])

CommandRet = NamedTuple('CommandRet', [('errorlevel', int), ('stdout', str), ('stderr', str)])
'''
class CommandRet(NamedTuple):
    # TODO: type hint is not supported by py3.5 ???
    #stdout: str = ''
    stdout = ''
    #errorlevel: int = 0  # 0, no error
    errorlevel = 0  # 0, no error
    #stderr: str = ''
    stderr = ''
'''
