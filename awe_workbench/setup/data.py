#!/usr/bin/env python3.10
# Copyright 2022, Educational Testing Service

import argparse
import os

from distutils.command.build import build
from distutils.command.build import build as _build
from distutils.command.install import install
from distutils.command.install import install as _install

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.develop import develop as _develop


class data:

    def extra_install_commands(self):

        # We need to make sure that the parser has all its datafiles set up.
        # Location is different depending on whether we're in install or
        # develop mode.
        if install:
            os.system('python -m nltk.downloader all')
            os.system('python -m awe_languagetool.setup.data --install')
            os.system('python -m awe_spellcorrect.setup.data --install')
            os.system('python -m awe_components.setup.data')
        elif develop:
            os.system('python -m awe_languagetool.setup.data --develop')
            os.system('python -m awe_spellcorrect.setup.data --develop')
            os.system('python -m awe_components.setup.data')

    def __init__(self, args):
        if args.install or args.develop:
            self.extra_install_commands()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run AWE \
                                     Workbench data download')
    parser.add_argument("-d",
                        "--develop",
                        help="Runs the data downloads to the development \
                              rather than the build location.",
                        action="store_true")
    parser.add_argument("-i",
                        "--install",
                        help="Runs the data downloads to the development \
                              rather than the build location.",
                        action="store_true")

    args = parser.parse_args()

    data(args)
