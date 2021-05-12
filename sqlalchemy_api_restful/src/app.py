from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from src.db import db
from src.resources import (UserRegister, Item, 
                           ItemList, Store, StoreList)
from src.security import authenticate, identity

app = Flask(__name__)
app.secret_key = "manu" # for JWT incription and decription
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # turn off flask 
                                                    # sqlalchemy tracker
# add app to db
db.init_app(app)
api = Api(app)

@app.before_first_request
def create_table():
    db.create_all()

jwt = JWT(app, authenticate, identity) # create a new endpoint /auth -> send username and
                                       # a password

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')