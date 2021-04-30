import functools
from src.security import authenticate, identity
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

app = Flask(__name__)
app.secret_key = "manu" # for JWT incription and decription
api = Api(app)

jwt = JWT(app, authenticate, identity) # create a new endpoint /auth -> send username and
                                       # a password

items = []

def check_name_existence(func):
    @functools.wraps(func)
    def check_name_existence_func(self, name:str):
        """Check existence of item in our database"""
        item = next(filter(lambda item: item['name'] == name, items),
                    None)
        if item:
            return {"message": f"An item with name {name!r} already exist."}, 400 # bad request
        else:
            return func(self, name)
    return check_name_existence_func

class Item(Resource):
    """Item Resources, inherit from Resource, this class contains all
    the endpoints for Students
    """
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type = float,
                        required = True,
                        help="This field cannot be left blank!")
    @jwt_required()
    def get(self, name:str):
        item = next(filter(lambda item: item['name'] == name, items), None)
        status_code = 200 if item else 404
        return {'item': item}, status_code
    
    @check_name_existence  # assure name uniqueness
    def post(self, name:str):
        data = Item.parser.parse_args()
        item = {
            'name': name,
            'price': data['price']
        }
        items.append(item)
        return item, 201 # for creating
    
    def delete(self, name:str):
        global items
        items = [item for item in items if item['name'] != name]
        return {'message': f'the item with the name {name!r} was deleted'}
        
    def put(self, name: str):
        data = Item.parser.parse_args()
        item:dict = next(filter(lambda item: item['name'] == name, items), None)
        if item is None:
            item = {
                'name': name,
                'price': data['price']
            }
            items.append(item)
        else:
            item.update(data)
        return {'item': item}
    
class ItemList(Resource):
    """ItemList Resorce, for items"""
    def get(self):
        return {'items': items}
    
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')