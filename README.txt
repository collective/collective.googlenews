*********************
collective.googlenews
*********************

.. contents:: Table of Contents

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

Article URLs
============

URL need to display a three-digit number. This add-on override the url
normalizer to add a unique id.

SiteMap
=======

This add-on add a @@googlenews-sitemap.xml view for topic content type. This
view add some checks before loading items:

* no more than 1000 items returned
* items must have been published in the last two days
* items are ordered on the effective date (reversed)

So you don't need to add criteria for these, but types should be set to News
Item to be sure you are publishing news.

How to publish my website into Google News ?
============================================

You need to have a topic instance in your website. By default in Plone
/news/aggregator is the one. In the process you can provide the sitemap to
help google to get the last news by providing the url
example.com/news/aggregator/@@googlenews-sitemap.xml

.. _`Google News`: https://news.google.com/
.. _`technical requirements`: https://support.google.com/news/publisher/bin/answer.py?answer=2481358&topic=2481296

