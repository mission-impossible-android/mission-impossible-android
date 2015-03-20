#!/usr/bin/env python3

from setuptools import setup

setup(
    name='mia',
    version='0.0.1',
    description='MIA - Mission Impossible: Hardening Android for Security and Privacy',
    author='The MIA team',
    url='https://github.com/SchnWalter/mission-impossible-android',
    scripts=['tools/mia'],
    install_requires=[
        'docopt',
        'PyYAML',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Topic :: Utilities',
    ]
)
