from models.recipe import RecipeModel
from models.user import UserModel
from models.users_favourite_recipes import FavouriteRecipesModel
from tests.base_test import BaseTest, URL
import json
from datetime import datetime


class TestUserStats(BaseTest):
    def test_get_user_stats_not_admin(self):
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

                response = client.get(f"{URL}/users_stats",
                                      headers={
                                          "Content-Type": "application/json",
                                          "Authorization": f"Bearer {access_token}"
                                      }
                                      )

                expected = {"message": "Admin permission required!"}

                self.assertDictEqual(json.loads(response.data), expected,
                                     "The return value is wrong when non-admin tries to get users stats.")
                self.assertEqual(response.status_code, 403,
                                 "Status code is wrong when non-admin tries to get users stats.")

    def test_get_users_stats_admin(self):
        with self.app_context():
            with self.app() as client:
                UserModel("TestAdmin", "TestPwd1!", admin=1).save_to_db()
                UserModel("TestUsername", "TestPwd1!").save_to_db()
                UserModel("TestUsername2", "TestPwd1!").save_to_db()
                UserModel("TestUsername3", "TestPwd1!").save_to_db()
                UserModel("TestUsername4", "TestPwd1!").save_to_db()

                current_time = datetime.utcnow()

                recipe_id1, _ = RecipeModel("Title1", "Url1", "Ingredients1, test1").save_to_db()
                recipe_id2, _ = RecipeModel("Title2", "Url2", "Ingredients2, test2").save_to_db()
                recipe_id3, _ = RecipeModel("Title3", "Url3", "Ingredients3, test3").save_to_db()
                FavouriteRecipesModel(2, recipe_id1, current_time,
                                      "Meat", "The most delicious ever!").save_to_db()
                FavouriteRecipesModel(2, recipe_id2, current_time,
                                      "Meat", "The most delicious ever!").save_to_db()
                FavouriteRecipesModel(2, recipe_id3, current_time,
                                      "Meat", "The most delicious ever!").save_to_db()

                FavouriteRecipesModel(3, recipe_id1, current_time).save_to_db()
                FavouriteRecipesModel(3, recipe_id2, current_time).save_to_db()
                FavouriteRecipesModel(3, recipe_id3, current_time).save_to_db()
                FavouriteRecipesModel(4, recipe_id1, current_time).save_to_db()
                FavouriteRecipesModel(4, recipe_id2, current_time).save_to_db()

                response = client.post(f"{URL}/login",
                                       data=json.dumps({
                                           "username": "TestAdmin",
                                           "password": "TestPwd1!"
                                       }),
                                       headers={
                                           "Content-Type": "application/json"
                                       }
                                       )
                access_token = json.loads(response.data)['access_token']

                response = client.get(f"{URL}/users_stats",
                                      headers={
                                          "Content-Type": "application/json",
                                          "Authorization": f"Bearer {access_token}"
                                      }
                                      )

                expected = {
                    "number_of_users_in_db": 5,
                    "users_details": [
                        {
                            "admin": 1,
                            "user_id": 1,
                            "username": "TestAdmin",
                            "number_of_favourite_recipes_saved": 0,
                            "ids_of_favourite_recipes": []
                        },
                        {
                            "admin": 0,
                            "user_id": 2,
                            "username": "TestUsername",
                            "number_of_favourite_recipes_saved": 3,
                            "ids_of_favourite_recipes": [1, 2, 3]
                        },
                        {
                            "admin": 0,
                            "user_id": 3,
                            "username": "TestUsername2",
                            "number_of_favourite_recipes_saved": 3,
                            "ids_of_favourite_recipes": [1, 2, 3]
                        },
                        {
                            "admin": 0,
                            "user_id": 4,
                            "username": "TestUsername3",
                            "number_of_favourite_recipes_saved": 2,
                            "ids_of_favourite_recipes": [1, 2]
                        },
                        {
                            "admin": 0,
                            "user_id": 5,
                            "username": "TestUsername4",
                            "number_of_favourite_recipes_saved": 0,
                            "ids_of_favourite_recipes": []
                        }
                    ]
                }

                self.maxDiff = None
                self.assertDictEqual(json.loads(response.data), expected,
                                     "The /users_stats GET returns wrong response.")