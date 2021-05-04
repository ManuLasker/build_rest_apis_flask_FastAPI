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
        
    def insert(self) -> None:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO items VALUES (NULL, ?, ?)",
                       (self.name, self.price))
        connection.commit()
        connection.close()
        
    def update(self, data:dict):
        for key in data.keys():
            setattr(self, key, data[key])
            
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        cursor.execute("UPDATE items SET price=? WHERE name=?",
                       (self.price, self.name))
        connection.commit()
        connection.close()
            
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
        