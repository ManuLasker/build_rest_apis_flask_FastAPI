import sqlite3
from typing import Dict
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

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
    
    @classmethod
    def find_by_name(cls, name: str) -> Dict:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        item = cursor.execute("SELECT * FROM items WHERE name=?", (name, )).fetchone()
        connection.close()
        if item:
            return {'name': item[1], 'price': item[2]}
        
    @jwt_required()
    def get(self, name:str):
        item = self.find_by_name(name)
        status_code = 200 if item else 404 # not found
        if item:
            return {'item':item}, status_code
        else:
            return  {'message': f'Item with name {name!r} not found!'}, status_code
    
    def post(self, name:str):
        if self.find_by_name(name):
            # already exist
            return {'message': f'Item with name {name!r} already exist!'}, 400 # bad request
        
        # create Item
        data = Item.parser.parse_args()
        item = {
            'name': name,
            'price': data['price']
        }
        try:
            self.insert(item)
        except:
            return {'message': 'An error ocurred inserting the item.'}, 500 # internal server error
        return item, 201 # for creating
    
    @classmethod
    def insert(cls, item):
        # connect
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = "INSERT INTO items VALUES (NULL, ?, ?)"
        cursor.execute(insert_query, (item['name'], item['price']))
        connection.commit()
        connection.close()
        
    @jwt_required()
    def delete(self, name:str):
        if not self.find_by_name(name):
            return {'message': f'Item with name {name!r} does not exist!'}, 400 # bad request
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        cursor.execute("DELETE FROM items WHERE name=?", (name, ))
        
        connection.commit()
        connection.close()
        
        return {'message': f'Item with name {name!r} deleted!'}
    
    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        cursor.execute("UPDATE items SET price=? WHERE name=?", (item['price'], item['name']))
        connection.commit()
        connection.close()
    
    @jwt_required()
    def put(self, name: str):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        if not item:
            item = {'name': name, 'price': data['price']}
            self.insert(item)
            return {'item': item}, 201
        else:
            item.update(data)
            self.update(item)
            return {'updated_item': item}

class ItemList(Resource):
    """ItemList Resorce, for items"""
    TABLE_NAME = 'items'
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        items = [{'name': item[1], 'price': item[2]} for item in cursor.execute('SELECT * FROM items').fetchall()]
        connection.close()
        return {'items': items}