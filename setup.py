#!/usr/bin/env python
# coding=utf-8

from setuptools import setup

setup(
    author='František Gažo',
    author_email='frantisek.gazo.313@gmail.com',
    name='invoicer',
    version='0.1.0-beta32',
    description="""
    Invoicer
    """,
    long_description="""
    Invoicer
    """,
    url='',
    platforms=['MacOS'],
    license='MIT License',
    classifiers=[  # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python :: 2.7',
        'Development Status :: 1 - Planning',
        'Operating System :: MacOS',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Utilities'
    ],
    packages=['invoicer'],
    package_dir={
        'invoicer': 'src/invoicer'
    },
    package_data={
        'invoicer': [
            'res/fonts/*.ttf',
            'res/imgs/*.png',
            'res/values/*.yaml'
        ]
    },
    install_requires=[  # list of this package dependencies
        'pyyaml==3.12',
        'reportlab==3.4.0',
    ],
    entry_points='''
        [console_scripts]
        invoicer=invoicer.main:main
    '''
)
