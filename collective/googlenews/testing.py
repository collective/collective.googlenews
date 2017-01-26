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


IS_PLONE_5 = api.env.plone_version().startswith('5')

IMAGES = [
    'logo_plone_not_transparent.png',
    'logo_plone_ok.png',
    'logo_plone_wrong_filetype.jpg',
    'logo_plone_wrong_size.png'
]


def _setup_content(n, in_the_past=False):
    """Create and publish dummy content with random ids."""
    from DateTime import DateTime
    from uuid import uuid1
    context = api.portal.get()
    for i in range(0, n):
        with api.env.adopt_roles(['Manager']):
            id_ = uuid1().hex[:8]  # generate random id
            obj = api.content.create(
                context, 'Dexterity Item', id_, standout_journalism=True)
            api.content.transition(obj=obj, transition='publish')
            if in_the_past:
                obj.effective_date = DateTime('01/01/2000')
            else:
                # XXX: api.content.transition doesn't set effective_date
                #      https://github.com/plone/plone.api/issues/343
                obj.effective_date = DateTime()
            obj.reindexObject()


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


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name='collective.googlenews:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name='collective.googlenews:Functional')


class RobotFixture(Fixture):

    """This fixture adds content to test the standout journalism validator."""

    def setUpPloneSite(self, portal):
        super(RobotFixture, self).setUpPloneSite(portal)
        # create and publish 6 items marked as standout journalism
        _setup_content(6)

ROBOT_FIXTURE = RobotFixture()

ROBOT_TESTING = FunctionalTesting(
    bases=(ROBOT_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='collective.googlenews:Robot',
)
