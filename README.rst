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

`Google News`_ is a computer-generated news service that aggregates headlines from more than 50,000 news sources worldwide,
grouping similar stories together, and displaying them according to each reader's interests.

In order for your content to be included in `Google News`_,
Google has certain restrictions in place to make sure their crawler only includes links to URLs that are actually news articles.

Google also asks you to review all of their guidelines before submitting your site for inclusion in `Google News`_.

This package helps you make your Plone site comply with Google's `technical requirements`_.

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

Google News Sitemap
===================

This add-on adds a ``@@googlenews-sitemap.xml`` view accessible on ``INavigationRoot`` context.
The view complies with Google News `sitemap guidelines`_,
listing only URLs for news articles published in the last two days,
and having no more than 1,000 items.

By default, the News sitemap includes only instances of the ``News Item`` content type in your site.
This can be changed into Google News configlet at 'Site Setup'.

Submitting your News sitemap
----------------------------

You can submit your News sitemap using the `Google Search Console`_.
Your News sitemap URL is something like:

    http://www.example.org/@@googlenews-sitemap.xml

Note that your site must be already included in Google News.
If it's not, you can apply for inclusion within the `Google News Publisher Center`_.

Editors' Picks feeds
====================

`Editors' Picks`_ enables you to provide up to five links to original news content you believe represents your organization's best journalistic work at any given moment,
and potentially have it displayed on the Google News homepage or select section pages.

Adding an Editors' Picks feed
-----------------------------

* In 'Site Setup', select the Google News configlet
* Add a logo that complies with the image guidelines
* Create a collection that lists up to five news items
* Submit the Atom feed associated with the collection into the `Google News Publisher Center`_

Contribute
==========

- Issue Tracker: https://github.com/collective/collective.googlenews/issues
- Source Code: https://github.com/collective/collective.googlenews

License
=======

The project is licensed under the GPLv2.

.. _`Editors' Picks`: https://support.google.com/news/publisher/answer/1407682
.. _`Google News Publisher Center`: https://partnerdash.google.com/partnerdash/d/news
.. _`Google News`: https://news.google.com/
.. _`Google Search Console`: https://www.google.com/webmasters/tools
.. _`sitemap guidelines`: https://support.google.com/news/publisher/answer/74288
.. _`technical requirements`: https://support.google.com/news/publisher/answer/2481358
