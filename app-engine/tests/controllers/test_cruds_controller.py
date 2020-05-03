"""
# Cruds Controller Test

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


class CrudsControllerTest(AppEngineControllerTest):
    #
    # Tests
    #
    def test_expects_to_get_index(self):
        # Arrange
        client = cruds_controller.test_client()

        # Assume
        endpoint = '/cruds/'
        page_selector = 'div#cruds-index'

        # Act
        response = client.get(endpoint, follow_redirects=False)
        html = parse_html(response.data)
        page = html.select(page_selector) if html else None

        # Assert
        self.assertEqual(response.status_code, 200, html)
        self.assertEqual(len(page), 1, html)

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

    def test_expects_admin_to_create_crud(self):
        # Arrange
        client = cruds_controller.test_client()
        admin = MockIdentityService.login_app_engine_user(self, as_admin=True)
        endpoint = '/cruds/create/'
        form_data = {
            'csrf_token': 'mock',
            'content': 'Hello World!'
        }

        # Assume
        self.assertTrue(admin.is_admin())

        # Act
        response = client.post(endpoint, data=form_data, follow_redirects=False)
        crud_id = extract_id_from_url(response.location)
        created_crud = Crud.read(crud_id)

        # Assert
        self.assertEqual(response.status_code, 302, response.data)
        self.assertEqual(redirect_path(response), '/cruds/%s/' % (crud_id))
        self.assertIsNotNone(created_crud)
        self.assertEqual(created_crud.content, form_data['content'])
        self.assertEqual(created_crud.creator.unique_id, admin.unique_id)

    def test_expects_non_admin_user_to_not_create_crud(self):
        # Arrange
        client = cruds_controller.test_client()
        guest = MockIdentityService.login_app_engine_user(self)
        endpoint = '/cruds/create/'
        form_data = {
            'csrf_token': 'mock',
            'content': 'Hello World!'
        }

        # Assume
        self.assertFalse(guest.is_admin())

        # Act
        response = client.post(endpoint, data=form_data, follow_redirects=False)
        html = parse_html(response.data)

        # Assert
        self.assertEqual(response.status_code, 403, response.data)
        self.assertEqual(html.h2.text, 'Permission Required')

    def test_expects_unauthenticated_user_to_be_denied_new_view(self):
        pass

    def test_expects_authenticated_user_to_access_new_view(self):
        pass
