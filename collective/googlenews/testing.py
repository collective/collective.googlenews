# -*- coding: utf-8 -*-
"""Setup testing infrastructure.

For Plone 5 we need to install plone.app.contenttypes.
"""
from plone import api
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import os
import pkg_resources
import shutil

try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    from plone.app.testing import PLONE_FIXTURE
else:
    from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE as PLONE_FIXTURE

IMAGES = [
    'logo_plone_not_transparent.png',
    'logo_plone_ok.png',
    'logo_plone_wrong_filetype.jpg',
    'logo_plone_wrong_size.png'
]


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.googlenews
        self.loadZCML(package=collective.googlenews)
        self.loadZCML(package=collective.googlenews, name='testing.zcml')

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.googlenews:default')
        self.applyProfile(portal, 'collective.googlenews:testfixture')

        # use simple_publication_workflow all over the place
        portal.portal_workflow.setDefaultChain('simple_publication_workflow')

        # configure our dummy content type as the one to be used
        record = 'collective.googlenews.interfaces.GoogleNewsSettings.portal_types'
        api.portal.set_registry_record(record, ['Dexterity Item'])

        current_dir = os.path.abspath(os.path.dirname(__file__))
        for img in IMAGES:
            img_path = os.path.join(current_dir, 'tests', img)
            shutil.copy2(img_path, '/tmp')


class RobotFixture(Fixture):

    """This fixture adds content to test the standout journalism validator."""

    def setUpPloneSite(self, portal):
        super(RobotFixture, self).setUpPloneSite(portal)
        from DateTime import DateTime
        from plone import api

        with api.env.adopt_roles(['Manager']):
            folder = api.content.create(portal, 'Folder', 'folder')

            # we will create and publish 7 news articles
            for i in range(0, 7):
                obj = api.content.create(
                    folder, 'Dexterity Item', str(i), standout_journalism=True)
                api.content.transition(obj, transition='publish')
                obj.setEffectiveDate(DateTime())
                obj.reindexObject()

        # one of them will be set as published one week in the past
        folder['0'].setEffectiveDate(DateTime() - 8)
        folder['0'].reindexObject()

FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='collective.googlenews:Integration',
)

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='collective.googlenews:Functional',
)

ROBOT_FIXTURE = RobotFixture()

ROBOT_TESTING = FunctionalTesting(
    bases=(ROBOT_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='collective.googlenews:Robot')
