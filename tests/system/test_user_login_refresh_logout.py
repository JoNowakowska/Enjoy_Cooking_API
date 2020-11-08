from blacklist import BLACKLIST_LOGOUT
from models.user import UserModel
from tests.base_test import BaseTest, URL
import json


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

