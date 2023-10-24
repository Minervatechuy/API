from app import db
from app import ma
import bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, name, surname, email, password):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = self.set_password(bytes(password, 'UTF-8'))

    def set_password(self, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        return hashed

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    name = ma.auto_field()
    surname = ma.auto_field()
    email = ma.auto_field()
    password = ma.auto_field()

user_schema = UserSchema()

