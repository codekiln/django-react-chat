#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup, find_packages


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    with open(os.path.join(package, '__init__.py'), 'rb') as init_py:
        src = init_py.read().decode('utf-8')
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", src).group(1)


setup(
    name='django-react-chat',
    version=get_version('django_react_chat'),
    url='https://github.com/codekiln/django-react-chat',
    license='MIT',
    description='React-Based Chat App for Django',
    author='Myer Nore',
    author_email='ptr.nore@gmail.com',

    packages=find_packages(
        where='.',
        exclude=('django_react_chat_example_project*', )
    ),
    include_package_data=True,
    install_requires=[
        "Django>=1.9",
        "djangorestframework>=3.2.0",
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
    ]
)