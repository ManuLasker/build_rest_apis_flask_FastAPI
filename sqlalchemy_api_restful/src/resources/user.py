from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from src.models import UserModel
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, get_jwt_identity, get_jwt)
from src.blacklist import BLACK_LIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username", type=str, required=True,
                    help='Set the username for the user, cannot be blank!')
_user_parser.add_argument("password", type=str, required=True,
                    help="Set the password for the user, cannot be blank!")
class UserRegister(Resource):
    
    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': f'User with username {data["user_name"]!r} already exist!'}, 400
        # create user
        user = UserModel(data['username'],
                         generate_password_hash(data['password']))
        user.save_to_db()
        return {'message': 'User created succesfully.'}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id:int):
        user = UserModel.find_by_id(user_id)
        if user:
            return {'user': user.json()}, 200
        else:
            return {'message': f'User with id {user_id} not found'}, 404
    
    @classmethod
    def delete(cls, user_id:int):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return {'message': f'User with id {user_id} deleted succesfully!'}, 200
        else:
            return {'message': f'User with id {user_id} not found'}, 404


class UserLogin(Resource):
    
    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()
        # find user in database
        user = UserModel.find_by_username(data['username'])
        # this is what authenticate function use to do
        if user and check_password_hash(user.password, data['password']):
            # identity = is what the indentity functino used to do
            # create access token
            access_token = create_access_token(identity=user.id, fresh=True)
            # create refresh token (we will look at this later!)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        
        return {'message': 'Ivalid credentials!'}, 401 # unothorize


class TokenRefresh(Resource):
    
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity() # this is not None because
                                        # jwt is required
        new_token = create_access_token(identity=current_user, fresh=False)
        return {
            'access_token': new_token
        }, 200


class UserLogout(Resource):
    
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLACK_LIST.add(jti)
        return {'message': 'succesfully logged out'}