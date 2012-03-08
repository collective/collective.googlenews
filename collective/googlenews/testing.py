from plone.testing import z2

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting

class AddOnLayer(PloneSandboxLayer):
    default_bases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.googlenews
        self.loadZCML(package=collective.googlenews)

        # Install product and call its initialize() function
        z2.installProduct(app, 'collective.googlenews')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.googlenews:default')

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, 'collective.googlenews')

FIXTURE = AddOnLayer()

INTEGRATION = IntegrationTesting(bases=(FIXTURE,), name="GoogleNews:Integration")
FUNCTIONAL = FunctionalTesting(bases=(FIXTURE,), name="GoogleNews:Functional")
