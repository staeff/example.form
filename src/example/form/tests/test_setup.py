# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from example.form.testing import EXAMPLE_FORM_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that example.form is properly installed."""

    layer = EXAMPLE_FORM_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if example.form is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'example.form'))

    def test_browserlayer(self):
        """Test that IExampleFormLayer is registered."""
        from example.form.interfaces import (
            IExampleFormLayer)
        from plone.browserlayer import utils
        self.assertIn(IExampleFormLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = EXAMPLE_FORM_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['example.form'])

    def test_product_uninstalled(self):
        """Test if example.form is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'example.form'))

    def test_browserlayer_removed(self):
        """Test that IExampleFormLayer is removed."""
        from example.form.interfaces import IExampleFormLayer
        from plone.browserlayer import utils
        self.assertNotIn(IExampleFormLayer, utils.registered_layers())
