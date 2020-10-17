from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.recipe import RecipeModel


class Recipe(Resource):
    @jwt_required
    def post(self):
        data_parser = reqparse.RequestParser()
        data_parser.add_argument("title",
                                 required=True,
                                 type=str,
                                 help="Please add recipe's title")
        data_parser.add_argument("href",
                                 required=True,
                                 type=str,
                                 help="Please add recipe's url")
        data_parser.add_argument("ingredients",
                                 required=True,
                                 type=str,
                                 help="Please add recipe's ingredients")
        data_parser.add_argument("category",
                                 required=False,
                                 type=str,
                                 help="You can categorize this recipe")
        data_parser.add_argument("comment",
                                 required=False,
                                 type=str,
                                 help="You can add a comment to this recipe")

        data = data_parser.parse_args()

        favourite_recipe = RecipeModel(**data)
        favourite_recipe.save_to_db()

        return favourite_recipe.json()


class FavouriteRecipe(Resource):
    @jwt_required
    def get(self, recipe_id):
        f_recipe = RecipeModel.find_by_recipe_id(recipe_id)
        if not f_recipe:
            return {"message": "Sorry, I couldn't find this recipe."}, 400

        return f_recipe.json()





