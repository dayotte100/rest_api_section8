import sqlite3
from flask_restful import Resource, reqparse
from models.usermodel import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()  # creates a new parser object - reminds me of argparse, but this is for requests.
    parser.add_argument('username',
        type=str,
        required=True,
        help="Username is a required field.")
    parser.add_argument('password',
        type=str,
        required=True,
        help="Password is a required field.")
    def post(self):
        data = UserRegister.parser.parse_args()  # refer to teh parser defined at the class level above.

        if UserModel.find_by_username(data['username']):
            return {"Message": "User already exists"}, 400

        #user = UserModel(data['username'], data['password'])
        # user = UserModel(**data)  # this works because of the format of data, and the constructor
        user = UserModel(data['username'], data['password'])
        user.save_to_db()


        return {"Message": "User Created Successfully."}, 201
