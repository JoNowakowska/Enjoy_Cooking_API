from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_raw_jwt, get_jwt_identity
from models.recipe import RecipeModel
from models.users_favourite_recipes import FavouriteRecipesModel
import datetime


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

        user_id = get_raw_jwt()['identity']
        current_time = datetime.datetime.utcnow()
        recipe_already_existing_in_db = RecipeModel.find_by_href(data['href'])
        if recipe_already_existing_in_db:
            recipe_id = recipe_already_existing_in_db.recipe_id
        else:
            recipe_id = RecipeModel(data['title'], data['href'], data['ingredients']).save_to_db()

        if FavouriteRecipesModel.find_by_recipe_id_user_id(recipe_id, user_id):
            return {"message":
                    "You have already this recipe saved in your favourites. "
                    "If you want to update it, use the update endpoint."}

        favourite = FavouriteRecipesModel(user_id, recipe_id, data['category'], data['comment'], current_time)
        favourite.save_to_db()

        return {'message': "Successfully saved",
                "saved_recipe": favourite.json()}


class FavouriteRecipe(Resource):
    @jwt_required
    def get(self, recipe_id):
        f_recipe = RecipeModel.find_by_recipe_id(recipe_id)
        if not f_recipe:
            return {"message": "Sorry, I couldn't find this recipe."}, 400

        return f_recipe.json()

    @fresh_jwt_required
    def delete(self, recipe_id):
        user_id = get_jwt_identity()
        recipe = FavouriteRecipesModel.find_by_recipe_id_user_id(recipe_id, user_id)
        if not recipe:
            return {"message": "I couldn't find this recipe in your favourites."}, 400
        recipe.delete_from_db()
        if not FavouriteRecipesModel.find_by_recipe_id(recipe_id):
            RecipeModel.delete_from_db(recipe_id)

        return {"message": f"Recipe with the id {recipe_id} removed successfully from your favourites!"}, 200





