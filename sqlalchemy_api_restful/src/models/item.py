import sqlite3
from typing import Dict, List

class ItemModel:
    def __init__(self, _id:int, name:str, price:float) -> None:
        self.id = _id
        self.name = name
        self.price = price
    
    def json(self) -> Dict:
        return {'name': self.name, 'price': self.price}
    
    @classmethod
    def find_by_name(cls, name:str) -> 'ItemModel':
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        item = cursor.execute("SELECT * FROM items WHERE name=?",
                              (name, )).fetchone()
        connection.close()
        if item:
            return cls(*item)
        
    @classmethod
    def insert(cls, item:'ItemModel') -> None:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO items VALUES (NULL, ?, ?)",
                       (item.name, item.price))
        connection.commit()
        connection.close()
        
    @classmethod
    def update(cls, item:'ItemModel') -> None:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        cursor.execute("UPDATE items SET price=? WHERE name=?",
                       (item.price, item.name))
        connection.commit()
        connection.close()
        
    def _update(self, data:dict):
        for key in data.keys():
            setattr(self, key, data[key])
            
    @classmethod
    def delete(cls, name:str) -> None:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        cursor.execute("DELETE FROM items WHERE name=?", (name, ))
        
        connection.commit()
        connection.close()
        
    @classmethod
    def get_all_items(cls) -> List['ItemModel']:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        items = [cls(*item) 
                for item in cursor.execute("SELECT * FROM items").fetchall()]
        connection.close()
        return items
        