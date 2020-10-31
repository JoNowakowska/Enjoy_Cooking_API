from models.recipe import RecipeModel
from models.user import UserModel
from models.users_favourite_recipes import FavouriteRecipesModel
from flask_restful import Resource, reqparse
import re
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_refresh_token_required,
                                get_jwt_identity,
                                fresh_jwt_required,
                                jwt_required,
                                get_raw_jwt,
                                get_jwt_claims
                                )
from blacklist import BLACKLIST_LOGOUT

_data_parser = reqparse.RequestParser()
_data_parser.add_argument("username",
                          required=True,
                          type=str,
                          help="Please provide a username.")
_data_parser.add_argument("password",
                          required=True,
                          type=str,
                          help="Please provide a password.")
_data_parser.add_argument("admin",
                          required=False,
                          type=int,
                          help="Please provide a privilege level")


class UserRegister(Resource):
    def post(self):
        users_data = _data_parser.parse_args()

        if UserModel.find_by_username(users_data["username"]):
            return {"message": "This username is already taken. Please select another one."}, 400

        pssw = users_data["password"]

        if not (re.search("[^A-Za-z0-9]", pssw) and re.search("[A-Z]", pssw) and re.search("[a-z]", pssw) and re.search(
                "[0-9]", pssw)):
            return {"message": "Your password needs to contain at least 1 small letter, 1 capital letter, 1 number "
                               "and 1 special character."}, 400
        if users_data["admin"]:
            user = UserModel(users_data['username'], pssw, users_data["admin"])
        else:
            user = UserModel(users_data['username'], pssw)

        user.save_to_db()

        return {"message": "User {} created successfully!".format(user.username)}, 201


class UserLogin(Resource):
    def post(self):
        data = _data_parser.parse_args()
        user = UserModel.find_by_username(data["username"])
        if user and safe_str_cmp(data["password"], user.password):
            access_token = create_access_token(identity=user.user_id, fresh=True)
            refresh_token = create_refresh_token(identity=user.user_id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        return {"message": "Invalid credentials."}


class UserLogout(Resource):
    @jwt_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST_LOGOUT.add(jti)
        return {"message": "Successfully logged out!"}, 200


class UserLogout2(Resource):
    @jwt_refresh_token_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST_LOGOUT.add(jti)
        return {"message": "Successfully logged out!"}, 200


class DeleteAccount(Resource):
    @fresh_jwt_required
    def delete(self, username):
        current_user_id = get_jwt_identity()
        current_user = UserModel.find_by_id(current_user_id)
        if not current_user.username == username:
            return {"message": "You need to be logged in to the account you want to remove!"}, 401

        user_favourite_recipe_ids = FavouriteRecipesModel.show_my_recipe_ids(current_user_id)
        print(user_favourite_recipe_ids)
        current_user.delete_from_db()
        # this is to remove the deleted user's recipes from the table 'recipes'/
        # if no other user have it saved in their favourites:
        for recipe_id in user_favourite_recipe_ids:
            if not FavouriteRecipesModel.find_by_recipe_id(recipe_id[0]):
                RecipeModel.delete_from_db(recipe_id[0])
        return {"message": f"User's account (username: {username}) deleted successfully!",
                "access_token": None,
                "refresh_token": None}, 200


class AdminDeleteAccount(Resource):
    @jwt_required
    def delete(self, user_id):
        claims = get_jwt_claims()
        if not claims["admin"]:
            return {"message": "Admin permission required!"}, 401
        print(type(user_id))
        user_to_delete = UserModel.find_by_id(user_id)
        user_favourite_recipe_ids = FavouriteRecipesModel.show_my_recipe_ids(user_id)
        print(user_favourite_recipe_ids)
        user_to_delete.delete_from_db()
        # this is to remove the deleted user's recipes from the table 'recipes'/
        # if no other user have it saved in their favourites:
        for recipe_id in user_favourite_recipe_ids:
            if not FavouriteRecipesModel.find_by_recipe_id(recipe_id[0]):
                RecipeModel.delete_from_db(recipe_id[0])
        return {"message": f"User's account (user_id: {user_id}) deleted successfully!"}, 200


class RefreshToken(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user_id = get_jwt_identity()
        new_token = create_access_token(identity=current_user_id, fresh=False)
        return {"access_token": new_token}


class UsersStats(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        if not claims["admin"]:
            return {"message": "Admin permission required!"}, 401

        number_of_users = UserModel.count_all()[0]

        users_details = [
            {
                "admin": u.admin,
                "user_id": u.user_id,
                "username": u.username,
                "number_of_favourite_recipes_saved": n,
                "ids_of_favourite_recipes": [x.recipe_id for x in u.recipes]
            }
            for (u, n) in UserModel.show_all()
        ]

        return {
                "number_of_users_in_db": number_of_users,
                "users_details": users_details
                }, 200
