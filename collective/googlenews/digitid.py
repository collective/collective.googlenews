import random
from zope import component
from plone.registry.interfaces import IRegistry

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
            newid += str(random.randint(100, 9999))+'.html'
    return newid
