from blacklist import BLACKLIST_LOGOUT
from models.recipe import RecipeModel
from models.user import UserModel
from models.users_favourite_recipes import FavouriteRecipesModel
from tests.base_test import BaseTest, URL
import json
from datetime import datetime


class TestUserLogin(BaseTest):
    def test_post_success(self):
        with self.app_context():
            with self.app() as client:
                UserModel("Test name", "aA1!").save_to_db()
                response = client.post(f"{URL}/login",
                                       data=json.dumps({
                                           "username": "Test name",
                                           "password": "aA1!"
                                       }),
                                       headers={
                                           "Content-Type": "application/json"
                                       }
                                       )
                self.assertEqual(response.status_code, 200,
                                 "Improper status code while trying to successfully log in.")
                self.assertIn("access_token", json.loads(response.data).keys(),
                              "Lack of access_token while trying to successfully log in.")
                self.assertIn("refresh_token", json.loads(response.data).keys(),
                              "Lack of refresh_token while trying to successfully log in.")

    def test_post_invalid_credentials(self):
        with self.app_context():
            with self.app() as client:
                response = client.post(f"{URL}/login",
                                       data=json.dumps({
                                           "username": "Test name",
                                           "password": "aA1!"
                                       }),
                                       headers={
                                           "Content-Type": "application/json"
                                       }
                                       )
                expected = {"message": "Invalid credentials."}

                self.assertEqual(response.status_code, 401,
                                 "Improper status code while trying to log in with invalid credentials.")
                self.assertEqual(json.loads(response.data), expected,
                                 "Improper message while trying to log in with invalid credentials.")


class TestRefreshToken(BaseTest):
    def test_post_refresh_token(self):
        with self.app_context():
            with self.app() as client:
                UserModel("Test name", "aA1!").save_to_db()
                response = client.post(f"{URL}/login",
                                       data=json.dumps({
                                           "username": "Test name",
                                           "password": "aA1!"
                                       }),
                                       headers={
                                           "Content-Type": "application/json"
                                       }
                                       )
                refresh_token = json.loads(response.data)['refresh_token']

                response = client.post(f"{URL}/refresh",
                                       headers={
                                           "Content-Type": "application/json",
                                           "Authorization": f"Bearer {refresh_token}"
                                       })
                self.assertEqual(response.status_code, 200)
                self.assertIn("access_token", json.loads(response.data).keys())


class TestUserLogoutAndLogout2(BaseTest):
    def test_delete(self):
        with self.app_context():
            with self.app() as client:
                UserModel("Test name", "aA1!").save_to_db()
                response = client.post(f"{URL}/login",
                                       data=json.dumps({
                                           "username": "Test name",
                                           "password": "aA1!"
                                       }),
                                       headers={
                                           "Content-Type": "application/json"
                                       }
                                       )
                access_token = json.loads(response.data)['access_token']
                refresh_token = json.loads(response.data)['refresh_token']

                self.assertEqual(len(BLACKLIST_LOGOUT), 0)

                response = client.delete(f"{URL}/logout",
                                         headers={
                                             "Content-Type": "application/json",
                                             "Authorization": f"Bearer {access_token}"
                                         })

                expected = {"message": "Successfully logged out!"}

                self.assertEqual(response.status_code, 200)
                self.assertEqual(json.loads(response.data), expected)
                self.assertEqual(len(BLACKLIST_LOGOUT), 1)

                response = client.delete(f"{URL}/logout2",
                                         headers={
                                             "Content-Type": "application/json",
                                             "Authorization": f"Bearer {refresh_token}"
                                         })

                expected = {"message": "Successfully logged out!"}

                self.assertEqual(response.status_code, 200)
                self.assertEqual(json.loads(response.data), expected)
                self.assertEqual(len(BLACKLIST_LOGOUT), 2)


