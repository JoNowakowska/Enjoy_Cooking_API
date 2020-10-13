from flask import Flask
from flask_restful import Api
from db import db
from resources.recipes import Recipes


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Recipes, '/recipes')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)



