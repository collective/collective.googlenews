from plone.app.registry.browser import controlpanel as base
from plone.z3cform import layout

from collective.googlenews import interfaces
from collective.googlenews import i18n

class SettingsEditForm(base.RegistryEditForm):

    schema = interfaces.GoogleNewsSettings
    label = i18n.controlpanel_label
    description = i18n.controlpanel_desc

ControlPanelView = layout.wrap_form(SettingsEditForm, base.ControlPanelFormWrapper)
