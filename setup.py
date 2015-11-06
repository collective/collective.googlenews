from setuptools import setup, find_packages
import os

version = '2.0a1.dev0'
long_description = open("README.rst").read() + "\n" + \
                   open(os.path.join("docs", "INSTALL.txt")).read() + "\n" + \
                   open(os.path.join("docs", "CREDITS.txt")).read() + "\n" + \
                   open(os.path.join("docs", "HISTORY.txt")).read()

setup(name='collective.googlenews',
      version=version,
      description="Make easy to add your Plone site to Google News.",
      long_description=long_description,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
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
        'plone.app.content',
        'plone.app.registry',
        'plone.registry',
        'Products.Archetypes',
        'Products.ATContentTypes',
        'Products.CMFPlone',
        'Products.GenericSetup',
        'setuptools',
        'zope.component',
        'zope.interface',
        'zope.schema',
      ],
      extras_require={
        'test': [
            'plone.app.testing',
            'plone.browserlayer',
        ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
