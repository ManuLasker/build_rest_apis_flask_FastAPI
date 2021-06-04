from flask import Flask, jsonify
from flask_restful import Api
# from flask_jwt import JWT
from flask_jwt_extended import JWTManager

from src.db import db
from src.resources import (UserRegister, UserLogin, UserLogout,
                           User, TokenRefresh,
                           Item, ItemList, Store, StoreList)
from src.blacklist import BLACK_LIST
# from src.security import authenticate, identity

app = Flask(__name__)
app.secret_key = "manu" # for JWT incription and decription
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # turn off flask 
                                                    # sqlalchemy tracker
app.config['PROPAGATE_EXCEPTIONS'] = True # JWT-extension raise exception
# add app to db
db.init_app(app)
api = Api(app)

@app.before_first_request
def create_table():
    db.create_all() 

# jwt = JWT(app, authenticate, identity) # create a new endpoint /auth -> send username and
#                                        # a password
# export flask_jwt to flask_jwt_extended
jwt = JWTManager(app) # does not create /auth endpoint

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """ message thats the token has expired"""
    return jsonify(description=f"The token has expired!", 
                   error="token_expired"), 401
    
@jwt.invalid_token_loader
def invalid_token_callback(error):
    # send an invalid jwt token
    return jsonify(description="Signature verification failed",
                   error="invalid token"), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    # token no autorizado or not given
    return jsonify(description="Request does not have a token",
                   error="authorization_required"), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    # token is not fresh
    return jsonify(description="The token is not fresh",
                   error="fresh_token_required"), 401

@jwt.token_in_blocklist_loader
def token_in_blocklist_callback(jwt_header, jwt_payload):
    # handle blocklist
    return (jwt_payload['sub'] in BLACK_LIST or 
            jwt_payload['jti'] in BLACK_LIST)


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    # token revoked
    return jsonify(description="The token has been revoked",
                   error="token_revoked"), 401


    

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/auth')
api.add_resource(UserLogout, '/logout')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(TokenRefresh, '/refresh')

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')