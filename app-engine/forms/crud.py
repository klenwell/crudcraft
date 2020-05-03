"""
    Crud Forms
"""
from flask_wtf import FlaskForm
from wtforms import (StringField, HiddenField)
from wtforms.validators import Required, Length

from forms.filters import scrub


#
# Constants
#
MAX_CRUD_LENGTH = 256


#
# Forms
#
class CrudForm(FlaskForm):
    public_id = HiddenField('Required only for edit form.')
    content = StringField('Content',
                          validators=[Required(), Length(max=MAX_CRUD_LENGTH)],
                          filters=[scrub])

    def preset(self, crud):
        self.public_id.data = crud.public_id
        self.content.data = crud.content

    def validate_update(self):
        # Avoid recursion: http://flask.pocoo.org/snippets/64/
        validates = FlaskForm.validate(self)
        if not validates:
            return False

        if not self.public_id.data:
            self.public_id.errors.append('Crud ID not found.')
            return False

        return True
