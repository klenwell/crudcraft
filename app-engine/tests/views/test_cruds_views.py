"""
# Cruds View Test

To run individually:

    nosetests -c nose.cfg tests/controllers/test_cruds_controller.py
"""
import json

from controllers.cruds import app as cruds_controller
from models.crud import Crud

from tests.helper import (AppEngineControllerTest, parse_html, MockIdentityService, redirect_path,
                          extract_id_from_url)
from tests.fixtures import guest_fixture
from models.guest import Guest


class CrudsViewsTest(AppEngineControllerTest):
    #
    # Tests
    #
    def test_expects_index_to_not_show_create_button_to_unauthenticated_user(self):
        # Arrange
        client = cruds_controller.test_client()
        guest = MockIdentityService.unauthenticated_guest(self)
        endpoint = '/cruds/'
        button_selector = 'a.btn.create-crud'

        # Assume
        self.assertFalse(guest.is_authenticated())

        # Act
        response = client.get(endpoint, follow_redirects=False)
        html = parse_html(response.data)
        button = html.select(button_selector) if html else None

        # Assert
        self.assertEqual(response.status_code, 200, html)
        self.assertEqual(len(button), 0, html)

    def test_expects_index_to_not_show_create_button_to_authenticated_user(self):
        # Arrange
        client = cruds_controller.test_client()
        guest = MockIdentityService.login_app_engine_user(self)
        endpoint = '/cruds/'
        button_selector = 'a.btn.create-crud'

        # Assume
        self.assertTrue(guest.is_authenticated())

        # Act
        response = client.get(endpoint, follow_redirects=False)
        html = parse_html(response.data)
        button = html.select(button_selector) if html else None

        # Assert
        self.assertEqual(response.status_code, 200, html)
        self.assertEqual(len(button), 0, html)

    def test_expects_index_to_show_create_button_to_admin_user(self):
        # Arrange
        client = cruds_controller.test_client()
        admin = MockIdentityService.login_app_engine_user(self, as_admin=True)
        endpoint = '/cruds/'
        button_selector = 'a.btn.create-crud'

        # Assume
        self.assertTrue(admin.is_admin())

        # Act
        response = client.get(endpoint, follow_redirects=False)
        html = parse_html(response.data)
        button = html.select(button_selector) if html else None

        # Assert
        self.assertEqual(response.status_code, 200, html)
        self.assertEqual(len(button), 1, html)
