import re

from werkzeug.security import check_password_hash, generate_password_hash

from .. import db
from sqlalchemy.orm import validates, relationship


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    articles = relationship("Article", backref="user")

    @validates("password")
    def validate_password(self, key, password):
        length_error = len(password) < 8
        digit_error = re.search(r"\d", password) is None
        uppercase_error = re.search(r"[A-Z]", password) is None
        lowercase_error = re.search(r"[a-z]", password) is None

        password_ok = not (length_error or digit_error or uppercase_error or lowercase_error)
        if not password_ok:
            raise ValueError("Password have to be minimal 8 characters lengths, "
                             "contain at least one lowercase and uppercase symbol")
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role_id": self.role_id
        }


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)  # Admin | Editor | Viewer
    users = relationship("User", backref="role")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
