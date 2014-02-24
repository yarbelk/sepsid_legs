#!/usr/bin/env python
#encoding: utf-8

from setuptools import setup

setup(name="sepsid_legs",
        version='0.1.1',
        description="A series of tools for the ananlysis of complexity of sepsid legs",
        author='James Rivett-Carnac',
        author_email='james.rivettcarnac@gmail.com',
        packages=['morpho_complexity',],
        install_requires=['path.py', 'pillow'],
        scripts=['scripts/sl_resize.py',],
        test_suite= 'nose.collector',
        test_requires = ['nose',]
        )
