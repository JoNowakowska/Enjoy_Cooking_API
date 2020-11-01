from tests.unit.base_test import BaseTest
from models.users_favourite_recipes import FavouriteRecipesModel
import datetime


class FavouriteRecipesModelTest(BaseTest):
    def setUp(self) -> None:
        self.time = datetime.datetime.utcnow()

    def test_init(self):
        favourite = FavouriteRecipesModel(1, 1, self.time, "salad", "good for a Halloween party")

        self.assertEqual(favourite.user_id, 1)
        self.assertEqual(favourite.recipe_id, 1)
        self.assertEqual(favourite.save_date, self.time)
        self.assertEqual(favourite.category, "salad")
        self.assertEqual(favourite.comment, "good for a Halloween party")

    def test_init_no_category_no_comment(self):
        favourite = FavouriteRecipesModel(1, 1, self.time)

        self.assertIsNone(favourite.category)
        self.assertIsNone(favourite.comment)

    def test_json(self):
        favourite = FavouriteRecipesModel(1, 1, self.time, "salad", "good for a Halloween party")
        expected = {
            "recipe_id": 1,
            "save_date": datetime.datetime.strftime(self.time, "%Y-%m-%d %H:%M"),
            "category": "salad",
            "comment": "good for a Halloween party"
        }

        self.assertDictEqual(favourite.json(), expected)

    def test_json_no_category_no_comment(self):
        favourite = FavouriteRecipesModel(1, 1, self.time)
        expected = {
            "recipe_id": 1,
            "save_date": datetime.datetime.strftime(self.time, "%Y-%m-%d %H:%M"),
            "category": None,
            "comment": None
        }

        self.assertDictEqual(favourite.json(), expected)