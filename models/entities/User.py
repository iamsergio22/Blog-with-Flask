from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, id, nombre, password1) -> None:
        self.id = id
        self.username = nombre
        self.password = password1

    @classmethod
    def check_password(self, hashed_password,password):
        return check_password_hash(hashed_password,password) 