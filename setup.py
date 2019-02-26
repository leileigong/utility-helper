#-*- encoding: UTF-8 -*-
"""
some usefull wrapper class,function etc.
"""
# from distutils.core import setup

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import sys
if sys.version > '3':
    PY3 = True
else:
    PY3 = False

VERSION = '0.1.4'

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
        name='utilityhelper',
        version=VERSION,
        author="Leo Gong",
        author_email="gongleilei@brilliance.com.cn",
        description="some usefull wrapper class,function etc.",
        long_description=long_description,
        classifiers=[  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
            "Environment :: Plugins",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Topic :: Utilities",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
        ],
        keywords='python helper util',
        license="MIT",
        packages=find_packages(exclude=[]),
        install_requires=[
            # 'MySQLdb' if not PY3 else 'pymysql',
        ]
)
