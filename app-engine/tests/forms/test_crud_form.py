"""
# Crud Form Tests

To run individually:

    nosetests -c nose.cfg tests/forms/test_crud_form.py
"""
from werkzeug.datastructures import ImmutableMultiDict
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

    def test_expects_form_to_validate(self):
        # Arrange
        app = self.initApp()
        content = u'test content'
        request_form = ImmutableMultiDict([('content', content)])

        # Assume
        self.assertEqual(request_form['content'], content)

        # Act
        with app.app_context():
            form = CrudForm(request_form)
            form_is_valid = form.validate()

        # Assert
        self.assertTrue(form_is_valid)
        self.assertEqual(form.content.data, content)

    def test_expects_form_not_to_validate(self):
        # Arrange
        app = self.initApp()
        content = u''
        request_form = ImmutableMultiDict([('content', content)])

        # Assume
        self.assertEqual(request_form['content'], content)

        # Act
        with app.app_context():
            form = CrudForm(request_form)
            form_is_valid = form.validate()

        # Assert
        self.assertFalse(form_is_valid)
        self.assertEqual(form.content.data, content)

    def test_expects_to_scrub_content_field(self):
        # Arrange
        app = self.initApp()
        content = '<strong>bold</strong> <script>alert("scripted!")</script> content'
        request_form = ImmutableMultiDict([('content', content)])

        # Assume
        self.assertEqual(request_form['content'], content)

        # Act
        with app.app_context():
            form = CrudForm(request_form)
            form_is_valid = form.validate()

        # Assert
        self.assertTrue(form_is_valid)
        self.assertEqual(form.content.data, 'bold alert("scripted!") content')

    def test_expects_to_preset_form(self):
        # Arrange
        app = self.initApp()
        email = 'user@gmail.com'
        MockIdentityService.stub_app_engine_user(self, email=email)
        app_engine_user = users.get_current_user()
        creator = Guest.app_engine_user(app_engine_user)
        content = 'This is a crud test.'
        crud = Crud.create(creator, content)

        # Assume
        self.assertEqual(crud.creator.email, email)
        self.assertIsNotNone(crud.public_id)

        # Act
        with app.app_context():
            form = CrudForm()
            form.preset(crud)
            form_is_valid = form.validate()

        # Assert
        self.assertTrue(form_is_valid)
        self.assertEqual(form.public_id.data, crud.public_id)
        self.assertEqual(form.content.data, content)
