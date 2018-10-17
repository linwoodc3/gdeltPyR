#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import codecs
import os
import re

from setuptools import setup

cwd = os.path.abspath(os.path.dirname(__file__))


def read(filename):
    with codecs.open(os.path.join(cwd, filename), 'rb', 'utf-8') as h:
        return h.read()


metadata = read(os.path.join(cwd, 'gdelt', '__init__.py'))


def extract_metaitem(meta):
    # swiped from https://hynek.me 's attr package
    meta_match = re.search(
        r"""^__{meta}__\s+=\s+['\"]([^'\"]*)['\"]""".format(meta=meta),
        metadata, re.MULTILINE)
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError('Unable to find __{meta}__ string.'.format(meta=meta))


setup(
    name='gdelt',
    version=extract_metaitem('version'),
    license=extract_metaitem('license'),
    description=extract_metaitem('description'),
    long_description=(read('README.rst') + '\n\n' +
                      read('AUTHORS.rst') + '\n\n' +
                      read('CHANGES')),
    author=extract_metaitem('author'),
    author_email=extract_metaitem('email'),
    maintainer=extract_metaitem('author'),
    maintainer_email=extract_metaitem('email'),
    url=extract_metaitem('url'),
    # download_url=extract_metaitem('download_url'),
    platforms=['Any'],
    packages=['gdelt'],
    install_requires=['numpy', 'pandas>=0.20.3', 'requests',
                      'python-dateutil',
                      'mock;python_version<"3.3"',
                      "futures; python_version < '3.0'",
                      "futures>=3.0.5; python_version == '2.6'"
                      " or python_version=='2.7'"
                      ],
    extras_require={
        'geoSpatial': ["fiona>=1.6", "shapely>=1.5", "geopandas>-1.7"],
        ":python_version<'3.3'": ["mock", "futures"],
        'r': ['pyarrow']
    },
    include_package_data=True,
    package_data={'utils': ['schema_csvs/*']},
    data_files=[('data', ['data/cameoCodes.json', 'data/events1.csv',
                          'data/events2.csv', 'data/gkg2.csv',
                          'data/iatv.csv', 'data/mentions.csv',
                          'data/visualgkg.csv', 'data/gkg2listsamp.gz',
                          'data/events2listsamp.gz', 'data/events1.csv',
                          'data/events1samp.gz',
                          'data/events2.csv',
                          'data/events2listsamp.gz',
                          'data/events2samp.gz',
                          'data/events2samps.csv.zip',
                          'data/events2Transsamp.gz',
                          'data/gkg1.csv',
                          'data/gkg1samp.gz',
                          'data/gkg2.csv',
                          'data/gkg2listsamp.gz',
                          'data/gkg2samp.gz',
                          'data/gkg2Transsamp.gz',
                          'data/iatv.csv',
                          'data/mentions.csv',
                          'data/mentionslistsamp.gz',
                          'data/mentionssamp.csv',
                          'data/mentionssamp.gz',
                          'data/mentionsTranssamp.gz',
                          'data/visualgkg.csv'
                          ])],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
keywords='gdelt pandas tidy data api',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Chat',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
)
