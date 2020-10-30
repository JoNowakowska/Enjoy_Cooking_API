from flask_restful import Resource, reqparse
import requests
from external_api_key import EXTERNAL_API_KEY
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from datetime import datetime

from models.recipe import RecipeModel
from models.users_favourite_recipes import FavouriteRecipesModel


request_parser = reqparse.RequestParser()
request_parser.add_argument('ingredients',
                            required=True,
                            type=str,
                            help="""Enter ingredients you want to use to prepare your dish 
                            as a comma separated values.
                            This field cannot be left blank""")
request_parser.add_argument('dish',
                            required=False,
                            type=str,
                            help="""Enter a dish you have in mind.""")


class Recipes(Resource):
    @jwt_required
    def post(self):
        users_data = request_parser.parse_args()

        if users_data['dish']:
            dish = f"&q={users_data['dish']}"
        else:
            dish = ''

        ingredients = '&i=' + users_data['ingredients'].replace(", ", '%2C')

        page_no = '?p=1'

        url = "https://recipe-puppy.p.rapidapi.com/"

        final_endpoint = url + page_no + ingredients + dish

        headers = {
            'x-rapidapi-host': "recipe-puppy.p.rapidapi.com",
            'x-rapidapi-key': EXTERNAL_API_KEY
        }

        response = requests.get(final_endpoint, headers=headers)

        res = response.json()

        list_of_results = res['results']

        return {f'''Recipes with the ingredients of your choice ({users_data['ingredients']})''': list_of_results}

    def get(self):
        all_recipes = RecipeModel.show_all()
        all_list = [a.json() for a in all_recipes]
        return {"all recipes": all_list}


class FavouriteRecipes(Resource):
    @jwt_required
    def get(self):
        current_user_id = get_jwt_identity()
        user_favourite_recipes = FavouriteRecipesModel.show_mine(current_user_id)
        user_favourite_recipes_display = [{"recipe_id": x[0].recipe_id,
                                           "save_date": datetime.strftime(x[0].save_date, "%Y-%m-%d %H:%M"),
                                           "category": x[0].category,
                                           "comment": x[0].comment,
                                           "recipe_title": x[1].recipe_title,
                                           "recipe_link": x[1].href,
                                           "ingredients": x[1].recipe_ingredients}
                                          for x in user_favourite_recipes]

        return {"Your favourite recipes: ": user_favourite_recipes_display}


class RecipesStats(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        if not claims["admin"]:
            return {"message": "Admin privileges required"}
        recipes_stats = FavouriteRecipesModel.count_users_by_recipe_id()
        recipes_stats_display = [{"recipe": r.json(), "number_of_users_who_saved_it_to_favourites": n} for r, n in recipes_stats]
        print(recipes_stats)
        return {"all recipes saved to the db - table 'recipes'": recipes_stats_display}

