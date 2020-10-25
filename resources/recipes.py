from flask_restful import Resource, reqparse
import requests
from external_api_key import EXTERNAL_API_KEY
from flask_jwt_extended import jwt_required, get_jwt_identity

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

    # tą całą metodę dać do nowego endpointu /favourite_recipes no wiec tez do nowej metody
    '''
    @jwt_required
    def get(self):
        # Zamiast ok musi zwracac jakoś ładnie RecipeModel wraz z dodatkowymi rzeczami z FavouriteRecipesModel
        # Zrobic taka metode jak mowie powyzej i uzyc jej tez w przypadku w resource.Recipe post - w ost return
        current_user_id = get_jwt_identity()
        user_favourite_recipes = FavouriteRecipesModel.show_mine(current_user_id)
        for x in user_favourite_recipes:
            print(x[0].json(), x[1].json(), '\n\n'
                  )
        return {"Your favourite recipes: ": 'ok'}'''

    def get(self):
        all_recipes = RecipeModel.show_all()
        all_list = [a.json() for a in all_recipes]
        return {"all recipes": all_list}
