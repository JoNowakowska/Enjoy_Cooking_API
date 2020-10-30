from db import db
from models.recipe import RecipeModel
from datetime import datetime


class FavouriteRecipesModel(db.Model):
    __tablename__ = "favourite_recipes"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'))
    recipe_id = db.Column(db.Integer(), db.ForeignKey('recipes.recipe_id'))
    save_date = db.Column(db.DateTime())
    category = db.Column(db.String(80), default=None)
    comment = db.Column(db.String(180), default=None)

    users = db.relationship("UserModel")
    recipes = db.relationship("RecipeModel")

    foreign_keys = ['users.user_id', 'recipes.recipe_id']

    def __init__(self, user_id, recipe_id, save_date, category=None, comment=None):
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.save_date = save_date
        self.category = category
        self.comment = comment

    def json(self):
        return {"recipe_id": self.recipe_id,
                "save_date": datetime.strftime(self.save_date, "%Y-%m-%d %H:%M"),
                "category": self.category,
                "comment": self.comment
                }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_recipe_id_user_id(cls, recipe_id, user_id):
        return cls.query.filter_by(recipe_id=recipe_id).filter_by(user_id=user_id).first()

    @classmethod
    def find_by_recipe_id(cls, recipe_id):
        return cls.query.filter_by(recipe_id=recipe_id).all()

    @classmethod
    def show_mine(cls, user_id):
        return db.session.query(FavouriteRecipesModel, RecipeModel)\
                .join(FavouriteRecipesModel, RecipeModel.recipe_id == FavouriteRecipesModel.recipe_id)\
                .filter_by(user_id=user_id)\
                .all()

    @classmethod
    def show_my_recipe_ids(cls, user_id):  # -> list of tuples, e.g. [(3,), (4,)]
        return db.session.query(FavouriteRecipesModel.recipe_id).filter_by(user_id=user_id).all()

    @classmethod
    def show_all(cls):
        return cls.query.all()

