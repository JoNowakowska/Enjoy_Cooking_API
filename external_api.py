import requests
from external_api_key import EXTERNAL_API_KEY

users_ingredients_list = []

dish = input("Please enter a dish you want to make or leave it blank if you have no idea: ")

if dish:
    dish = f"&q={dish}"

next_ingredient = input("Please enter an ingredient you want to use to make your dish or leave this field empty if there are no more ingredients you want to use and then press Enter: ")

while next_ingredient:
    users_ingredients_list.append(next_ingredient)
    next_ingredient = input(
        "Please enter an ingredient or leave this field empty if there are no more ingredients you want to use and then press Enter: ")

users_ingredients_string = '&i='+'%2C'.join(users_ingredients_list)

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

print(res)
