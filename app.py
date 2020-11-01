from flask import Flask
from flask_restful import Api
from db import db
from models.user import UserModel
from resources.user import (
                            UserRegister,
                            UserLogin,
                            UserLogout,
                            UserLogout2,
                            DeleteAccount,
                            AdminDeleteAccount,
                            RefreshToken,
                            UsersStats
)
from resources.recipes import NewRecipes, FavouriteRecipes, RecipesStats
from resources.recipe import Recipe
from resources.recipe import FavouriteRecipe
from models.users_favourite_recipes import FavouriteRecipesModel
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST_LOGOUT


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_SECRET_KEY'] = "sdjfknfvlkdm vdnskzldcnvnharewlkdmvc "
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ("access", "refresh")

api = Api(app)

jwt = JWTManager(app)


# this will add the defined values (here "admin") to jwt whenever a new access token is created:
# used here in GET and DELETE /admin_recipes endpoint
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    user = UserModel.find_by_id(identity)
    if user.admin == 1:
        return {"admin": True}
    return {"admin": False}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in BLACKLIST_LOGOUT


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserLogout2, '/logout2')
api.add_resource(DeleteAccount, "/delete_account/<string:username>")
api.add_resource(AdminDeleteAccount, "/admin_delete_account/<int:user_id>")
api.add_resource(RefreshToken, "/refresh")
api.add_resource(RecipesStats, "/recipes_stats")
api.add_resource(UsersStats, "/users_stats")
api.add_resource(NewRecipes, '/new_recipes')
api.add_resource(FavouriteRecipes, '/favourite_recipes')
api.add_resource(Recipe, '/favourite_recipe')
api.add_resource(FavouriteRecipe, '/favourite_recipe/<int:recipe_id>')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
