from zope import interface
from zope import schema

class IGoogleNewsLayer(interface.Interface):
    """browser layer for this addon"""

class GoogleNewsSettings(interface.Interface):
    """Settings site wide of this addon"""
    