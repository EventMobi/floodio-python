# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='floodio-python',
    author='Devon Meunier',
    author_email='devon@eventmobi.com',
    version='0.3',
    license='MIT',
    description='Flood.io client for Python 2 and 3',
    packages=['floodio'],
    install_requires=['requests', 'python-dateutil'],
)
