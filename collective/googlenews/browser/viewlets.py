# -*- coding: utf-8 -*-
from collective.googlenews.utils import get_current_standout_journalism
from plone import api
from plone.app.layout.viewlets.common import ViewletBase


class GoogleNewsMetaTagViewlet(ViewletBase):

    """Viewlet to include Google News meta tags."""

    def news_keywords(self):
        return ', '.join(self.context.news_keywords)


class GoogleNewsWarningViewlet(ViewletBase):
    """Viewlet to show a warning message alerting the user when the
    "Publish" workflow transition is disabled.
    """

    @property
    def enabled(self):
        """Check if the warning viewlet will be shown."""
        if api.content.get_state(self.context) == 'published':
            return False  # item is already published

        if not self.context.standout_journalism:
            return False  # this is not standout journalism

        results = get_current_standout_journalism()
        # there should never be more than 7 items marked as
        # standout journalism at any given time
        assert len(results) <= 7
        if len(results) < 7:
            return False

        return True
