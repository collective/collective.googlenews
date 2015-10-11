import random

from zope import component
from zope import interface

from collective.googlenews import interfaces
from collective.googlenews.interfaces import GoogleNewsSettings

from plone.registry.interfaces import IRegistry
from plone.app.content.interfaces import INameFromTitle


def randomid():
    return '-' + str(random.randint(100, 9999)) + '.html'


def generateNewId(self, name=None, instance=None):
    # its a dexterity ct
    if hasattr(self, '_old_chooseName'):
        newid = self._old_chooseName(name, instance)
        request = getattr(self.context, 'REQUEST', None)
    else:
        newid = self._old_generateNewId()
        request = getattr(self, 'REQUEST', None)
    if not interfaces.IGoogleNewsLayer.providedBy(request):
        return newid
    # the addon is activate, check the content type
    registry = component.queryUtility(IRegistry, None)
    try:
        portal_types = ['News Item']
        if registry:
            settings = registry.forInterface(GoogleNewsSettings, False)
            if hasattr(settings, 'portal_types'):
                portal_types = settings.portal_types
    except:
        portal_types = ['News Item']
    if not instance:
        instance = self
    if getattr(instance, 'portal_type') in portal_types:
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
