# -*- coding: utf-8 -*-
from collective.googlenews.behaviors.interfaces import IGoogleNews
from collective.googlenews.interfaces import GoogleNewsSettings
from collective.googlenews.utils import get_current_standout_journalism
from plone import api
from plone.formwidget.namedfile.converter import b64decode_file
from plone.namedfile.browser import Download
from plone.namedfile.file import NamedImage
from Products.Five.browser import BrowserView


class GoogleNewsLogo(Download):

    """Return Google News logo data"""

    def __init__(self, context, request):
        """Set Google News logo data if available."""
        super(GoogleNewsLogo, self).__init__(context, request)
        self.filename = None
        self.data = None

        logo = api.portal.get_registry_record(
            GoogleNewsSettings.__identifier__ + '.logo')

        if logo is not None:
            # set Google News logo data for download
            filename, data = b64decode_file(logo)
            data = NamedImage(data=data, filename=filename)
            self.data = data
            self.filename = filename

    def _getFile(self):
        """Return Google News logo data."""
        return self.data


class GoogleNewsHelper(BrowserView):
    """Helper view to be used as a workflow transition guard."""

    @property
    def publish_transition_allowed(self):
        """Check if the publish transition is allowed.

        This workflow guard only takes care of content being published;
        content being edited is checked within an invariant.
        """
        if not IGoogleNews.providedBy(self.context):
            return True  # behavior is not enabled in this context

        if not self.context.standout_journalism:
            return True  # this is not standout journalism

        results = get_current_standout_journalism()
        # there should never be more than 7 items marked as
        # standout journalism at any given time
        assert len(results) <= 7
        if len(results) < 7:
            return True

        return False
