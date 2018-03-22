# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 16:55:00 2018

@author: TFBURNS
"""

import os
from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as fd:
    long_description = fd.read()

setup(
    name='mouse_drawing_app',
    version='0.2.1',

    description="Tom's Mouse Drawing App",
    long_description='A simple GUI app for the generation of 2d mouse input data',

    url='https://github.com/oist-cnru/mouse_drawing_app',

    author='Thomas F. Burns',
    author_email='tfburns@oist.jp',

    license='GPL-3.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Science/Research',

        'Programming Language :: Python :: 2.7',
    ],

    # where is our code
    packages=['mouse_drawing_app'],

    # required dependencies
    install_requires=['numpy', 'pandas', 'kivy', 'pygame'],
)
