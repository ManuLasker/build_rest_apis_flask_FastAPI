from typing import Dict, List
from src.db import db

class StoreModel(db.Model):
    # extends the db Model to tell sqlalchmy this is the model
    __tablename__ = 'stores'
    
    # specify the columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    
    items = db.relationship('ItemModel') # backref
    
    def __init__(self, name:str) -> None:
        self.name = name
    
    def json(self) -> Dict:
        return {'name': self.name, 'items': [item.json()
                                             for item in self.items]}
    
    @classmethod
    def find_by_name(cls, name:str) -> 'StoreModel':
        """Return Store from database whith specific name
        Returns:
            [ItemModel]: Store object with id, name
        """
        # SELECT * FROM stores WHERE name=name LIMIT 1
        return cls.query.filter_by(name=name).first()
        
    def save_to_db(self) -> None:
        """Insert or Update Object into database.
        """
        db.session.add(self)
        db.session.commit() # save to database
        
    def delete_from_db(self) -> None:
        """Delete Store object from database.
        """
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def get_all_stores(cls) -> List['StoreModel']:
        """Return all stores in our database.
        Returns:
            [List[StoreModel]]: list of store objects
        """
        return cls.query.all()