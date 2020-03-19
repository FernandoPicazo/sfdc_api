# from distutils.core import setup
from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='sfdc_api',
      version='0.1.5',
      packages=find_packages(),
      license='MIT',
      download_url='https://github.com/FernandoPicazo/sfdc_api.git',
      long_description=long_description,
      long_description_content_type='text/markdown',
      description='A Salesforce API wrapper focused on a zero dependency development workflow')
