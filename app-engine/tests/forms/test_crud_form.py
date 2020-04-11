"""
# Crud Form Tests

To run individually:

    nosetests -c nose.cfg tests/forms/test_crud_form.py
"""
from google.appengine.ext import db
from google.appengine.api import users
from flask_wtf import FlaskForm

from models.guest import Guest
from models.crud import Crud
from forms.crud import CrudForm

from tests.helper import (AppEngineTestCase, MockIdentityService)


#
# Test Case
#
class CrudFormTest(AppEngineTestCase):
    #
    # Class Tests
    #
    def test_expects_instance_of_crud_form(self):
        # Arrange
        app = self.initApp()

        # Act
        with app.app_context():
            form = CrudForm()

        # Assert
        self.assertIsInstance(form, FlaskForm)
        self.assertIsInstance(form, CrudForm)
