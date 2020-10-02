#! /usr/bin/env python
"""A template for scikit-learn compatible packages."""

import codecs
import os

from setuptools import find_packages, setup

# Cython compiling
from distutils.core import setup, Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext
import numpy

# get __version__ from _version.py
ver_file = os.path.join('simforest', '_version.py')
with open(ver_file) as f:
    exec(f.read())

DISTNAME = 'simforest'
DESCRIPTION = 'Similarity Forest implementation compatible with Scikit-Learn API.'
with codecs.open('README.rst', encoding='utf-8-sig') as f:
    LONG_DESCRIPTION = f.read()
MAINTAINER = 'Stanisław Czekalski'
MAINTAINER_EMAIL = 'sfczekalski@gmail.com'
URL = 'https://github.com/sfczekalski/similarity_forest'
LICENSE = 'new BSD'
DOWNLOAD_URL = 'https://github.com/sfczekalski/similarity_forest'
VERSION = __version__
INSTALL_REQUIRES = ['numpy', 'scipy', 'scikit-learn']
CLASSIFIERS = ['Intended Audience :: Science/Research',
               'Intended Audience :: Developers',
               'License :: OSI Approved',
               'Programming Language :: Python',
               'Topic :: Software Development',
               'Topic :: Scientific/Engineering',
               'Operating System :: Microsoft :: Windows',
               'Operating System :: POSIX',
               'Operating System :: Unix',
               'Operating System :: MacOS',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3.5',
               'Programming Language :: Python :: 3.6',
               'Programming Language :: Python :: 3.7']
EXTRAS_REQUIRE = {
    'tests': [
        'pytest',
        'pytest-cov'],
    'docs': [
        'sphinx',
        'sphinx-gallery',
        'sphinx_rtd_theme',
        'numpydoc',
        'matplotlib'
    ]
}

setup(name=DISTNAME,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      description=DESCRIPTION,
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      long_description=LONG_DESCRIPTION,
      zip_safe=False,  # the package can run out of an .egg file
      classifiers=CLASSIFIERS,
      packages=find_packages(),
      install_requires=INSTALL_REQUIRES,
      extras_require=EXTRAS_REQUIRE,
      cmdclass={'build_ext': build_ext},  # Cython compiling
      ext_modules=cythonize(["simforest/*.pyx", "simforest/cluster/*.pyx"]),
      include_dirs=[numpy.get_include()]
      )
