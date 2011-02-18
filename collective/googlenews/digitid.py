import random
from zope import component
from zope import interface
try:
    from plone.registry.interfaces import IRegistry
except ImportError, e:
    class IRegistry(interface.Interface):
        pass

def generateNewId(self):
    #TODO: check the add-on is installed (request/browserlayer)
    
    registry = component.getUtility(IRegistry, None)
    newid = self._old_generateNewId()
    try:
        if registry:
            portal_types = registry['collective.googlenews.interfaces.IGoogleNewsSettings.portal_types']
        else:
            portal_types = ['News Item']
    except KeyError, e:
        portal_types = ['News Item']
    if getattr(self,'portal_type') in portal_types:
        if newid is not None:
            newid += str(random.randint(100, 9999))+'.html'
    return newid
