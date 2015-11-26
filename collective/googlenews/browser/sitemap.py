# -*- coding: utf-8 -*-
from collective.googlenews.interfaces import GoogleNewsSettings
from DateTime import DateTime
from plone import api
from Products.Five import BrowserView


class GoogleNewsSiteMap(BrowserView):

    """News sitemap view. It generates an XML file you can submit to
    Google Search Console.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _brain2news(self, brain):
        """Transform brain into sitemap-ready data."""
        return {
            'loc': brain.getURL(),
            'publication_date': brain.EffectiveDate,
            'title': brain.Title,
        }

    def news(self):
        """Return news articles for the News sitemap.

        Complies with Google News sitemap guidelines, listing only URLs
        for news articles published in the last two days, and returning
        no more than 1,000 items.
        """
        portal_types = api.portal.get_registry_record(
            GoogleNewsSettings.__identifier__ + '.portal_types')

        catalog = api.portal.get_tool('portal_catalog')
        results = catalog(
            portal_type=portal_types,
            sort_on='effective',
            sort_order='reverse',
            sort_limit=1000,
            effective=dict(query=DateTime() - 2, range='min'),
        )
        return [self._brain2news(b) for b in results]

    def portal_title(self):
        """Return the portal title."""
        return api.portal.get().Title()

    def portal_language(self):
        """Return the portal language."""
        language = api.portal.get().language
        if language in ('zh-cn', 'zh-tw'):
            return language
        return language[:2]
