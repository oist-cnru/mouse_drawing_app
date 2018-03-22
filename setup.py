# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 18:05:25 2018
Last saved on Thu Mar 22 16:55:00 2018

@author: TFBURNS
"""

"""Setup script
For details: https://packaging.python.org/en/latest/distributing.html
"""

import os
import setuptools

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as fd:
    long_description = fd.read()

setuptools.setup(
    name='mouse_drawing_app',
    version='0.2.1',

    description="Tom's Mouse Drawing App",
    long_description='A simple GUI app for the generation of 2d mouse input data',

    url='https://github.com/oist-cnru/mouse_drawing_app',

    author='Thomas F. Burns',
    author_email='tfburns@oist.jp',

    license='GPL-3.0',

    keywords='mouse input, touch input, drawing, touch data, mouse data, data generation',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Science/Research',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # where is our code
    packages=['mouse_drawing_app'],

    # required dependencies
    install_requires=['numpy', 'pandas', 'cython<0.27', 'pygame', 'docutils', 'pygments', 'pypiwin32', 'kivy.deps.sdl2', 'kivy.deps.glew', 'kivy'],
)
