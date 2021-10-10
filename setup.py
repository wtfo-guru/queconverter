# -*- coding: utf-8 -*-

from qc3 import qc3const
from setuptools import find_packages
from distutils.core import setup, Extension

module1 = Extension('qc3.cms._lcms2',
                    # define_macros = [('MAJOR_VERSION', '1'),
                    #                  ('MINOR_VERSION', '0')],
                    libraries = ['lcms2'],
                    library_dirs = ['/usr/lib'],
                    include_dirs = ['/usr/include'],
                    sources = ['qc3/cms/lcms2/_lcms2.c'])

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='queconverter',
    version=qc3const.VERSION + qc3const.REVISION,
    description='Graphic File Converter',
    long_description=readme,
    author='Quien Sabe',
    author_email='qs5779@mail.com',
    url='https://github.com/wtfo-guru/queconverter',
    license='Apache License Version 2.0',
    packages=find_packages(exclude=('tests', 'docs', 'subproj')),
    ext_modules = [module1]
)