class TestDeleteAccount(BaseTest):
    def setUp(self) -> None:
        super(TestDeleteAccount, self).setUp()
        with self.app_context():
            with self.app() as client:
                self.current_time = datetime.utcnow()
                UserModel("TestUsername", "TestPwd1!").save_to_db()
                self.recipe_id1, _ = RecipeModel("Title1", "Url1", "Ingredients1, test1").save_to_db()
                recipe_id2, _ = RecipeModel("Title2", "Url2", "Ingredients2, test2").save_to_db()
                recipe_id3, _ = RecipeModel("Title3", "Url3", "Ingredients3, test3").save_to_db()
                FavouriteRecipesModel(1, self.recipe_id1, self.current_time,
                                      "Test category - salad", "Test comment - for Friday's dinner").save_to_db()
                FavouriteRecipesModel(1, recipe_id2, self.current_time,
                                      "Test category - salad", "Test comment - for Friday's dinner").save_to_db()
                FavouriteRecipesModel(1, recipe_id3, self.current_time,
                                      "Test category - salad", "Test comment - for Friday's dinner").save_to_db()

    def test_delete_with_all_recipes(self):
        with self.app_context():
            with self.app() as client:
                self.assertEqual(RecipeModel.count_all()[0], 3,
                                 "The number of recipes saved to db is not correct.")
                self.assertEqual(len(FavouriteRecipesModel.show_mine(1)), 3,
                                 "The number of favourite recipes saved to db is not correct.")

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

                response = client.delete(f"{URL}/delete_account/TestUsername",
                                         headers={
                                             "Content-Type": "application/json",
                                             "Authorization": f"Bearer {access_token}"
                                         }
                                         )

                expected = {"message": f"User's account (username: TestUsername) deleted successfully!",
                            "access_token": None,
                            "refresh_token": None}

                self.assertEqual(response.status_code, 200,
                                 "Status code after deleting a user is not correct.")
                self.assertEqual(json.loads(response.data), expected,
                                 "Message returned after deleting a user is not correct.")
                self.assertEqual(RecipeModel.count_all()[0], 0,
                                 "The number of recipes saved to db after deleting a user is not correct.")
                self.assertEqual(len(FavouriteRecipesModel.show_mine(1)), 0,
                                 "The number of favourite recipes saved to db after deleting a user is not correct.")

    def test_delete_when_2_users_saved_same_recipe(self):
        with self.app_context():
            with self.app() as client:
                UserModel("User2", "pwd1!").save_to_db()
                FavouriteRecipesModel(2, self.recipe_id1, self.current_time,
                                      "Category of the second user", "User2's comment").save_to_db()

                self.assertEqual(RecipeModel.count_all()[0], 3,
                                 "The number of recipes saved to db is not correct.")
                self.assertEqual(len(FavouriteRecipesModel.show_mine(1)), 3,
                                 "The number of favourite recipes saved to db is not correct.")
                self.assertEqual(len(FavouriteRecipesModel.show_mine(2)), 1,
                                 "The number of favourite recipes saved to db is not correct.")

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

                response = client.delete(f"{URL}/delete_account/TestUsername",
                                         headers={
                                             "Content-Type": "application/json",
                                             "Authorization": f"Bearer {access_token}"
                                         }
                                         )

                expected = {"message": f"User's account (username: TestUsername) deleted successfully!",
                            "access_token": None,
                            "refresh_token": None}

                self.assertEqual(response.status_code, 200,
                                 "Status code after deleting a user is not correct.")
                self.assertDictEqual(json.loads(response.data), expected,
                                     "Message returned after deleting a user is not correct.")
                self.assertEqual(RecipeModel.count_all()[0], 1,
                                 "The number of recipes saved to db after deleting a user is not correct.")
                self.assertEqual(len(FavouriteRecipesModel.show_mine(1)), 0,
                                 "The number of favourite recipes saved to db after deleting a user is not correct.")
                self.assertEqual(len(FavouriteRecipesModel.show_mine(2)), 1,
                                 "The number of favourite recipes saved to db after deleting a user is not correct.")


