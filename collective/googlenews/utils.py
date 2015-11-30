# -*- coding: utf-8 -*-
from collective.googlenews import _
from DateTime import DateTime
from PIL import Image
from plone import api
from plone.formwidget.namedfile.converter import b64decode_file
from zope.interface import Invalid

import cStringIO
import os


def validate_logo(value):
    """Validate the image to be used in the feed.

    The image must follow these specifications:
    * Image should be .png format
    * Image dimensions must match one of two options:
      * height between 20 and 40px, width of 250px
      * height of 40px, width between 125 and 250px
    * Image background should be transparent

    :param value: Image encoded into base64 to be validated
    :type value: string
    :raises:
        :class:`~zope.interface.Invalid` if the image is not valid
    """
    if not value:
        return True

    filename, data = b64decode_file(value)

    # check extension
    name, extension = os.path.splitext(filename)
    if extension != u'.png':
        raise Invalid(_(u'Image should be in PNG format.'))

    stream = cStringIO.StringIO(data)
    img = Image.open(stream)

    # Check image size
    width, height = img.size
    if not((20 <= height <= 40 and width == 250) or
       (height == 40 and 125 <= width <= 250)):
        raise Invalid(_(
            u'Image should have height beetween 20px and 40px and width equal 250px '
            u'or height equal 40px and width beetween 125px and 250px.'
        ))

    # Check image transparency.
    if not((img.mode in ('RGBA', 'LA')) or
       (img.mode == 'P' and 'transparency' in img.info)):
        raise Invalid(_(u'Image should have transparency layer.'))

    return True


def _valid_as_standout_journalism():
    """Check there are currently less than seven news articles marked as
    standout journalism in the past calendar week.
    """
    catalog = api.portal.get_tool('portal_catalog')
    date_range = dict(query=DateTime() - 7, range='max')
    results = catalog(standout_journalism=True, effective=date_range)
    return len(results) < 7
