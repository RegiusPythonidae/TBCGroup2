from ext import db, app, login_manager

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.commit()


class Product(db.Model, BaseModel):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.ForeignKey("product_categories.id"))
    name = db.Column(db.String)
    price = db.Column(db.Float)
    img = db.Column(db.String)

    category = db.relationship("ProductCategory")


class ProductCategory(db.Model, BaseModel):

    __tablename__ = "product_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    products = db.relationship("Product")


class User(db.Model, BaseModel, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)

    def __init__(self, username, password, role="normal"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        new_user = User(username="admin", password="password123", role="admin")
        new_user.create()
