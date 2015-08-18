# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='floodio-python',
    author='Devon Meunier',
    author_email='devon@eventmobi.com',
    version='0.1',
    license='MIT',
    description='Flood.io client for Python 2 and 3',
    packages=['floodio'],
    install_requires=['requests', 'python-dateutil'],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
