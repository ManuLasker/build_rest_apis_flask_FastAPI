import sqlite3
from flask import request
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash


class User:
    def __init__(self, _id:int, username:str, password:str) -> None:
        self.id = _id
        self.username = username
        self.password = password
    
    @classmethod
    def find_by_username(cls, username: str) -> 'User':
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username=?"
        user = cursor.execute(query, (username,)).fetchone() # get the fetch row
        connection.close()
        if user:
            return cls(*user)
        
    @classmethod
    def find_by_id(cls, _id: str) -> 'User':
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE id=?"
        user = cursor.execute(query, (_id,)).fetchone() # get the fetch row
        connection.close()
        if user:
            return cls(*user)
        
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("user_name", type=str, required=True,
                        help='Set the username for the user, cannot be blank!')
    parser.add_argument("password", type=str, required=True,
                        help="Set the password for the user, cannot be blank!")
    
    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_by_username(data['user_name']):
            return {'message': f'User with username {data["user_name"]!r} already exist!'}, 400
        # connect to db
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        # insert user
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['user_name'], generate_password_hash(data['password'])))
        # save
        connection.commit()
        connection.close()
        return {'message': 'User created succesfully.'}, 201