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


def _valid_as_standout_journalism(context):
    """Check there are currently less than seven published news articles
    marked as standout journalism in the past calendar week.

    :param context: the object being validated
    :type context: Dexterity-based content type instance or None
    :returns: True if we can mark this object as standout journalism
    :rtype: bool
    """
    record = 'collective.googlenews.interfaces.GoogleNewsSettings.portal_types'
    portal_types = api.portal.get_registry_record(record)
    catalog = api.portal.get_tool('portal_catalog')
    query = dict(
        portal_type=portal_types,
        standout_journalism=True,
        effective=dict(query=DateTime() - 7, range='min'),
        review_state='published',
    )
    results = catalog(**query)

    # to validate, we will need a list of object UUIDs
    results = [b.getObject() for b in results]
    results = [api.content.get_uuid(o) for o in results]

    # we could have false positives if we are editing an item already marked
    if context is not None:  # we are not adding, but editing
        uuid = api.content.get_uuid(context)
        if uuid in results:  # if the UUID is there, ignore it
            results.remove(uuid)

    # XXX: there's still a potential source of problems here:
    #      suppose we have six news articles marked as standout and we
    #      create another two; as they are not published yet, both can
    #      be marked and published after that.
    #      so, we ended with eight news articles marked as standout.
    #      we should work with workflow scripts to avoid that.

    return len(results) < 7
