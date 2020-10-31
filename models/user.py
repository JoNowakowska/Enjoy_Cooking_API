from db import db
from models.users_favourite_recipes import FavouriteRecipesModel


class UserModel(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(100))
    admin = db.Column(db.Integer())

    recipes = db.relationship("RecipeModel", secondary="favourite_recipes")

    def __init__(self, username, password, admin=0):
        self.username = username
        self.password = password
        self.admin = admin

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        user = cls.query.filter_by(username=username).first()
        return user

    @classmethod
    def find_by_id(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        return user

    @classmethod
    def count_all(cls):
        return db.session.query(db.func.count(UserModel.user_id)).first()

    @classmethod
    def show_all(cls):
        return db.session.query(UserModel, db.func.count(FavouriteRecipesModel.recipe_id)) \
            .join(FavouriteRecipesModel, UserModel.user_id == FavouriteRecipesModel.user_id, isouter=True) \
            .group_by(UserModel.user_id) \
            .order_by(UserModel.admin.desc()).all()
