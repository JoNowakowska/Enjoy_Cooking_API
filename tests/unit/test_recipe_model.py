from tests.unit.base_test import BaseTest
from models.recipe import RecipeModel


class RecipeModelTest(BaseTest):
    def setUp(self) -> None:
        self.new_recipe = RecipeModel("Test title", "Test http", "Test ingredients")
        self.new_recipe.recipe_id = 1

    def test_init(self):
        self.assertEqual(self.new_recipe.recipe_title, "Test title")
        self.assertEqual(self.new_recipe.href, "Test http")
        self.assertEqual(self.new_recipe.recipe_ingredients, "Test ingredients")

    def test_json(self):
        expected_output = {
            "recipe_id": 1,
            "recipe_title": "Test title",
            "recipe_link": "Test http",
            "recipe_ingredients": "Test ingredients"
        }

        self.assertDictEqual(self.new_recipe.json(), expected_output)