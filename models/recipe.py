from db import db


class RecipeModel(db.Model):
    __tablename__ = 'recipes'

    recipe_id = db.Column(db.Integer(), primary_key=True)
    recipe_title = db.Column(db.String(200))
    href = db.Column(db.String())
    recipe_ingredients = db.Column(db.String())

    users = db.relationship("UserModel", secondary="favourite_recipes")

    def __init__(self, title, href, ingredients):
        self.recipe_title = title
        self.href = href
        self.recipe_ingredients = ingredients

    def json(self):
        return {"recipe_id": self.recipe_id,
                "recipe_title": self.recipe_title,
                "recipe_link": self.href,
                "recipe_ingredients": self.recipe_ingredients,
                }

    @classmethod
    def find_by_recipe_id(cls, recipe_id):
        return cls.query.filter_by(recipe_id=recipe_id).first()

    @classmethod
    def find_by_href(cls, href):
        return cls.query.filter_by(href=href).first()

    def save_to_db(self):
        existing_recipe = self.find_by_href(self.href)
        if existing_recipe:
            recipe_id = existing_recipe.recipe_id
            return recipe_id, existing_recipe
        db.session.add(self)
        db.session.commit()
        return self.recipe_id, self

    @classmethod
    def delete_from_db(cls, recipe_id):
        recipe = RecipeModel.find_by_recipe_id(recipe_id)
        db.session.delete(recipe)
        db.session.commit()

    @classmethod
    def show_all(cls):
        return cls.query.all()