class TestAdminDeleteAccount(BaseTest):
    def test_delete_when_not_admin(self):
        with self.app_context():
            with self.app() as client:
                UserModel("TestUser", "Pwd1!").save_to_db()
                UserModel("TestUserToBeDeleted", "Pwd1!").save_to_db()
                response = client.post(f"{URL}/login",
                                       data=json.dumps({
                                           "username": "TestUser",
                                           "password": "Pwd1!"
                                       }),
                                       headers={
                                           "Content-Type": "application/json"
                                       }
                                       )
                access_token = json.loads(response.data)['access_token']
                response = client.delete(f"{URL}/admin_delete_account/2",
                                         data=json.dumps({
                                             "username": "TestUser",
                                             "password": "Pwd1!"
                                         }),
                                         headers={
                                             "Content-Type": "application/json",
                                             "Authorization": f"Bearer {access_token}"
                                         }
                                         )

                expected = {"message": "Admin permission required!"}

                self.assertEqual(response.status_code, 403)
                self.assertDictEqual(json.loads(response.data), expected)

    def test_delete_when_admin(self):
        with self.app_context():
            with self.app() as client:
                UserModel("TestAdmin", "Pwd1!", admin=1).save_to_db()
                UserModel("TestUserToBeDeleted", "Pwd1!").save_to_db()

                self.current_time = datetime.utcnow()
                self.recipe_id1, _ = RecipeModel("Title1", "Url1", "Ingredients1, test1").save_to_db()
                recipe_id2, _ = RecipeModel("Title2", "Url2", "Ingredients2, test2").save_to_db()
                recipe_id3, _ = RecipeModel("Title3", "Url3", "Ingredients3, test3").save_to_db()
                FavouriteRecipesModel(2, self.recipe_id1, self.current_time,
                                      "Test category - salad", "Test comment - for Friday's dinner").save_to_db()
                FavouriteRecipesModel(2, recipe_id2, self.current_time,
                                      "Test category - salad", "Test comment - for Friday's dinner").save_to_db()
                FavouriteRecipesModel(2, recipe_id3, self.current_time,
                                      "Test category - salad", "Test comment - for Friday's dinner").save_to_db()

                FavouriteRecipesModel(1, self.recipe_id1, self.current_time,
                                      "Category of the second user", "User2's comment").save_to_db()

                self.assertEqual(RecipeModel.count_all()[0], 3,
                                 "The number of recipes saved to db is not correct.")
                self.assertEqual(len(FavouriteRecipesModel.show_mine(2)), 3,
                                 "The number of favourite recipes saved to db is not correct.")
                self.assertEqual(len(FavouriteRecipesModel.show_mine(1)), 1,
                                 "The number of favourite recipes saved to db is not correct.")

                response = client.post(f"{URL}/login",
                                       data=json.dumps({
                                           "username": "TestAdmin",
                                           "password": "Pwd1!"
                                       }),
                                       headers={
                                           "Content-Type": "application/json"
                                       }
                                       )
                access_token = json.loads(response.data)['access_token']
                response = client.delete(f"{URL}/admin_delete_account/2",
                                         data=json.dumps({
                                             "username": "TestUser",
                                             "password": "Pwd1!"
                                         }),
                                         headers={
                                             "Content-Type": "application/json",
                                             "Authorization": f"Bearer {access_token}"
                                         }
                                         )

                expected = {"message": f"User's account (user_id: 2) deleted successfully!"}

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), expected)

                self.assertEqual(RecipeModel.count_all()[0], 1,
                                 "The number of recipes saved to db is not correct.")
                self.assertEqual(len(FavouriteRecipesModel.show_mine(2)), 0,
                                 "The number of favourite recipes saved to db is not correct.")
                self.assertEqual(len(FavouriteRecipesModel.show_mine(1)), 1,
                                 "The number of favourite recipes saved to db is not correct.")