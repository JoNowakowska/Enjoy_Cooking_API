from tests.unit.base_test import BaseTest
from models.recipe import RecipeModel


class RecipeModelTest(BaseTest):
    def setUp(self) -> None:
        self.new_recipe = RecipeModel("Title1", "Url1", "Ingredients1, test1")
        self.new_recipe.recipe_id = 1

    def test_init(self):
        self.assertEqual(self.new_recipe.recipe_title, "Title1")
        self.assertEqual(self.new_recipe.href, "Url1")
        self.assertEqual(self.new_recipe.recipe_ingredients, "Ingredients1, test1")

    def test_json(self):
        expected_output = {
            "recipe_id": 1,
            "recipe_title": "Title1",
            "recipe_link": "Url1",
            "recipe_ingredients": "Ingredients1, test1"
        }

        self.assertDictEqual(self.new_recipe.json(), expected_output)