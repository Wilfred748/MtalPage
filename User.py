from werkzeug.security import check_password_hash
from flask_login import UserMixin, AnonymousUserMixin


class User(UserMixin):

    def __init__(self, id, email, password, role, name="", ) -> None:
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.role = role

    @classmethod
    def check_password(cls, hashed_password, password):
        return check_password_hash(hashed_password, password)
    
class AnonymousUser(AnonymousUserMixin):
  def __init__(self, name, id):
    self.name = name
    self.id = id
