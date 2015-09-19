#!/usr/bin/env python
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

from setuptools import setup

setup(name='tracestack',
      version='0.1.6',
      description='Instantly search your Python error messages on the web.',
      author='Dan Robinson',
      author_email='danrobinson010@gmail.com',
      url='https://www.github.com/danrobinson/tracestack',
      download_url='https://github.com/danrobinson/tracestack/tarball/0.1.6',
      long_description=long_description,
      packages=['tracestack'],
      test_suite="tests",
      entry_points = {'console_scripts': ['tracestack=tracestack.command_line:run'],}
     )
