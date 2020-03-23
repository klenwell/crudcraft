"""
# Crud Model
A crud is a simple record that can be created, read, updated, and (soft-)deleted.

## Related Models
- belongs_to guest
- belongs_to crud
- has_many cruds
- has_many crud_ops

"""
from google.appengine.ext import ndb


#
# Model
#
class Crud(ndb.Model):
    #
    # Attrs
    #
    # Fields
    message = ndb.StringProperty(required=True)
    read_count = ndb.IntegerProperty(default=0)
    edit_count = ndb.IntegerProperty(default=0)
    delete_count = ndb.IntegerProperty(default=0)

    # References
    creator_key = ndb.KeyProperty(required=True)    # kind=Guest
    parent_key = ndb.KeyProperty(required=True)    # kind=Crud
    child_keys = ndb.KeyProperty(repeated=True)    # kind=Crud

    # Timestamps
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    updated_at = ndb.DateTimeProperty(auto_now=True)

    #
    # Virtual Attrs
    #
    @property
    def public_id(self):
        if not self.key:
            return None
        else:
            return self.key.id()

    #
    # Relationships
    #
    @property
    def creator(self):
        if not self.creator_key:
            return None
        else:
            return self.creator_key.get()

    @property
    def parent(self):
        if not self.parent_key:
            return None
        else:
            return self.parent_key.get()

    #
    # Class Methods
    #
    # CRUD Methods
    @staticmethod
    def create(creator, message):
        crud = Crud(creator_key=creator.key,
                    message=message)
        crud.put()
        return crud

    @staticmethod
    def read(public_id):
        return Crud.get_by_public_id(public_id)
