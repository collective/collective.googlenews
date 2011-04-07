import random
from Acquisition import aq_base
from collective.googlenews import interfaces
from plone.app.content import namechooser
from zope import component
from zope import interface
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

def generateNewId(self):
    newid = self._old_generateNewId()
    request = getattr(self, 'REQUEST', None)
    if request is not None:
        if not interfaces.IGoogleNewsLayer.providedBy(request):
            #the addon is not activated -> stay on old way to generate ids
            return newid
    #the addon is activate, check the content type
    registry = component.queryUtility(IRegistry, None)
    try:
        if registry:
            portal_types = registry['collective.googlenews.interfaces.IGoogleNewsSettings.portal_types']
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
    component.adapts(interfaces.INewsItem)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        id = aq_base.getId()
        title = getattr(aq_base(object), 'id', None)
        title += randomid()
        return title

