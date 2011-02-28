import random
from zope import component
from zope import interface
from plone.registry.interfaces import IRegistry
from collective.googlenews import interfaces

def randomid():
    return str(random.randint(100, 9999))+'.html'

def generateNewId(self):
    #TODO: check the add-on is installed (request/browserlayer)
    registry = component.getUtility(IRegistry)
    newid = self._old_generateNewId()
    try:
        portal_types = registry['collective.googlenews.interfaces.IGoogleNewsSettings.portal_types']
    except KeyError, e:
        portal_types = ['News Item']
    if getattr(self,'portal_type') in portal_types:
        if newid is not None:
            newid += randomid()
    return newid

from plone.app.content import namechooser
from Acquisition import aq_base

class NameFromTitle(object):
    """Name chooser to fit google news constraints"""
    interface.implements(INameFromTitle)
    component.adapts(interfaces.INewsItem)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        id = aq_base.getId()
        title = getattr(aq_base(object), 'id', None)
        title += randomid()
        return title

