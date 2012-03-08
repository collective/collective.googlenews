*********************
collective.googlenews
*********************

.. contents:: Table of Contents

Introduction
============

`Google News`_ service has some technical requirements. This add-on solve the
only issues Plone have regarding these constraints. Lets Plone be `Google News`_
ready.

Technical requirements can be found at
http://www.google.com/support/news_pub/bin/topic.py?hl=en&topic=11665

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
