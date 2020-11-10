from tests.unit.base_test import BaseTest
from models.user import UserModel


class UserModelTest(BaseTest):
    def test_init_admin(self):
        user = UserModel("TestAdmin", "TestPwd1!", 1)
        user.user_id = 1

        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.username, "TestAdmin")
        self.assertEqual(user.password, "TestPwd1!")
        self.assertEqual(user.admin, 1)

    def test_init_user(self):
        user = UserModel("TestUsername", "TestPwd1!")
        user.user_id = 1

        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.username, "TestUsername")
        self.assertEqual(user.password, "TestPwd1!")
        self.assertEqual(user.admin, 0)