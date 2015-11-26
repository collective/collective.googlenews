# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import common as base


class GoogleNewsMetaTagViewlet(base.ViewletBase):

    """Viewlet to include Google News meta tags."""

    def news_keywords(self):
        return ', '.join(self.context.news_keywords)
