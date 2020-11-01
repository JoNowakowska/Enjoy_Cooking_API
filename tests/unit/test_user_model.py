from tests.unit.base_test import BaseTest
from models.user import UserModel


class UserModelTest(BaseTest):
    def test_init_admin(self):
        user = UserModel("Test username", "Test password", 1)
        user.user_id = 1

        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.username, "Test username")
        self.assertEqual(user.password, "Test password")
        self.assertEqual(user.admin, 1)

    def test_init_user(self):
        user = UserModel("Test username", "Test password")
        user.user_id = 1

        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.username, "Test username")
        self.assertEqual(user.password, "Test password")
        self.assertEqual(user.admin, 0)