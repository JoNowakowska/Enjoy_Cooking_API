import json
from datetime import datetime

from models.recipe import RecipeModel
from models.user import UserModel
from models.users_favourite_recipes import FavouriteRecipesModel
from tests.base_test import BaseTest, URL


class TestNewRecipes(BaseTest):
    def setUp(self) -> None:
        super(TestNewRecipes, self).setUp()
        with self.app_context():
            with self.app() as client:
                UserModel("TestUsername", "TestPwd1!").save_to_db()
                response = client.post(f"{URL}/login",
                                       data=json.dumps({
                                           "username": "TestUsername",
                                           "password": "TestPwd1!"
                                       }),
                                       headers={
                                           "Content-Type": "application/json"
                                       }
                                       )
                self.access_token = json.loads(response.data)['access_token']

    def test_post_by_ingredients_and_dish(self):
        with self.app_context():
            with self.app() as client:
                response = client.post(f"{URL}/new_recipes",
                                       data=json.dumps({
                                           "ingredients": "pork, onion",
                                           "dish": "chop"
                                       }),
                                       headers={
                                           "Content-Type": "application/json",
                                           "Authorization": f"Bearer {self.access_token}"

                                       }
                                       )

                self.assertEqual(response.status_code, 200,
                                 "Improper status code while requesting new recipes based on ingredients and a dish.")
                self.assertIn("Recipes with the ingredients of your choice (pork, onion)",
                              json.loads(response.data).keys(),
                              "Improper return message while requesting new recipes based on ingredients and a dish.")

    def test_post_by_ingredients_only(self):
        with self.app_context():
            with self.app() as client:
                response = client.post(f"{URL}/new_recipes",
                                       data=json.dumps({
                                           "ingredients": "pork, onion"
                                       }),
                                       headers={
                                           "Content-Type": "application/json",
                                           "Authorization": f"Bearer {self.access_token}"

                                       }
                                       )

                self.assertEqual(response.status_code, 200,
                                 "Improper status code while requesting new recipes based on ingredients only.")
                self.assertIn("Recipes with the ingredients of your choice (pork, onion)",
                              json.loads(response.data).keys(),
                              "Improper return message while requesting new recipes based on ingredients only.")


class TestFavouriteRecipes(BaseTest):
    def test_get_no_favourites(self):
        with self.app_context():
            with self.app() as client:
                UserModel("TestUsername", "TestPwd1!").save_to_db()
                response = client.post(f"{URL}/login",
                                       data=json.dumps({
                                           "username": "TestUsername",
                                           "password": "TestPwd1!"
                                       }),
                                       headers={
                                           "Content-Type": "application/json"
                                       }
                                       )

                access_token = json.loads(response.data)['access_token']

                response = client.get(f"{URL}/favourite_recipes",
                                      headers={
                                          "Content-Type": "application/json",
                                          "Authorization": f"Bearer {access_token}"
                                      })

                expected = {"Your favourite recipes: ": []}

                self.assertDictEqual(json.loads(response.data), expected,
                                     "Wrong response returned when getting user favourites recipes "
                                     "- which should be an empty list.")
                self.assertEqual(response.status_code, 200,
                                 "Wrong status code returned when getting user favourites recipes "
                                 "- which should be an empty list."
                                 )

    def test_get(self):
        with self.app_context():
            with self.app() as client:
                UserModel("TestUsername", "TestPwd1!").save_to_db()
                current_time = datetime.utcnow()

                recipe_id1, _ = RecipeModel("Title1", "Url1", "Ingredients1, test1").save_to_db()
                recipe_id2, _ = RecipeModel("Title2", "Url2", "Ingredients2, test2").save_to_db()
                recipe_id3, _ = RecipeModel("Title3", "Url3", "Ingredients3, test3").save_to_db()
                FavouriteRecipesModel(1, recipe_id1, current_time,
                                      "Test category - salad", "Test comment - for Friday's dinner").save_to_db()
                FavouriteRecipesModel(1, recipe_id2, current_time,
                                      "Test category - snack", "Test comment - for Sunday's break.").save_to_db()
                FavouriteRecipesModel(1, recipe_id3, current_time
                                      ).save_to_db()

                response = client.post(f"{URL}/login",
                                       data=json.dumps({
                                           "username": "TestUsername",
                                           "password": "TestPwd1!"
                                       }),
                                       headers={
                                           "Content-Type": "application/json"
                                       }
                                       )

                access_token = json.loads(response.data)['access_token']

                response = client.get(f"{URL}/favourite_recipes",
                                      headers={
                                          "Content-Type": "application/json",
                                          "Authorization": f"Bearer {access_token}"
                                      })

                expected = {"Your favourite recipes: ":
                    [
                        {"recipe_id": 1,
                         "save_date": datetime.strftime(current_time, "%Y-%m-%d %H:%M"),
                         "category": "Test category - salad",
                         "comment": "Test comment - for Friday's dinner",
                         "recipe_title": "Title1",
                         "recipe_link": "Url1",
                         "ingredients": "Ingredients1, test1"},
                        {"recipe_id": 2,
                         "save_date": datetime.strftime(current_time, "%Y-%m-%d %H:%M"),
                         "category": "Test category - snack",
                         "comment": "Test comment - for Sunday's break.",
                         "recipe_title": "Title2",
                         "recipe_link": "Url2",
                         "ingredients": "Ingredients2, test2"},
                        {"recipe_id": 3,
                         "save_date": datetime.strftime(current_time, "%Y-%m-%d %H:%M"),
                         "category": None,
                         "comment": None,
                         "recipe_title": "Title3",
                         "recipe_link": "Url3",
                         "ingredients": "Ingredients3, test3"}
                    ]
                }

                self.maxDiff = None
                self.assertDictEqual(json.loads(response.data), expected,
                                     "Wrong response returned when getting user favourites recipes "
                                     "- which should be a list of 3 favourites.")
                self.assertEqual(response.status_code, 200,
                                 "Wrong status code returned when getting user favourites recipes "
                                 "- which should be a list of 3 favourites.")


