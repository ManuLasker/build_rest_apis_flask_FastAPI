import sqlite3
from flask import request
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
from src.models import UserModel
        
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("user_name", type=str, required=True,
                        help='Set the username for the user, cannot be blank!')
    parser.add_argument("password", type=str, required=True,
                        help="Set the password for the user, cannot be blank!")
    
    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['user_name']):
            return {'message': f'User with username {data["user_name"]!r} already exist!'}, 400
        user = UserModel(0, username=data['user_name'],
                         password=generate_password_hash(data['password']))
        user.insert()
        return {'message': 'User created succesfully.'}, 201