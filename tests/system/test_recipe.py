import json
from datetime import datetime

from models.recipe import RecipeModel
from models.user import UserModel
from models.users_favourite_recipes import FavouriteRecipesModel
from tests.base_test import BaseTest, URL


class TestRecipeResource(BaseTest):
    def setUp(self) -> None:
        super(TestRecipeResource, self).setUp()
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
                self.current_time = datetime.utcnow()

    def test_post_as_favourite_completely_new_recipe_no_category_no_comment(self):
        with self.app_context():
            with self.app() as client:
                response = client.post(f"{URL}/favourite_recipe",
                                       data=json.dumps({
                                           "title": "Test title",
                                           "href": "Test url",
                                           "ingredients": "Test, ingredients"
                                       }),
                                       headers={
                                           "Content-Type": "application/json",
                                           "Authorization": f"Bearer {self.access_token}"
                                       })

        expected = {'message': "Successfully saved",
                    "saved_recipe": {
                        "recipe_id": 1,
                        "save_date": datetime.strftime(self.current_time, "%Y-%m-%d %H:%M"),
                        "category": None,
                        "comment": None,
                        "recipe_title": "Test title",
                        "recipe_link": "Test url",
                        "ingredients": "Test, ingredients"
                    }
                    }

        self.assertDictEqual(json.loads(response.data), expected,
                             "Message returned when successfully saving a favourite recipe "
                             "(and in a background a recipe in the recipes table) is incorrect.")
        self.assertEqual(response.status_code, 201,
                         "Status code returned when successfully saving a favourite recipe "
                         "(and in a background a recipe in the recipes table) is incorrect.")

    def test_post_as_favourite_recipe_already_existing_in_db(self):
        with self.app_context():
            with self.app() as client:
                RecipeModel("Test title", "Test url", "Test, ingredients").save_to_db()
                response = client.post(f"{URL}/favourite_recipe",
                                       data=json.dumps({
                                           "title": "Test title",
                                           "href": "Test url",
                                           "ingredients": "Test, ingredients",
                                           "category": "Meat",
                                           "comment": "The most delicious ever!"
                                       }),
                                       headers={
                                           "Content-Type": "application/json",
                                           "Authorization": f"Bearer {self.access_token}"
                                       })

        expected = {'message': "Successfully saved",
                    "saved_recipe": {
                        "recipe_id": 1,
                        "save_date": datetime.strftime(self.current_time, "%Y-%m-%d %H:%M"),
                        "category": "Meat",
                        "comment": "The most delicious ever!",
                        "recipe_title": "Test title",
                        "recipe_link": "Test url",
                        "ingredients": "Test, ingredients"
                    }
                    }

        self.assertDictEqual(json.loads(response.data), expected,
                             "Message returned when successfully saving a favourite recipe "
                             "(which was already existing in the recipes table) is incorrect.")
        self.assertEqual(response.status_code, 201,
                         "Status code returned when successfully saving a favourite recipe "
                         "(which was already existing in the recipes table) is incorrect.")

    def test_post_as_favourite_duplicate(self):
        with self.app_context():
            with self.app() as client:
                client.post(f"{URL}/favourite_recipe",
                            data=json.dumps({
                                "title": "Test title",
                                "href": "Test url",
                                "ingredients": "Test, ingredients",
                                "category": "Meat",
                                "comment": "The most delicious ever!"
                            }),
                            headers={
                                "Content-Type": "application/json",
                                "Authorization": f"Bearer {self.access_token}"
                            })

                response = client.post(f"{URL}/favourite_recipe",
                                       data=json.dumps({
                                           "title": "Test title",
                                           "href": "Test url",
                                           "ingredients": "Test, ingredients",
                                           "category": "Meat",
                                           "comment": "The most delicious ever!"
                                       }),
                                       headers={
                                           "Content-Type": "application/json",
                                           "Authorization": f"Bearer {self.access_token}"
                                       })

        expected = {"message":
                        "You have already this recipe saved in your favourites. "
                        "If you want to update it, use the update endpoint."}

        self.assertDictEqual(json.loads(response.data), expected,
                             "Message returned after a client attempted to save a duplicate recipe"
                             "as a favourite recipe is incorrect.")
        self.assertEqual(response.status_code, 400,
                         "Status code returned after a client attempted to save a duplicate recipe"
                         "as a favourite recipe is incorrect.")


