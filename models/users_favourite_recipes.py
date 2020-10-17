from db import db


class FavouriteRecipesModel(db.Model):
    __tablename__ = "favourite_recipes"
    user_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'), primary_key=True)
    recipe_id = db.Column(db.Integer(), db.ForeignKey('recipes.recipe_id'))

    users = db.relationship("UserModel")
    recipes = db.relationship("RecipeModel")

