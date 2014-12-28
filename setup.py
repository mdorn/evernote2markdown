#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='evernote2markdown',
    version='0.1.0',
    description='evernote2markdown converts an Evernote export (.enex) file to a set of Markdown files.',
    long_description=readme + '\n\n' + history,
    author='Matt Dorn',
    author_email='matt.dorn@gmail.com',
    url='https://github.com/mdorn/evernote2markdown',
    packages=[
        'evernote2markdown',
    ],
    package_dir={'evernote2markdown':
                 'evernote2markdown'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='evernote2markdown',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points=("""
        [console_scripts]
        evernote2markdown = evernote2markdown.main:main
    """)
)
