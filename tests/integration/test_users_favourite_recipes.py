from tests.base_test import BaseTest
from models.users_favourite_recipes import FavouriteRecipesModel
from models.user import UserModel
from models.recipe import RecipeModel
from datetime import datetime


class TestUsersFavouriteRecipes(BaseTest):
    def setUp(self) -> None:
        super(TestUsersFavouriteRecipes, self).setUp()
        with self.app_context():
            self.user = UserModel("TestUsername", "TestPwd1!")
            self.user.save_to_db()
            recipe = RecipeModel("Title1", "Url1", "Ingredients1, test1")
            recipe.save_to_db()
            self.time_now = datetime.utcnow()
            self.f_recipe = FavouriteRecipesModel(self.user.user_id, recipe.recipe_id, self.time_now,
                                                  "Meat", "The most delicious ever!")

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
            self.assertEqual(FavouriteRecipesModel.find_by_recipe_id(1)[0].category, "Meat",
                             "The favourite recipe's category is not correct.")
            self.assertEqual(FavouriteRecipesModel.find_by_recipe_id(1)[0].comment, "The most delicious ever!",
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

            expected = {"recipe_id": 1,
                        "save_date": datetime.strftime(self.time_now, "%Y-%m-%d %H:%M"),
                        "category": "Meat",
                        "comment": "The most delicious ever!",
                        "recipe_title": "Title1",
                        "recipe_link": "Url1",
                        "ingredients": "Ingredients1, test1"
                        }

            self.assertEqual(favourite_recipe.json(), expected,
                             "UsersFavouriteRecipes.json() method does not return a desired dictionary.")

    def test_update_to_db(self):
        with self.app_context():
            self.f_recipe.save_to_db()
            favourite_recipe = FavouriteRecipesModel.find_by_recipe_id_user_id(1, 1)
            favourite_recipe.update_to_db({"category": "Meat", "comment": "The most delicious ever!"})
            self.assertEqual(favourite_recipe.category, "Meat",
                             "The updated category does not match to the one saved in db.")
            self.assertEqual(favourite_recipe.comment, "The most delicious ever!",
                             "The updated comment does not match to the one saved in db.")

    def test_show_mine(self):
        with self.app_context():
            self.f_recipe.save_to_db()
            recipe2 = RecipeModel("Title2", "Url2", "Ingredients2, test2")
            recipe2.save_to_db()
            f_recipe2 = FavouriteRecipesModel(self.user.user_id, recipe2.recipe_id, self.time_now)
            f_recipe2.save_to_db()
            my_recipes = [x.json() for x in FavouriteRecipesModel.show_mine(self.user.user_id)]

            expected = [
                {
                    "recipe_id": 1,
                    "save_date": datetime.strftime(self.time_now, "%Y-%m-%d %H:%M"),
                    "category": "Meat",
                    "comment": "The most delicious ever!",
                    "recipe_title": "Title1",
                    "recipe_link":  "Url1",
                    "ingredients":  "Ingredients1, test1"},
                {
                    "recipe_id": 2,
                    "save_date": datetime.strftime(self.time_now, "%Y-%m-%d %H:%M"),
                    "category": None,
                    "comment": None,
                    "recipe_title": "Title2",
                    "recipe_link":  "Url2",
                    "ingredients":  "Ingredients2, test2"}
            ]

            self.assertListEqual(my_recipes, expected,
                                 "FavouriteRecipesModel.show_mine() query does not return proper values.")

    def test_show_my_recipe_ids(self):
        with self.app_context():
            self.f_recipe.save_to_db()
            recipe2 = RecipeModel("Title2", "Url2", "Ingredients2, test2")
            recipe2.save_to_db()
            f_recipe2 = FavouriteRecipesModel(self.user.user_id, recipe2.recipe_id, self.time_now)
            f_recipe2.save_to_db()
            my_recipes_ids = FavouriteRecipesModel.show_my_recipe_ids(self.user.user_id)
            self.assertListEqual(my_recipes_ids, [(1,), (2,)],
                                 "FavouriteRecipesModel.show_my_recipe_ids() returns wrong values.")

    def test_show_all(self):
        with self.app_context():
            self.f_recipe.save_to_db()
            recipe2 = RecipeModel("Title2", "Url2", "Ingredients2, test2")
            recipe2.save_to_db()
            f_recipe2 = FavouriteRecipesModel(self.user.user_id, recipe2.recipe_id, self.time_now)
            f_recipe2.save_to_db()
            all_recipes = FavouriteRecipesModel.show_all()
            self.assertEqual(len(all_recipes), 2,
                             "FavouriteRecipesModel.show_all() does not query the db appropriately.")

    def test_show_stats(self):
        with self.app_context():
            self.f_recipe.save_to_db()
            recipe2 = RecipeModel("Title2", "Url2", "Ingredients2, test2")
            recipe2.save_to_db()
            f_recipe2 = FavouriteRecipesModel(self.user.user_id, recipe2.recipe_id, self.time_now)
            f_recipe2.save_to_db()
            user2 = UserModel("TestUsername2", "TestPwd1!")
            user2.save_to_db()
            f_rec_user2 = FavouriteRecipesModel(user2.user_id, recipe2.recipe_id, self.time_now)
            f_rec_user2.save_to_db()
            stats = [(rm.recipe_id, stat) for (rm, stat) in FavouriteRecipesModel.show_stats()]
            expected = [(1, 1), (2, 2)]

            self.assertListEqual(stats, expected,
                                 "FavouriteRecipesModel.show_stats() produces improper stats.")
