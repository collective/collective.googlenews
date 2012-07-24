# -*- coding: utf-8 -*-

from plone.app.registry.browser import controlpanel as base

from collective.googlenews import _
from collective.googlenews.interfaces import GoogleNewsSettings


class SettingsEditForm(base.RegistryEditForm):

    schema = GoogleNewsSettings
    label = _(u"Google News Settings")
    description = _(u"controlpanel_desc",
                    default=u"You can configure the settings of collective.googlenews add-on")

    def updateWidgets(self):
        super(SettingsEditForm, self).updateWidgets()
        self.widgets['portal_types'].style = u'min-width: 200px;'


class ControlPanelView(base.ControlPanelFormWrapper):
    form = SettingsEditForm
