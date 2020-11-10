from tests.base_test import BaseTest
from models.user import UserModel


class UserModelTest(BaseTest):
    def test_crud_user(self):
        with self.app_context():
            new_user = UserModel("TestUsername", "TestPwd1!")
            self.assertIsNone(UserModel.find_by_username("TestUsername"),
                              "A user should not be found in db, but was.")
            new_user.save_to_db()
            self.assertIsNotNone(UserModel.find_by_username("TestUsername"),
                                 f"A user {new_user.username} should exist in db, but doesn't.")
            self.assertEqual(UserModel.find_by_username("TestUsername").admin, 0,
                             "This user should have the admin property = 0, while it has not.")
            self.assertEqual(UserModel.find_by_username("TestUsername").password, "TestPwd1!",
                             "User's password does not match to the desired one.")
            new_user.delete_from_db()
            self.assertIsNone(UserModel.find_by_username("TestUsername"),
                              "A user should not be found in db, but was.")

    def test_crud_admin(self):
        with self.app_context():
            new_admin = UserModel("TestAdmin", "TestPwd1!", admin=1)
            self.assertIsNone(UserModel.find_by_id(1),
                              "An admin should not be found in db, but was.")
            new_admin.save_to_db()
            self.assertEqual(UserModel.find_by_username("TestAdmin").admin, 1,
                             "This user is not an admin while should be.")
            self.assertEqual(UserModel.find_by_username("TestAdmin").password, "TestPwd1!",
                             "Admin's password does not match to the desired one.")
            new_admin.delete_from_db()
            self.assertIsNone(UserModel.find_by_id(1),
                              "An admin should not be found in db, but was.")

    def test_count_all_and_show_all(self):
        with self.app_context():
            user1 = UserModel("TestUsername", "TestPwd1!")
            user2 = UserModel("TestUsername2", "TestPwd1!")
            user3 = UserModel("TestUsername3", "TestPwd1!")
            user1.save_to_db()
            user2.save_to_db()
            user3.save_to_db()
            no_of_users = UserModel.count_all()[0]
            self.assertEqual(no_of_users, 3,
                             "Number of users does not much the number calculated by the UserModel.count_all() method.")
            all_usernames = [u.username for (u, _) in UserModel.show_all()]
            self.assertListEqual(all_usernames, ["TestUsername", "TestUsername2", "TestUsername3"],
                                 "The UserModel.show_all() does not create a proper list of users "
                                 "- demonstrated by a comparison of usernames")
