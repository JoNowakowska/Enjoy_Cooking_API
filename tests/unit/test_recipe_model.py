from unittest import TestCase
from models.recipe import RecipeModel
from models.users_favourite_recipes import FavouriteRecipesModel
from models.user import UserModel


class RecipeModelTest(TestCase):
    def test_init(self):
        new_recipe = RecipeModel("Test title", "Test http", "Test ingredients")
        self.assertEqual(new_recipe.recipe_title, "Test title")
        self.assertEqual(new_recipe.href, "Test http")
        self.assertEqual(new_recipe.recipe_ingredients, "Test ingredients")

    def test_json(self):
        new_recipe = RecipeModel("Test title", "Test http", "Test ingredients")
        new_recipe.recipe_id = 1
        expected_output = {
            "recipe_id": 1,
            "recipe_title": "Test title",
            "recipe_link": "Test http",
            "recipe_ingredients": "Test ingredients"
        }

        self.assertDictEqual(new_recipe.json(), expected_output)