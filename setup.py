#!/usr/bin/env python

from setuptools import setup

setup(name='tracestack',
      version='0.1',
      description='Search your last error on Stack Overflow.',
      author='Dan Robinson',
      author_email='danrobinson010@gmail.com',
      url='https://www.github.com/danrobinson/tracestack',
      download_url='https://github.com/danrobinson/tracestack/tarball/0.1',
      packages=['tracestack'],
      entry_points = {'console_scripts': ['tracestack=tracestack.command_line:run'],}
     )
