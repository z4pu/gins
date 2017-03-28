# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='gins',
    version='0.1.0',
    description='Goethe Institut Singapore scraper',
    long_description=readme,
    author='szp',
    author_email='luminasce@gmail.com',
    url='https://github.com/z4pu/gins',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
