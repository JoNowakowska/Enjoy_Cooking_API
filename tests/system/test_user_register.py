from models.user import UserModel
from tests.base_test import BaseTest, URL
import json


class TestUserRegister(BaseTest):
    def test_post_password_not_secure(self):
        with self.app_context():
            with self.app() as client:
                response = client.post(f"{URL}/register",
                                       data=json.dumps({
                                           "username": "Test username",
                                           "password": "Test password"
                                       }),
                                       headers={
                                           "Content-Type": "application/json"
                                       }
                                       )
                expected = {"message": "Your password needs to contain at least 1 small letter, "
                                       "1 capital letter, 1 number and 1 special character."}

                self.assertEqual(json.loads(response.data), expected,
                                 "The message returned by the endpoint /register "
                                 "while trying to set an unsecure password is not what was expected")
                self.assertEqual(response.status_code, 400,
                                 "The status code returned by the endpoint /register "
                                 "while trying to set an unsecure password is not what was expected")

    def test_post_duplicate_user(self):
        with self.app_context():
            with self.app() as client:
                UserModel("Test username", "Test password").save_to_db()
                response = client.post(f"{URL}/register",
                                       data=json.dumps({
                                           "username": "Test username",
                                           "password": "Test password"
                                       }),
                                       headers={
                                           "Content-Type": "application/json"
                                       }
                                       )
                expected = {"message": "This username is already taken. Please select another one."}

                self.assertEqual(json.loads(response.data), expected,
                                 "The message returned by the endpoint /register "
                                 "while trying to register an already existing username is not what was expected")
                self.assertEqual(response.status_code, 400,
                                 "The status code returned by the endpoint /register "
                                 "while trying to register an already existing username is not what was expected")

    def test_post_successfully_created(self):
        with self.app_context():
            with self.app() as client:
                response = client.post(f"{URL}/register",
                                       data=json.dumps({
                                           "username": "Test username",
                                           "password": "Aa1!"
                                       }),
                                       headers={
                                           "Content-Type": "application/json"
                                       }
                                       )
                expected = {"message": "User Test username created successfully!"}

                self.assertEqual(json.loads(response.data), expected,
                                 "The message returned by the endpoint /register "
                                 "while registering user successfully is not what was expected")
                self.assertEqual(response.status_code, 201,
                                 "The status code returned by the endpoint /register "
                                 "while registering user successfully is not what was expected")