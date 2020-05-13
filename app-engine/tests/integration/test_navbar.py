"""
# Navbar Integration Test

To run individually:

    nosetests -c nose.cfg tests/integration/test_navbar.py
"""
from controllers.pages import app as pages_controller

from tests.helper import (AppEngineControllerTest, MockIdentityService, parse_html)


class NavbarIntegrationTest(AppEngineControllerTest):
    def test_should_display_navbar_to_any_guest(self):
        # Arrange
        client = pages_controller.test_client()
        unauthenticated_guest = MockIdentityService.unauthenticated_guest(self)

        # Assume
        self.assertFalse(unauthenticated_guest.is_authenticated())

        # Act
        response = client.get('/')
        html = parse_html(response.data)
        navbar = html.select_one('nav.navbar')

        # Assert
        self.assertEqual(response.status_code, 200, response.data)
        self.assertIsNotNone(navbar, html)

    def test_should_display_cruds_tab_in_navbar_to_any_guest(self):
        # Arrange
        client = pages_controller.test_client()
        unauthenticated_guest = MockIdentityService.unauthenticated_guest(self)

        # Assume
        self.assertFalse(unauthenticated_guest.is_authenticated())

        # Act
        response = client.get('/')
        html = parse_html(response.data)
        cruds_tab = html.select_one('nav.navbar li.cruds')

        # Assert
        self.assertEqual(response.status_code, 200, response.data)
        self.assertIsNotNone(cruds_tab, html)
