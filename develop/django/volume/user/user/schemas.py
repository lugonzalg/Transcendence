from ninja import Schema, ModelSchema
from . import models

class UserProfile(Schema):

    username: str
    email: str
    bio: str

class ReturnUserProfile(ModelSchema):

    class Meta:

        model = models.user_login
        fields = ['username', 'avatar']