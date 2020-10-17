from db import db


class RecipeModel(db.Model):
    __tablename__ = 'recipes'

    recipe_id = db.Column(db.Integer(), primary_key=True)
    recipe_title = db.Column(db.String(200))
    recipe_link = db.Column(db.String())
    recipe_ingredients = db.Column(db.String())
    category = db.Column(db.String(80))
    comment = db.Column(db.String(180))

    favourite_recipes = db.relationship("FavouriteRecipesModel")

    def __init__(self, title, href, ingredients, category=None, comment=None):
        self.recipe_title = title
        self.recipe_link = href
        self.recipe_ingredients = ingredients
        self.category = category
        self.comment = comment

    def json(self):
        return {"recipe_id": self.recipe_id,
                "recipe_title": self.recipe_title,
                "recipe_link": self.recipe_link,
                "recipe_ingredients": self.recipe_ingredients,
                "category": self.category,
                "comment": self.comment}

    @classmethod
    def find_by_recipe_id(cls, recipe_id):
        return cls.query.filter_by(recipe_id=recipe_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

