from tests.base_test import BaseTest
from models.recipe import RecipeModel


class RecipeModelTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            recipe = RecipeModel("Title1", "Url1", "Ingredients1, test1")
            self.assertIsNone(RecipeModel.find_by_href("Url1"),
                              f"Recipe object with a href {recipe.href} should not exist in the table.")
            recipe.save_to_db()
            self.assertIsNotNone(RecipeModel.find_by_href("Url1"),
                                 f"Recipe object with a link {recipe.href} failed to save to db")
            self.assertIsNotNone(RecipeModel.find_by_recipe_id(1),
                                 f"Recipe did not find by its (manually created) id.")
            self.assertEqual(RecipeModel.find_by_href("Url1").recipe_title, "Title1",
                             f"Recipe title does not equal the desired one {recipe.recipe_title}")
            recipe.delete_from_db(1)
            self.assertIsNone(RecipeModel.find_by_href("Url1"),
                              "Recipe object found in db, while it should already be deleted.")

    def test_count_all(self):
        with self.app_context():
            recipe1 = RecipeModel("Title1", "Url1", "Ingredients1, test1")
            recipe2 = RecipeModel("Title2", "Url2", "Ingredients1, test2")
            recipe3 = RecipeModel("Title3", "Url3", "Ingredients1, test3")
            recipe1.save_to_db()
            recipe2.save_to_db()
            recipe3.save_to_db()
            no_of_recipes = RecipeModel.count_all()[0]

            self.assertEqual(no_of_recipes, 3,
                             "RecipeModel.count_all() failed to count a proper number of recipes")
