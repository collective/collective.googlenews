# -*- coding: utf-8 -*-
from collective.googlenews import _
from collective.googlenews.interfaces import GoogleNewsEditorsPicksGroup
from collective.googlenews.interfaces import GoogleNewsSettings
from collective.googlenews.interfaces import IGoogleNewsSchema
from plone.app.registry.browser import controlpanel as base
from plone.formwidget.namedfile.widget import NamedImageFieldWidget
from plone.registry.interfaces import IRegistry
from zope.component._api import getUtility
from zope.interface import alsoProvides


class SettingsEditForm(base.RegistryEditForm):

    """Google News control panel settings form."""

    schema = IGoogleNewsSchema
    label = _(u"Google News Settings")
    description = _(u"controlpanel_desc",
                    default=u"You can configure the settings of collective.googlenews add-on")

    fields = GoogleNewsSettings
    groups = (GoogleNewsEditorsPicksGroup,)

    def getContent(self):
        """Set multiple registry schema."""
        return AbstractRecordsProxy(self.schema)

    def updateFields(self):
        """Change Google News logo widget."""
        super(SettingsEditForm, self).updateFields()
        group = self.groups[0]
        group.fields['logo'].widgetFactory = NamedImageFieldWidget


class AbstractRecordsProxy(object):
    """Multiple registry schema proxy.

    This class supports schemas that contain derived fields. The
    settings will be stored with respect to the individual field
    interfaces.
    """

    def __init__(self, schema):
        state = self.__dict__
        state['__registry__'] = getUtility(IRegistry)
        state['__proxies__'] = {}
        state['__schema__'] = schema
        alsoProvides(self, schema)

    def __getattr__(self, name):
        try:
            field = self.__schema__[name]
        except KeyError:
            raise AttributeError(name)
        else:
            proxy = self._get_proxy(field.interface)
            return getattr(proxy, name)

    def __setattr__(self, name, value):
        try:
            field = self.__schema__[name]
        except KeyError:
            self.__dict__[name] = value
        else:
            proxy = self._get_proxy(field.interface)
            return setattr(proxy, name, value)

    def __repr__(self):
        return '<AbstractRecordsProxy for %s>' % self.__schema__.__identifier__

    def _get_proxy(self, interface):
        proxies = self.__proxies__
        return proxies.get(interface) or proxies.setdefault(interface, self.__registry__.forInterface(interface))


class ControlPanelView(base.ControlPanelFormWrapper):

    """Control Panel Form Wrapper."""

    form = SettingsEditForm
