#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup


def long_desc_img_replacer(long_desc):
    replacements = (
        (
            '(docs/overview.svg)',
            '(https://raw.githubusercontent.com/debonzi/gc-event-system/master/docs/overview.svg?sanitize=true)'
        ),
    )
    for f, t in replacements:
        long_desc = long_desc.replace(f, t)
    return long_desc


with open('README.md') as f:
    long_description = long_desc_img_replacer(f.read())

requires = [
    'google-cloud-pubsub',
    'python-dateutil'
]

extras_require = {
    'celery': [
        'celery[redis]>=3.1.20',
    ],
    'test': [
        'coverage==4.5.1',
        'pytest==3.8.1',
        'pytest-cov==2.6.0',
        'mock==2.0.0',
    ],
    'ci': [
        'python-coveralls==2.9.1',
    ]
}


setup(name='gces',
      version='0.0.8-alpha',
      description='Google Cloud Event System.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Daniel Debonzi',
      author_email='debonzi@gmail.com',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6'
      ],
      install_requires=requires,
      extras_require=extras_require,
      url='https://github.com/debonzi/gc-event-system',
      packages=[
          'gces',
          'gces.ext',
          'gces.ext.celery',
          'gces.ext.pyramid'
      ],
      )
