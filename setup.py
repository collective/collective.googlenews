# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '2.0b3.dev0'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(name='collective.googlenews',
      version=version,
      description="Make easy to add your Plone site to Google News.",
      long_description=long_description,
      classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Office/Business :: News/Diary",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone google',
      author='JeanMichel FRANCOIS aka toutpt',
      author_email='toutpt@gmail.com',
      url='https://github.com/collective/collective.googlenews',
      license='GPLv2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'collective.monkeypatcher',
        'plone.api >=1.5',
        'plone.app.dexterity',
        'plone.app.layout',
        'plone.app.registry',
        'plone.behavior',
        'plone.dexterity',
        'plone.directives.form',
        'plone.formwidget.namedfile >=1.0.12',
        'plone.namedfile',
        'plone.supermodel',
        'Products.CMFCore',
        'Products.CMFPlone >=4.3',
        'Products.GenericSetup',
        'setuptools',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
      ],
      extras_require={
        'test': [
            'AccessControl',
            'plone.app.robotframework',
            'plone.app.testing [robot]',
            'plone.browserlayer',
            'plone.registry',
            'zope.component',
        ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
