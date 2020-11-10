from tests.unit.base_test import BaseTest
from models.users_favourite_recipes import FavouriteRecipesModel
from datetime import datetime


class FavouriteRecipesModelTest(BaseTest):
    def setUp(self) -> None:
        self.current_time = datetime.utcnow()

    def test_init(self):
        favourite = FavouriteRecipesModel(1, 1, self.current_time, "Meat", "The most delicious ever!")

        self.assertEqual(favourite.user_id, 1)
        self.assertEqual(favourite.recipe_id, 1)
        self.assertEqual(favourite.save_date, self.current_time)
        self.assertEqual(favourite.category, "Meat")
        self.assertEqual(favourite.comment, "The most delicious ever!")

    def test_init_no_category_no_comment(self):
        favourite = FavouriteRecipesModel(1, 1, self.current_time)

        self.assertIsNone(favourite.category)
        self.assertIsNone(favourite.comment)
