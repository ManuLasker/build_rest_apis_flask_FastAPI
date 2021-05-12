from typing import Dict, List
from src.db import db

class ItemModel(db.Model):
    # extends the db Model to tell sqlalchmy this is the model
    __tablename__ = 'items'
    
    # specify the columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    stores = db.relationship('StoreModel')
    
    def __init__(self, name:str, price:float, store_id:int) -> None:
        self.name = name
        self.price = price
        self.store_id = store_id
    
    def json(self) -> Dict:
        return {'name': self.name, 'price': self.price}
    
    @classmethod
    def find_by_name(cls, name:str) -> 'ItemModel':
        """Return Item from database whith specific name
        Returns:
            [ItemModel]: item object with id, name and price
        """
        # SELECT * FROM items WHERE name=name LIMIT 1
        return cls.query.filter_by(name=name).first()
        
    def save_to_db(self) -> None:
        """Insert or Update Object into database.
        """
        db.session.add(self)
        db.session.commit() # save to database
        
    def delete_from_db(self) -> None:
        """Delete item object from database.
        """
        db.session.delete(self)
        db.session.commit()
        
    def _update(self, data:dict) -> None:
        """Update item object from data's information dict.
        Args:
            data (dict): information to update in item object.
        """
        for key, value in data.items():
            setattr(self, key, value)
        
    @classmethod
    def get_all_items(cls) -> List['ItemModel']:
        return cls.query.all()