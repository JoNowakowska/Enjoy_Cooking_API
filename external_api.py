import requests
from external_api_key import EXTERNAL_API_KEY
from models.recipe import Recipe

users_ingredients_list = []

dish = input("Please enter a dish you want to make or leave it blank if you have no idea: ")

if dish:
    dish = f"&q={dish}"

next_ingredient = input(
    "Please enter an ingredient you want to use to make your dish or leave this field empty if there are no more ingredients you want to use and then press Enter: ")

while next_ingredient:
    users_ingredients_list.append(next_ingredient)
    next_ingredient = input(
        "Please enter an ingredient or leave this field empty if there are no more ingredients you want to use and then press Enter: ")

users_ingredients_string = '&i=' + '%2C'.join(users_ingredients_list)

page_no = '?p=1'

url = "https://recipe-puppy.p.rapidapi.com/"

final_endpoint = url + page_no + users_ingredients_string + dish

print(final_endpoint)

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

recipe_to_save_to_db = input("Please enter the id of an recipe you want to save for your further reference and press enter OR simply press enter if you don't want to save any: ")

if recipe_to_save_to_db:
    new_to_save_recipe = list_of_results[int(recipe_to_save_to_db)-1]
    print(new_to_save_recipe)
    recipe = Recipe(new_to_save_recipe['title'], new_to_save_recipe['href'], new_to_save_recipe['ingredients'])
    recipe.save_to_db()


