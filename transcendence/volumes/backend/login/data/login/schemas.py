from ninja import Schema

class User(Schema):

    login: str
    email: str
    password: str