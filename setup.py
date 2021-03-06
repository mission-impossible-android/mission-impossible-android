#!/usr/bin/env python

import io
import os
import re
from setuptools import find_packages, setup


def read_file_contents(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fp:
        return fp.read()


def get_package_info(name):
    file_contents = read_file_contents(os.path.join('mia', '__init__.py'))
    version_match = re.search(r'^%s\s*=\s*[\'"](.*?)[\'"]' % name, file_contents, re.M)

    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find %s string.' % name)


setup(
    name='mia',
    version=get_package_info('__version__'),
    description=get_package_info('__description__'),
    author=get_package_info('__author__'),
    author_email=get_package_info('__author_email__'),
    license=get_package_info('__license__'),
    url=get_package_info('__url__'),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'mia = mia.__main__:main'
        ],
    },
    install_requires=[
        'docopt',
        'PyYAML',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ]
)
