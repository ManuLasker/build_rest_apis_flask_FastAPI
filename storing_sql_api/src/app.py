from src.security import authenticate, identity
from src import create_table
from src.user import UserRegister
from src.item import Item, ItemList
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

app = Flask(__name__)
app.secret_key = "manu" # for JWT incription and decription
api = Api(app)

jwt = JWT(app, authenticate, identity) # create a new endpoint /auth -> send username and
                                       # a password

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')