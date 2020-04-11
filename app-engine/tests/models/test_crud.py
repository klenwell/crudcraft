"""
# Crud Model Tests

To run individually:

    nosetests -c nose.cfg tests/models/test_crud.py
"""
from google.appengine.ext import db
from google.appengine.api import users

from models.guest import Guest
from models.crud import Crud

from tests.helper import (AppEngineModelTest, MockIdentityService)


#
# Test Case
#
class GuestModelTest(AppEngineModelTest):
    #
    # Class Tests
    #
    def test_expects_new_crud_to_require_message(self):
        # Arrange
        email = 'user@gmail.com'
        MockIdentityService.stub_app_engine_user(self, email=email)
        app_engine_user = users.get_current_user()
        creator = Guest.app_engine_user(app_engine_user)
        content = None

        # Act
        with self.assertRaises(db.BadValueError) as c:
            Crud.create(creator, content)

        # Assert
        self.assertEqual(str(c.exception), "Entity has uninitialized properties: content")

    def test_expects_new_crud_to_require_creator(self):
        # Arrange
        creator = None
        content = 'This is a crud test.'

        # Act
        with self.assertRaises(AttributeError) as c:
            Crud.create(creator, content)

        # Assert
        self.assertEqual(str(c.exception), "'NoneType' object has no attribute 'key'")

    def test_expects_to_create_new_crud(self):
        # Arrange
        email = 'user@gmail.com'
        MockIdentityService.stub_app_engine_user(self, email=email)
        app_engine_user = users.get_current_user()
        creator = Guest.app_engine_user(app_engine_user)
        content = 'This is a crud test.'

        # Assume
        self.assertEqual(creator.email, email)

        # Act
        crud = Crud.create(creator, content)

        # Assert
        self.assertEqual(crud.creator, creator)
        self.assertEqual(crud.content, content)
