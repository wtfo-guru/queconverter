# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='queconverter',
    version='0.1.0',
    description='Graphic File Converter',
    long_description=readme,
    author='Quien Sabe',
    author_email='qs5779@mail.com',
    url='https://github.com/wtfo-guru/queconverter',
    license='Apache License Version 2.0',
    packages=find_packages(exclude=('tests', 'docs', 'uc2'))
)

