from zope import interface
from zope import schema

from collective.googlenews import i18n

class IGoogleNewsLayer(interface.Interface):
    """browser layer for this addon"""

class GoogleNewsSettings(interface.Interface):
    """Settings site wide of this addon"""
    
    portal_types = schema.List(title=i18n.portal_types_title,
                               description=i18n.portal_types_desc,
                               value_type=schema.ASCIILine(title=i18n.portal_type_title))


try:
    from Products.ATContentTypes.interface import IATTopic
except ImportError, e:
    from Products.ATContentTypes.interfaces import IATTopic