class TestFavouriteRecipeResource(BaseTest):
    def setUp(self) -> None:
        super(TestFavouriteRecipeResource, self).setUp()
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
                self.current_time = datetime.utcnow()

    def test_get_not_found(self):
        with self.app_context():
            with self.app() as client:
                response = client.get(f"{URL}/favourite_recipe/1",
                                      headers={
                                          "Authorization": f"Bearer {self.access_token}"
                                      })

                expected = {'message': "Sorry, I couldn't find this recipe in your favourites."}

                self.assertDictEqual(json.loads(response.data), expected,
                                     "Message returned when favourite recipe not found in favourites is incorrect.")
                self.assertEqual(response.status_code, 404,
                                 "Status code returned when favourite recipe not found in favourites is incorrect.")

    def test_get_success(self):
        with self.app_context():
            with self.app() as client:
                recipe_id, _ = RecipeModel("Title1", "Url1", "Ingredients1, test1").save_to_db()
                FavouriteRecipesModel(1, recipe_id, self.current_time,
                                      "Meat", "The most delicious ever!").save_to_db()

                response = client.get(f"{URL}/favourite_recipe/1",
                                      headers={
                                          "Authorization": f"Bearer {self.access_token}"
                                      })

                expected = {"Recipe": {
                    "recipe_id": 1,
                    "save_date": datetime.strftime(self.current_time, "%Y-%m-%d %H:%M"),
                    "category": "Meat",
                    "comment": "The most delicious ever!",
                    "recipe_title": "Title1",
                    "recipe_link": "Url1",
                    "ingredients": "Ingredients1, test1"
                }
                }

                self.assertDictEqual(json.loads(response.data), expected,
                                     "Favourite recipe returned to a client is not what expected.")
                self.assertEqual(response.status_code, 200,
                                 "Status code of an attempt to return a favourite recipe "
                                 "to a client is not what expected.")

    def test_put_not_found(self):
        with self.app_context():
            with self.app() as client:
                response = client.put(f"{URL}/favourite_recipe/1",
                                      data=json.dumps({
                                          "category": "Awful",
                                          "comment": "Don't ever try again!!"
                                      }),
                                      headers={
                                          "Content-Type": "application/json",
                                          "Authorization": f"Bearer {self.access_token}"
                                      })

                expected = {'message': "Sorry, I couldn't find this recipe among your favourites."}

                self.assertDictEqual(json.loads(response.data), expected,
                                     "Message returned while trying to update a favourite recipe"
                                     "but it was not found in favourites is incorrect.")
                self.assertEqual(response.status_code, 404,
                                 "Status code returned while trying to update a favourite recipe"
                                 "but it was not found in favourites is incorrect.")

    def test_put_success(self):
        with self.app_context():
            with self.app() as client:
                recipe_id, _ = RecipeModel("Title1", "Url1", "Ingredients1, test1").save_to_db()
                FavouriteRecipesModel(1, recipe_id, self.current_time,
                                      "Meat", "The most delicious ever!").save_to_db()

                response = client.put(f"{URL}/favourite_recipe/1",
                                      data=json.dumps({
                                          "category": "Awful",
                                          "comment": "Don't ever try again!!"
                                      }),
                                      headers={
                                          "Content-Type": "application/json",
                                          "Authorization": f"Bearer {self.access_token}"
                                      })

                expected = {"Recipe updated!": {
                    "recipe_id": 1,
                    "save_date": datetime.strftime(self.current_time, "%Y-%m-%d %H:%M"),
                    "category": "Awful",
                    "comment": "Don't ever try again!!",
                    "recipe_title": "Title1",
                    "recipe_link": "Url1",
                    "ingredients": "Ingredients1, test1"
                }
                }

                self.assertDictEqual(json.loads(response.data), expected,
                                     "Message returned while trying to successfully update a favourite recipe"
                                     " is incorrect.")
                self.assertEqual(response.status_code, 201,
                                 "Status code returned while trying to successfully update a favourite recipe"
                                 " is incorrect.")

    def test_delete_not_found(self):
        with self.app_context():
            with self.app() as client:
                response = client.delete(f"{URL}/favourite_recipe/1",
                                         headers={
                                             "Authorization": f"Bearer {self.access_token}"
                                         })

                expected = {'message': "Sorry, I couldn't find this recipe among your favourites."}

                self.assertDictEqual(json.loads(response.data), expected,
                                     "Incorrect message returned while trying to delete a favourite recipe"
                                     "but it was not found in favourites.")
                self.assertEqual(response.status_code, 404,
                                 "Incorrect status code returned while trying to delete a favourite recipe"
                                 "but it was not found in favourites.")

    def test_delete_success(self):
        with self.app_context():
            with self.app() as client:
                recipe_id, _ = RecipeModel("Title1", "Url1", "Ingredients1, test1").save_to_db()
                FavouriteRecipesModel(1, recipe_id, self.current_time,
                                      "Meat", "The most delicious ever!").save_to_db()

                self.assertIsNotNone(RecipeModel.find_by_recipe_id(1),
                                     "While running TestFavouriteRecipeResource.test_delete_success(),"
                                     "the recipe was not saved successfully to db.")

                self.assertIsNotNone(FavouriteRecipesModel.find_by_recipe_id(1),
                                     "While running TestFavouriteRecipeResource.test_delete_success(),"
                                     "the favourite recipe was not saved successfully to db.")

                response = client.delete(f"{URL}/favourite_recipe/1",
                                         headers={
                                             "Authorization": f"Bearer {self.access_token}"
                                         })

                expected = {"message": f"Recipe with the id 1 removed successfully from your favourites!"}

                self.assertDictEqual(json.loads(response.data), expected,
                                     "Incorrect message returned while trying to successfully delete "
                                     "a favourite recipe.")
                self.assertEqual(response.status_code, 200,
                                 "Incorrect status code returned while trying to successfully delete "
                                 "a favourite recipe.")

                self.assertIsNone(RecipeModel.find_by_recipe_id(1),
                                  "While running TestFavouriteRecipeResource.test_delete_success(),"
                                  "the recipe was not deleted successfully from db.")

                self.assertListEqual(FavouriteRecipesModel.find_by_recipe_id(1), [],
                                     "While running TestFavouriteRecipeResource.test_delete_success(),"
                                     "the favourite recipe was not deleted successfully from db.")
