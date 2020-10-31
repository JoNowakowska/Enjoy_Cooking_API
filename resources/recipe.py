from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_raw_jwt, get_jwt_identity
from models.recipe import RecipeModel
from models.users_favourite_recipes import FavouriteRecipesModel
from datetime import datetime


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
        current_time = datetime.utcnow()
        recipe_obj = RecipeModel.find_by_href(data['href'])
        if recipe_obj:
            recipe_id = recipe_obj.recipe_id
        else:
            recipe_id, recipe_obj = RecipeModel(data['title'], data['href'], data['ingredients']).save_to_db()

        if FavouriteRecipesModel.find_by_recipe_id_user_id(recipe_id, user_id):
            return {"message":
                        "You have already this recipe saved in your favourites. "
                        "If you want to update it, use the update endpoint."}, 400

        favourite = FavouriteRecipesModel(user_id, recipe_id, current_time, data['category'], data['comment'])
        favourite.save_to_db()

        just_saved_recipe_display = {"recipe_id": favourite.recipe_id,
                                     "save_date": datetime.strftime(favourite.save_date, "%Y-%m-%d %H:%M"),
                                     "category": favourite.category,
                                     "comment": favourite.comment,
                                     "recipe_title": recipe_obj.recipe_title,
                                     "recipe_link": recipe_obj.href,
                                     "ingredients": recipe_obj.recipe_ingredients}

        return {'message': "Successfully saved",
                "saved_recipe": just_saved_recipe_display}, 201


class FavouriteRecipe(Resource):
    @jwt_required
    def get(self, recipe_id):
        recipe_obj = RecipeModel.find_by_recipe_id(recipe_id)
        if recipe_obj:
            user_id = get_jwt_identity()
            favourite = FavouriteRecipesModel.find_by_recipe_id_user_id(recipe_id, user_id)
            if favourite:
                recipe_to_display = {"recipe_id": favourite.recipe_id,
                                     "save_date": datetime.strftime(favourite.save_date, "%Y-%m-%d %H:%M"),
                                     "category": favourite.category,
                                     "comment": favourite.comment,
                                     "recipe_title": recipe_obj.recipe_title,
                                     "recipe_link": recipe_obj.href,
                                     "ingredients": recipe_obj.recipe_ingredients
                                     }
                return {"Recipe": recipe_to_display}, 200
        return {'message': "Sorry, I couldn't find this recipe in your favourites."}, 404

    @fresh_jwt_required
    def put(self, recipe_id):
        parser = reqparse.RequestParser()
        parser.add_argument("category",
                            required=False,
                            type=str)
        parser.add_argument("comment",
                            required=False,
                            type=str)
        data = parser.parse_args()
        user_id = get_jwt_identity()
        favourite = FavouriteRecipesModel.find_by_recipe_id_user_id(recipe_id, user_id)
        if not favourite:
            return {"message": "Sorry, I couldn't find this recipe among your favourites."}, 404
        favourite.update_to_db(data)
        return {"Recipe updated!": favourite.json()}, 201

    @fresh_jwt_required
    def delete(self, recipe_id):
        user_id = get_jwt_identity()
        recipe = FavouriteRecipesModel.find_by_recipe_id_user_id(recipe_id, user_id)
        if not recipe:
            return {"message": "I couldn't find this recipe in your favourites."}, 404
        recipe.delete_from_db()
        if not FavouriteRecipesModel.find_by_recipe_id(recipe_id):
            RecipeModel.delete_from_db(recipe_id)

        return {"message": f"Recipe with the id {recipe_id} removed successfully from your favourites!"}, 200
