# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '2.0a1.dev0'
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
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
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
        'plone.api',
        'plone.app.dexterity',
        'plone.app.registry',
        'plone.behavior',
        'plone.dexterity',
        'plone.directives.form',
        'plone.formwidget.namedfile >=1.0.12',
        'plone.namedfile',
        'plone.registry',
        'plone.supermodel',
        'Products.ATContentTypes',
        'Products.CMFCore',
        'Products.CMFPlone >=4.3',
        'Products.GenericSetup',
        'setuptools',
        'zope.component',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
      ],
      extras_require={
        'test': [
            'AccessControl',
            'plone.app.testing',
            'plone.browserlayer',
        ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
