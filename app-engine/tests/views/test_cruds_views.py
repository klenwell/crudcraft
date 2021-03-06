"""
# Cruds View Test

To run individually:

    nosetests -c nose.cfg tests/controllers/test_cruds_controller.py
"""
from google.appengine.api import users

from controllers.cruds import app as cruds_controller
from models.crud import Crud

from tests.helper import (AppEngineControllerTest, parse_html, MockIdentityService,
                          extract_id_from_url)
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

    def test_expects_index_table_row_will_link_to_detailed_view(self):
        # Arrange
        # TODO: Put this in a factory or method.
        MockIdentityService.stub_app_engine_user(self, email='user@gmail.com')
        app_engine_user = users.get_current_user()
        creator = Guest.app_engine_user(app_engine_user)
        crud = Crud.create(creator, 'This is a crud test.')

        client = cruds_controller.test_client()
        guest = MockIdentityService.unauthenticated_guest(self)
        endpoint = '/cruds/'
        table_rows_selector = 'table.cruds tr.clickable'
        url_attr = 'data-href'

        # Assume
        self.assertFalse(guest.is_authenticated())

        # Act
        response = client.get(endpoint, follow_redirects=False)
        html = parse_html(response.data)
        table_rows = html.select(table_rows_selector) if html else []
        first_row = table_rows[0] if len(table_rows) > 0 else None
        crud_url = first_row.attrs.get(url_attr) if first_row else None
        crud_id = extract_id_from_url(crud_url)

        # Assert
        self.assertEqual(response.status_code, 200, html)
        self.assertIsNotNone(first_row, html)
        self.assertIsNotNone(crud_url)
        self.assertEqual(crud_id, crud.public_id)