class TestRecipesStats(BaseTest):
    def test_get_not_admin(self):
        with self.app_context():
            with self.app() as client:
                UserModel("TestUsername", "TestPwd1!").save_to_db()
                response = client.post(f"{URL}/login",
                                       data=json.dumps({
                                           "username": "TestUsername",
                                           "password": "TestPwd1!"
                                       }),
                                       headers={
                                           "Content-Type": "application/json"
                                       }
                                       )

                access_token = json.loads(response.data)['access_token']

                response = client.get(f"{URL}/recipes_stats",
                                      headers={
                                          "Content-Type": "application/json",
                                          "Authorization": f"Bearer {access_token}"
                                      }
                                      )

                expected = {"message": "Admin privileges required"}

                self.assertDictEqual(json.loads(response.data), expected)
                self.assertEqual(response.status_code, 403)

    def test_get_admin(self):
        with self.app_context():
            with self.app() as client:
                UserModel("User1", "Pwd1!").save_to_db()
                UserModel("User2", "Pwd1!").save_to_db()
                UserModel("User3", "Pwd1!").save_to_db()
                UserModel("User4", "Pwd1!").save_to_db()

                current_time = datetime.utcnow()

                recipe_id1, _ = RecipeModel("Title1", "Url1", "Ingredients1, test1").save_to_db()
                recipe_id2, _ = RecipeModel("Title2", "Url2", "Ingredients2, test2").save_to_db()
                recipe_id3, _ = RecipeModel("Title3", "Url3", "Ingredients3, test3").save_to_db()
                FavouriteRecipesModel(2, recipe_id1, current_time,
                                      "Test category - salad", "Test comment - for Friday's dinner").save_to_db()
                FavouriteRecipesModel(2, recipe_id2, current_time,
                                      "Test category - salad", "Test comment - for Friday's dinner").save_to_db()
                FavouriteRecipesModel(2, recipe_id3, current_time,
                                      "Test category - salad", "Test comment - for Friday's dinner").save_to_db()

                FavouriteRecipesModel(3, recipe_id1, current_time).save_to_db()
                FavouriteRecipesModel(3, recipe_id2, current_time).save_to_db()
                FavouriteRecipesModel(3, recipe_id3, current_time).save_to_db()
                FavouriteRecipesModel(4, recipe_id1, current_time).save_to_db()
                FavouriteRecipesModel(4, recipe_id2, current_time).save_to_db()

                UserModel("TestUsername", "TestPwd1!", admin=1).save_to_db()
                response = client.post(f"{URL}/login",
                                       data=json.dumps({
                                           "username": "TestUsername",
                                           "password": "TestPwd1!"
                                       }),
                                       headers={
                                           "Content-Type": "application/json"
                                       }
                                       )

                access_token = json.loads(response.data)['access_token']

                response = client.get(f"{URL}/recipes_stats",
                                      headers={
                                          "Content-Type": "application/json",
                                          "Authorization": f"Bearer {access_token}"
                                      }
                                      )

                expected = {"a number of recipes saved into the table 'recipes'": 3,
                            'details of the recipes and a number of people who saved each of them as their favourites':
                                [
                                    {'recipe':
                                        {
                                            'recipe_id': 1,
                                            'recipe_title': 'Title1',
                                            'recipe_link': 'Url1',
                                            'recipe_ingredients': 'Ingredients1, test1'
                                        },
                                        'number_of_users_who_have_it_saved_to_favourites': 3,
                                        'ids_of_users_who_saved_it_to_favourites': [2, 3, 4]
                                    },
                                    {'recipe':
                                        {
                                            'recipe_id': 2,
                                            'recipe_title': 'Title2',
                                            'recipe_link': 'Url2',
                                            'recipe_ingredients': 'Ingredients2, test2'
                                        },
                                        'number_of_users_who_have_it_saved_to_favourites': 3,
                                        'ids_of_users_who_saved_it_to_favourites': [2, 3, 4]
                                    },
                                    {'recipe':
                                        {
                                            'recipe_id': 3,
                                            'recipe_title': 'Title3',
                                            'recipe_link': 'Url3',
                                            'recipe_ingredients': 'Ingredients3, test3'
                                        },
                                        'number_of_users_who_have_it_saved_to_favourites': 2,
                                        'ids_of_users_who_saved_it_to_favourites': [2, 3]
                                    }
                                ]
                            }

                self.assertDictEqual(json.loads(response.data), expected)
                self.assertEqual(response.status_code, 200)
