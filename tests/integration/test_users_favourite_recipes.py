from tests.base_test import BaseTest
from models.users_favourite_recipes import FavouriteRecipesModel
from models.user import UserModel
from models.recipe import RecipeModel
from datetime import datetime


class TestUsersFavouriteRecipes(BaseTest):
    def setUp(self) -> None:
        super(TestUsersFavouriteRecipes, self).setUp()
        with self.app_context():
            self.user = UserModel("Test name", "Test password")
            self.user.save_to_db()
            recipe = RecipeModel("Test title", "Test link", "Test ingredients")
            recipe.save_to_db()
            self.time_now = datetime.utcnow()
            self.f_recipe = FavouriteRecipesModel(self.user.user_id, recipe.recipe_id, self.time_now, "Test cat",
                                                  "Test comment")

    def test_crud(self):
        with self.app_context():
            self.assertListEqual(FavouriteRecipesModel.find_by_recipe_id(1), [],
                                 "The favourite recipe was found in db (by id = 1) while it should not be found,"
                                 "because has not been saved yet.")
            self.f_recipe.save_to_db()

            self.assertEqual(len(FavouriteRecipesModel.find_by_recipe_id(1)), 1,
                             "The favourite recipe wasn't found in db (by id = 1) while it should be found.")
            self.assertEqual(FavouriteRecipesModel.find_by_recipe_id(1)[0].save_date, self.time_now,
                             "The favourite recipe's save_date is not correct.")
            self.assertEqual(FavouriteRecipesModel.find_by_recipe_id(1)[0].category, "Test cat",
                             "The favourite recipe's category is not correct.")
            self.assertEqual(FavouriteRecipesModel.find_by_recipe_id(1)[0].comment, "Test comment",
                             "The favourite recipe's comment is not correct.")
            self.assertIsNotNone(FavouriteRecipesModel.find_by_recipe_id_user_id(1, 1),
                                 "The favourite recipe wasn't found in db (by recipe_id = 1 and user_id = 1)"
                                 "while it should be found.")
            self.f_recipe.delete_from_db()
            self.assertListEqual(FavouriteRecipesModel.find_by_recipe_id(1), [],
                                 "The favourite recipe was found in db (by id = 1) while it should not be found, "
                                 "because should be deleted.")

    def test_json(self):
        with self.app_context():
            self.f_recipe.save_to_db()
            favourite_recipe = FavouriteRecipesModel.find_by_recipe_id_user_id(1, 1)
            expected = {
                "recipe_id": 1,
                "save_date": datetime.strftime(self.time_now, "%Y-%m-%d %H:%M"),
                "category": "Test cat",
                "comment": "Test comment"
            }

            self.assertEqual(favourite_recipe.json(), expected,
                             "Json method does not return a desired dictionary.")

    def test_update_to_db(self):
        with self.app_context():
            self.f_recipe.save_to_db()
            favourite_recipe = FavouriteRecipesModel.find_by_recipe_id_user_id(1, 1)
            favourite_recipe.update_to_db({"category": "New cat", "comment": "New comment"})
            self.assertEqual(favourite_recipe.category, "New cat",
                             "The updated category does not match to the one saved in db.")
            self.assertEqual(favourite_recipe.comment, "New comment",
                             "The updated comment does not match to the one saved in db.")

    def test_show_mine(self):
        with self.app_context():
            self.f_recipe.save_to_db()
            recipe2 = RecipeModel("Test title 2", "Test link 2", "Test ingredients 2")
            recipe2.save_to_db()
            f_recipe2 = FavouriteRecipesModel(self.user.user_id, recipe2.recipe_id, self.time_now)
            f_recipe2.save_to_db()
            my_recipes = [(
                fr.recipe_id,
                fr.save_date,
                fr.category,
                fr.comment,
                rm.recipe_title,
                rm.href,
                rm.recipe_ingredients
            )
                for (fr, rm) in FavouriteRecipesModel.show_mine(self.user.user_id)]

            expected = [
                (
                    1,
                    self.time_now,
                    'Test cat',
                    'Test comment',
                    'Test title',
                    'Test link',
                    'Test ingredients'
                ),
                (
                    2,
                    self.time_now,
                    None,
                    None,
                    'Test title 2',
                    'Test link 2',
                    'Test ingredients 2'
                )
            ]

            self.assertListEqual(my_recipes, expected,
                                 "FavouriteRecipesModel.show_mine() query does not return proper values.")

    def test_show_my_recipe_ids(self):
        with self.app_context():
            self.f_recipe.save_to_db()
            recipe2 = RecipeModel("Test title 2", "Test link 2", "Test ingredients 2")
            recipe2.save_to_db()
            f_recipe2 = FavouriteRecipesModel(self.user.user_id, recipe2.recipe_id, self.time_now)
            f_recipe2.save_to_db()
            my_recipes_ids = FavouriteRecipesModel.show_my_recipe_ids(self.user.user_id)
            self.assertListEqual(my_recipes_ids, [(1,), (2,)],
                                 "FavouriteRecipesModel.show_my_recipe_ids() returns wrong values.")

    def test_show_all(self):
        with self.app_context():
            self.f_recipe.save_to_db()
            recipe2 = RecipeModel("Test title 2", "Test link 2", "Test ingredients 2")
            recipe2.save_to_db()
            f_recipe2 = FavouriteRecipesModel(self.user.user_id, recipe2.recipe_id, self.time_now)
            f_recipe2.save_to_db()
            all_recipes = FavouriteRecipesModel.show_all()
            self.assertEqual(len(all_recipes), 2,
                             "FavouriteRecipesModel.show_all() does not query the db appropriately.")

    def test_show_stats(self):
        with self.app_context():
            self.f_recipe.save_to_db()
            recipe2 = RecipeModel("Test title 2", "Test link 2", "Test ingredients 2")
            recipe2.save_to_db()
            f_recipe2 = FavouriteRecipesModel(self.user.user_id, recipe2.recipe_id, self.time_now)
            f_recipe2.save_to_db()
            user2 = UserModel("User 2", "Pass 2")
            user2.save_to_db()
            f_rec_user2 = FavouriteRecipesModel(user2.user_id, recipe2.recipe_id, self.time_now)
            f_rec_user2.save_to_db()
            stats = [(rm.recipe_id, stat) for (rm, stat) in FavouriteRecipesModel.show_stats()]
            expected = [(1, 1), (2, 2)]

            self.assertListEqual(stats, expected,
                                 "FavouriteRecipesModel.show_stats() produces improper stats.")
