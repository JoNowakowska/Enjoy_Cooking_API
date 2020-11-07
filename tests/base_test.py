"""
BaseTest

This class should be the parent class to each non-unit test.
It allows for instantiation of the db dynamically
and makes sure that it is a new, blank db each time.
"""

from unittest import TestCase
from app import app
from db import db

from models.user import UserModel
from models.recipe import RecipeModel
from models.users_favourite_recipes import FavouriteRecipesModel


class BaseTest(TestCase):
    def setUp(self) -> None:
        #  Make sure db exists
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        with app.app_context():
            db.init_app(app)
            db.create_all()

        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self) -> None:
        with app.app_context():
            db.session.remove()
            db.drop_all()