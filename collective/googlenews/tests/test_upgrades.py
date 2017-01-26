# -*- coding: utf-8 -*-
from collective.googlenews.config import PROJECTNAME
from collective.googlenews.testing import INTEGRATION_TESTING
from plone import api

import unittest


PROFILE = PROJECTNAME + ':default'


class UpgradeTestCaseBase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self, from_version, to_version):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']
        self.from_version = from_version
        self.to_version = to_version

    def _get_upgrade_step(self, title):
        """Get one of the upgrade steps.

        :param title: [required] the title used to register the upgrade step
        :type obj: str
        """
        self.setup.setLastVersionForProfile(PROFILE, self.from_version)
        upgrades = self.setup.listUpgrades(PROFILE)
        steps = [s for s in upgrades[0] if s['title'] == title]
        return steps[0] if steps else None

    def _do_upgrade_step(self, step):
        """Execute an upgrade step.

        :param step: [required] the step we want to run
        :type step: str
        """
        request = self.layer['request']
        request.form['profile_id'] = PROFILE
        request.form['upgrades'] = [step['id']]
        self.setup.manage_doUpgrades(request=request)

    def _how_many_upgrades_to_do(self):
        self.setup.setLastVersionForProfile(PROFILE, self.from_version)
        upgrades = self.setup.listUpgrades(PROFILE)
        assert len(upgrades) > 0
        return len(upgrades[0])


class Upgrade1001to1002TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'1001', u'1002')

    def test_upgrade_to_1002_registrations(self):
        version = self.setup.getLastVersionForProfile(PROFILE)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self._how_many_upgrades_to_do(), 1)

    def test_update_portal_catalog(self):
        # check if the upgrade step is registered
        title = u'Update portal catalog'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        catalog = api.portal.get_tool('portal_catalog')
        # remove indexes
        catalog.delIndex('standout_journalism')
        catalog.delIndex('news_keywords')
        self.assertNotIn('standout_journalism', catalog.Indexes)
        self.assertNotIn('news_keywords', catalog.Indexes)
        # remove metadata
        catalog.delColumn('standout_journalism')
        catalog.delColumn('news_keywords')
        self.assertNotIn('standout_journalism', catalog.schema())
        self.assertNotIn('news_keywords', catalog.schema())

        # run the upgrade step to validate the update
        self._do_upgrade_step(step)
        self.assertIn('standout_journalism', catalog.Indexes)
        self.assertIn('news_keywords', catalog.Indexes)
        self.assertIn('standout_journalism', catalog.schema())
        self.assertIn('news_keywords', catalog.schema())


class Upgrade1002to1003TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'1002', u'1003')

    def test_upgrade_to_1003_registrations(self):
        version = self.setup.getLastVersionForProfile(PROFILE)[0]
        assert int(version) >= int(self.to_version)
        self.assertEqual(self._how_many_upgrades_to_do(), 1)

    def test_update_portal_catalog(self):
        # check if the upgrade step is registered
        title = u'Add guard expressions'
        step = self._get_upgrade_step(title)
        assert step is not None

        # simulate state on previous version
        from collective.googlenews.config import GUARD_EXPRESSION
        from collective.googlenews.setuphandlers import remove_guard_expressions
        from collective.googlenews.utils import get_workflows_with_publish_transition
        remove_guard_expressions()
        for wf in get_workflows_with_publish_transition():
            assert wf.transitions['publish'].guard.getExprText() == ''

        # run the upgrade step to validate the update
        self._do_upgrade_step(step)
        for wf in get_workflows_with_publish_transition():
            self.assertEqual(wf.transitions['publish'].guard.getExprText(), GUARD_EXPRESSION)
