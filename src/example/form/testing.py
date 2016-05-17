# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import example.form


class ExampleFormLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=example.form)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'example.form:default')


EXAMPLE_FORM_FIXTURE = ExampleFormLayer()


EXAMPLE_FORM_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EXAMPLE_FORM_FIXTURE,),
    name='ExampleFormLayer:IntegrationTesting'
)


EXAMPLE_FORM_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EXAMPLE_FORM_FIXTURE,),
    name='ExampleFormLayer:FunctionalTesting'
)


EXAMPLE_FORM_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        EXAMPLE_FORM_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='ExampleFormLayer:AcceptanceTesting'
)
