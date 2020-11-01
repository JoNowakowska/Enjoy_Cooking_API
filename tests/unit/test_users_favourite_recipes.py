from unittest import TestCase
from models.users_favourite_recipes import FavouriteRecipesModel
from models.recipe import RecipeModel
from models.user import UserModel
import datetime


class FavouriteRecipesModelTest(TestCase):
    def test_init(self):
        time = datetime.datetime.utcnow()
        favourite = FavouriteRecipesModel(1, 1, time, "salad", "good for a Halloween party")

        self.assertEqual(favourite.user_id, 1)
        self.assertEqual(favourite.recipe_id, 1)
        self.assertEqual(favourite.save_date, time)
        self.assertEqual(favourite.category, "salad")
        self.assertEqual(favourite.comment, "good for a Halloween party")

    def test_init_no_category_no_comment(self):
        time = datetime.datetime.utcnow()
        favourite = FavouriteRecipesModel(1, 1, time)

        self.assertIsNone(favourite.category)
        self.assertIsNone(favourite.comment)

    def test_json(self):
        time = datetime.datetime.utcnow()
        favourite = FavouriteRecipesModel(1, 1, time, "salad", "good for a Halloween party")
        expected = {
            "recipe_id": 1,
            "save_date": datetime.datetime.strftime(time, "%Y-%m-%d %H:%M"),
            "category": "salad",
            "comment": "good for a Halloween party"
        }

        self.assertDictEqual(favourite.json(), expected)

    def test_json_no_category_no_comment(self):
        time = datetime.datetime.utcnow()
        favourite = FavouriteRecipesModel(1, 1, time)
        expected = {
            "recipe_id": 1,
            "save_date": datetime.datetime.strftime(time, "%Y-%m-%d %H:%M"),
            "category": None,
            "comment": None
        }

        self.assertDictEqual(favourite.json(), expected)