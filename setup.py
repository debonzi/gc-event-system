#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

requires = [
    'google-cloud-pubsub',
]

extras_require = {
    'celery': [
        'celery[redis]>=3.1.20',
    ],
    'test': [
        'pytest',
        'pytest-cov',
        'mock',
    ],
    'ci': [
        'python-coveralls',
    ]
}


setup(name='gces',
      version='0.0.1-alpha',
      description='Google Cloud Event System.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Daniel Debonzi',
      author_email='debonzi@gmail.com',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6'
      ],
      install_requires=requires,
      extras_require=extras_require,
      url='',
      packages=['gces'],
      )
