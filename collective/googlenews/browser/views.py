# -*- coding: utf-8 -*-
from collective.googlenews.interfaces import GoogleNewsSettings
from plone import api
from plone.formwidget.namedfile.converter import b64decode_file
from plone.namedfile.browser import Download
from plone.namedfile.file import NamedImage


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
