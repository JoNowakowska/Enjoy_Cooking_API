from flask_restful import Resource, reqparse
import requests
from external_api_key import EXTERNAL_API_KEY

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
    def post(self):
        users_data = request_parser.parse_args()

        if users_data['dish']:
            dish = f"&q={users_data['dish']}"

        ingredients = '&i=' + users_data['ingredients'].replace(", ", '%2C')

        page_no = '?p=1'

        print(ingredients)

        url = "https://recipe-puppy.p.rapidapi.com/"

        final_endpoint = url + page_no + ingredients + dish

        headers = {
            'x-rapidapi-host': "recipe-puppy.p.rapidapi.com",
            'x-rapidapi-key': EXTERNAL_API_KEY
        }

        response = requests.get(final_endpoint, headers=headers)

        res = response.json()

        list_of_results = res['results']
        n = 1
        for result in list_of_results:
            print(f'''{n} - {result['title']}
            Ingredients: {result['ingredients']},
            Link to the recipe: {result['href']}
            ''')
            n += 1