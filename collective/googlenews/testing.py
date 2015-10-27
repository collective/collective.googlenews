# -*- coding: utf-8 -*-

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import os
import shutil


IMAGES = [
    'logo_plone_not_transparent.png',
    'logo_plone_ok.png',
    'logo_plone_wrong_filetype.jpg',
    'logo_plone_wrong_size.png'
]


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.googlenews
        self.loadZCML(package=collective.googlenews)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.googlenews:default')

        current_dir = os.path.abspath(os.path.dirname(__file__))
        for img in IMAGES:
            img_path = os.path.join(current_dir, 'tests', img)
            shutil.copy2(img_path, '/tmp')


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='collective.googlenews:Integration',
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='collective.googlenews:Functional',
)
