import random
from Acquisition import aq_base

from zope import component
from zope import interface
from zope.component import getMultiAdapter, getUtility

from collective.googlenews import interfaces
from collective.googlenews.interfaces import GoogleNewsSettings

try:
    from plone.registry.interfaces import IRegistry
    from plone.app.content.interfaces import INameFromTitle
except ImportError, e:
    class IRegistry(interface.Interface):
        pass
    class INameFromTitle(interface.Interface):
        pass


def randomid():
    return '-'+str(random.randint(100, 9999))+'.html'

def generateNewId(self, name=None, object=None):
    #its a dexterity ct
    if hasattr(self, '_old_chooseName'):
        newid = self._old_chooseName(name, object)
        request = getattr(self.context, 'REQUEST', None)
        self = object
    else:
        newid = self._old_generateNewId()
        request = getattr(self, 'REQUEST', None)
    if not interfaces.IGoogleNewsLayer.providedBy(request):
        return newid
    #the addon is activate, check the content type
    settings = getUtility(IRegistry).forInterface(GoogleNewsSettings, False)
    try:
        if hasattr(settings, 'portal_types'):
            portal_types = settings.portal_types
        else:
            portal_types = ['News Item']
    except KeyError, e:
        portal_types = ['News Item']
    if getattr(self,'portal_type') in portal_types:
        if newid is not None:
            newid += randomid()
    return newid


class NameFromTitle(object):
    """Name chooser to fit google news constraints"""
    interface.implements(INameFromTitle)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return self.context.Title() + randomid()