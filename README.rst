*********************
collective.googlenews
*********************

.. contents:: Table of Contents


.. image:: http://img.shields.io/pypi/v/collective.googlenews.svg
    :target: https://pypi.python.org/pypi/collective.googlenews

.. image:: https://img.shields.io/travis/collective/collective.googlenews/master.svg
    :target: http://travis-ci.org/collective/collective.googlenews

.. image:: https://img.shields.io/coveralls/collective/collective.googlenews/master.svg
    :target: https://coveralls.io/r/collective/collective.googlenews


Introduction
============

`Google News`_ is compiled solely by a computer algorithm that scans all the
sites included in their system. In order for your content to be included in
`Google News`_, the layout and format of your site must be easy for their
crawler to read and decipher. Additionally, they have certain restrictions in
place to make sure their crawler only includes links to URLs that are actually
news articles.

Google asks that you to review all of their guidelines before submitting your
site for inclusion in `Google News`_. Making sure your site conforms to all
their `technical requirements`_ now will help prevent any issues with your
site in the future.

This package helps you make your Plone site comply with these `technical
requirements`_.

Installation
============

To enable this product in a buildout-based installation:

1. Edit your buildout.cfg and add ``collective.googlenews`` to the list of eggs to install::

    [buildout]
    ...
    eggs =
        collective.googlenews

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``collective.googlenews`` and click the 'Activate' button.

Article URLs
============

URL need to display a three-digit number. This add-on override the url
normalizer to add a unique id.

SiteMap
=======

This add-on add a **@@googlenews-sitemap.xml** view for topic content type. This
view add some checks before loading items:

* no more than 1000 items returned
* items must have been published in the last two days
* items are ordered on the effective date (reversed)

So you don't need to add criteria for these, but types should be set to News
Item to be sure you are publishing news.

How to publish my website into Google News ?
============================================

You need to have a topic instance in your website. By default in Plone
**/news/aggregator** is the one. In the process you can provide the sitemap to
help google to get the last news by providing the url
``example.com/news/aggregator/@@googlenews-sitemap.xml``.

Contribute
==========

- Issue Tracker: https://github.com/collective/collective.googlenews/issues
- Source Code: https://github.com/collective/collective.googlenews
- Google News technical requirements: https://support.google.com/news/publisher/answer/2481358?topic=2481296

License
=======

The project is licensed under the GPLv2.

.. _`Google News`: https://news.google.com/
.. _`technical requirements`: https://support.google.com/news/publisher/answer/2481358?topic=2481296
