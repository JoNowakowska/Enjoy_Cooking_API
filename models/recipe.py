from db import db


class Recipe(db.Model):
    __tablename__ = 'recipes'

    recipe_id = db.Column(db.Integer(), primary_key=True)
    recipe_title = db.Column(db.String(200))
    recipe_link = db.Column(db.String())
    recipe_ingredients = db.Column(db.String())

    def __init__(self, title, href, ingredients):
        self.recipe_title = title
        self.recipe_link = href
        self.recipe_ingredients = ingredients

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

