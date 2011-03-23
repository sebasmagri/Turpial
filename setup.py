#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import re

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

from distutils.command.build import build as _build
from babel.messages import frontend as babel
from turpial.config import GLOBAL_CFG

LONG_DESCRIPTION = """
Turpial es un cliente alternativo para microblogging con multiples
interfaces. Esta escrito en Python y tiene como meta ser una aplicacion con
bajo consumo de recursos y que se integre al escritorio del usuario pero sin
renunciar a ninguna funcionalidad
"""

class build(_build):
    sub_commands = [('compile_catalog', None), ] + _build.sub_commands

    def run(self):
        """Run all sub-commands"""
        _build.run(self)

setup_info  = dict(
    name="turpial",
    version=GLOBAL_CFG['App']['version'],
    description="Cliente Twitter escrito en Python",
    long_description=LONG_DESCRIPTION,
    author="Wil Alvarez",
    author_email="wil.alejandro@gmail.com",
    maintainer="Milton Mazzarri",
    maintainer_email="milmazz@gmail.com",
    url="http://turpial.org.ve",
    download_url="http://turpial.org.ve/downloads",
    license="GPLv3",
    keywords='twitter identi.ca microblogging turpial',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: X11 Applications :: GTK",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Topic :: Communications"
    ],
    packages=find_packages(),
    cmdclass={
        'build': build,
        'compile_catalog': babel.compile_catalog,
        'extract_messages': babel.extract_messages,
        'init_catalog': babel.init_catalog,
        'update_catalog': babel.update_catalog,
    },
)

if os.name == 'nt':
    import py2exe

    _data_files = [
        "dlls/Microsoft.VC90.CRT.manifest",
        "dlls/msvcm90.dll",
        "dlls/msvcp90.dll",
        "dlls/msvcr71.dll",
        "dlls/msvcr90.dll"
    ]

    for dirname, dirnames, files in os.walk('data'):
        fpath = []
        for f in files:
            fpath.append(os.path.join(dirname, f))
        _data_files.append((dirname, fpath))

    opts = {
        "py2exe": {
            "packages": ["encodings", "gtk"],
            "includes": ["locale", "gio", "cairo", "pangocairo", "pango",
                         "atk", "gobject", "os", "code", "winsound", "win32api",
                         "win32gui", "optparse"],
            "excludes": ["ltihooks", "pywin", "pywin.debugger",
                         "pywin.debugger.dbgcon", "pywin.dialogs",
                         "pywin.dialogs.list", "Tkconstants", "Tkinter", "tcl",
                         "doctest", "macpath", "pdb", "cookielib", "ftplib",
                         "pickle", "calendar", "win32wnet", "unicodedata",
                         "getopt", "gdk"],
            "dll_excludes": ["libglade-2.0-0.dll", "w9xpopen.exe"],
            "optimize": "2",
            "dist_dir": "dist",
            "skip_archive": 1
        }
    }

    setup(
        requires   = ["gtk"],
        windows    = [{"script": "turpial/main.py", "dest_base": "turpial"}],
        console    = [{"script": "turpial/main.py", "dest_base": "turpial_debug"}],
        options    = opts,
        data_files = _data_files,
        **setup_info
    )

else:
    # TODO: Maybe find some better ways to do this
    # looking distutils's copy_tree method
    data_files=[
        ('share/pixmaps', ['turpial/data/pixmaps/turpial.png']),
        ('share/applications', ['turpial.desktop']),
        ('share/doc/turpial', ['doc/turpial.png',
                               'doc/turpial.dia',
                               'ChangeLog',
                               'README.rst',
                               'COPYING']),
    ]

    pattern = re.compile('turpial/i18n/')
    for root, dirs, files in os.walk(os.path.join('turpial', 'i18n')):
        for filename in files:
            if filename.endswith('.mo'):
                fullpath = os.path.join(root, filename)
                dest = os.path.join('/', 'usr', 'share', 'locale', re.sub(pattern, '', root))
                data_files.append((dest, [fullpath]))

    setup(
        data_files = data_files,
        include_package_data = True,
        package_data={
            'turpial': ['data/pixmaps/*', 'data/sounds/*', 'data/themes/default/*']
        },
        entry_points={
            'console_scripts': [
                'turpial = turpial.main:Turpial',
            ],
        },
    )
