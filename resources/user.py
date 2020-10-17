from models.user import UserModel
from flask_restful import Resource, reqparse
import re
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token


_data_parser = reqparse.RequestParser()
_data_parser.add_argument("username",
                             required=True,
                             type=str,
                             help="Please provide a username.")
_data_parser.add_argument("password",
                             required=True,
                             type=str,
                             help="Please provide a password.")

class UserRegister(Resource):


    def post(self):
        users_data = _data_parser.parse_args()

        if UserModel.find_by_username(users_data["username"]):
            return {"message": "This username is already taken. Please select another one."}, 400

        pssw = users_data["password"]

        if not (re.search("[^A-Za-z0-9]", pssw) and re.search("[A-Z]", pssw) and re.search("[a-z]", pssw) and re.search("[0-9]", pssw)):
            return {"message": "Your password needs to contain at least 1 small letter, 1 capital letter, 1 number "
                               "and 1 special character."},400

        user = UserModel(users_data['username'], pssw)
        user.save_to_db()
        return {"message": "User created successfully!"}, 201


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

