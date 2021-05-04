import sqlite3
from typing import Dict
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from src.models import ItemModel

class Item(Resource):
    """Item Resources, inherit from Resource, this class contains all
    the endpoints for Students
    """
    TABLE_NAME = 'items'
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type = float,
                        required = True,
                        help="This field cannot be left blank!")
        
    @jwt_required()
    def get(self, name:str):
        item = ItemModel.find_by_name(name)
        status_code = 200 if item else 404 # not found
        if item:
            return {'item':item.json()}, status_code
        else:
            return  {'message': f'Item with name {name!r} not found!'}, status_code
    
    def post(self, name:str):
        if ItemModel.find_by_name(name):
            # already exist
            return {'message': f'Item with name {name!r} already exist!'}, 400 # bad request
        
        # create Item
        data = Item.parser.parse_args()
        item = ItemModel(0, name=name, price=data['price'])
        try:
            ItemModel.insert(item)
        except:
            return {'message': 'An error ocurred inserting the item.'}, 500 # internal server error
        return item.json(), 201 # for creating
    
    @jwt_required()
    def delete(self, name:str):
        if not ItemModel.find_by_name(name):
            return {'message': f'Item with name {name!r} does not exist!'}, 400 # bad request
        try:
            ItemModel.delete(name)
            return {'message': f'Item with name {name!r} deleted!'}
        except:
            return {'message': f'Internal error deleting item'}, 500
    
    @jwt_required()
    def put(self, name: str):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if not item:
            item = ItemModel(0, name=name, price=data['price'])
            ItemModel.insert(item)
            return {'item': item.json()}, 201
        else:
            item._update(data)
            ItemModel.update(item)
            return {'updated_item': item.json()}


class ItemList(Resource):
    """ItemList Resorce, for items"""
    def get(self):
        items = [item.json() for item in ItemModel.get_all_items()]
        return {'items': items}