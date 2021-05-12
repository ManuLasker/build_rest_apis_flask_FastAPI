from flask_restful import Resource
# from flask_jwt import jwt_required
from src.models import StoreModel

class Store(Resource):
    TABLE_NAME = 'stores'
    
    def get(self, name:str):
        store = StoreModel.find_by_name(name)
        if store:
            return {'store': store.json()}, 200
        else: 
            return {'message': 'Store with the name ' + name + ' not found'}, 404
    
    def post(self, name:str):
        if StoreModel.find_by_name(name):
            return {'message': 'Store with the name ' + name + ' already exists'}, 400 # bad request
        
        store = StoreModel(name=name)
        store.save_to_db()
        return {'store': store.json()}, 201
    
    def delete(self, name:str):
        store = StoreModel.find_by_name(name)
        if not store:
            return {'message': 'Store with name ' + name + ' not found'}, 404
        else:
            store.delete_from_db()
            return {'message': 'Store with name ' + name + ' deleted'}, 200
        

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.get_all_stores()]}