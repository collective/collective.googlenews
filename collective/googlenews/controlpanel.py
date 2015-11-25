# -*- coding: utf-8 -*-
from collective.googlenews import _
from collective.googlenews.interfaces import GoogleNewsSettings
from plone.app.registry.browser import controlpanel as base
from plone.formwidget.namedfile.widget import NamedImageFieldWidget


class GoogleNewsSettingsEditForm(base.RegistryEditForm):

    """Google News control panel settings form."""

    schema = GoogleNewsSettings
    label = _(u"Google News Settings")
    description = _(u"controlpanel_desc",
                    default=u"You can configure the settings of collective.googlenews add-on")

    def updateFields(self):
        """Update logo widget."""
        super(GoogleNewsSettingsEditForm, self).updateFields()
        self.fields['logo'].widgetFactory = NamedImageFieldWidget


class GoogleNewsControlPanelView(base.ControlPanelFormWrapper):

    """Control Panel Form Wrapper."""

    form = GoogleNewsSettingsEditForm
