from flask import Flask
from flask_restful import Api
from db import db
from resources.user import UserRegister, UserLogin
from resources.recipes import Recipes
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['JWT_SECRET_KEY'] = "sdjfknfvlkdm vdnskzldcnvnharewlkdmvc "

api = Api(app)

jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(Recipes, '/recipes')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)



