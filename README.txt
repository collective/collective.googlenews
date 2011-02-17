Introduction
============

GoogleNews_ service has some technical requirements. This add-on solve some issues
and let Plone be GoogleNews_ ready.

Technical requirements can be found at http://www.google.com/support/news_pub/bin/topic.py?hl=en&topic=11665

Article URLs
============

URL need to display a three-digit number. This add-on override the url normalizer
to add a unique id.

SiteMap
=======

This add-on add a @@googlenews-sitemap.xml view for topic content type. This 
view add some checks:

* no more than 1000 items returned
* items must have been published in the last two days
* items are ordered on the effective date (reversed)

So you don't need to add criteria for these, but types
should be set to News Item to be sure you are publishing news.
