# -*- coding: utf-8 -*-
from collective.googlenews import _
from collective.googlenews.logger import logger
from cStringIO import StringIO
from DateTime import DateTime
from PIL import Image
from plone import api
from plone.formwidget.namedfile.converter import b64decode_file
from zope.interface import Invalid


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

    img = Image.open(StringIO(data))

    # check format
    if img.format != 'PNG':
        raise Invalid(_(u'Image should be in PNG format.'))

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


def get_current_standout_journalism():
    """Return content currently marked as standout journalism.

    :returns: a list of objects marked as standout journalism
    :rtype: list of content type instances
    :raises AssertionError: if there are more than 7 items
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
    msg = 'There are currently {0} items marked as standout'
    logger.info(msg.format(len(results)))
    logger.info(repr([b.id for b in results]))
    return [b.getObject() for b in results]


def get_workflows_with_publish_transition():
    wf_tool = api.portal.get_tool('portal_workflow')
    workflows = []
    for id_ in wf_tool.listWorkflows():
        wf = wf_tool.getWorkflowById(id_)
        if 'publish' in wf.transitions:
            workflows.append(wf)
    return workflows
