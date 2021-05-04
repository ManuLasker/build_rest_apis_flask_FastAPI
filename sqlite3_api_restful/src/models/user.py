import sqlite3

class UserModel:
    def __init__(self, _id:int, username:str, password:str) -> None:
        self.id = _id
        self.username = username
        self.password = password
    
    @classmethod
    def find_by_username(cls, username: str) -> 'UserModel':
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username=?"
        user = cursor.execute(query, (username,)).fetchone() # get the fetch row
        connection.close()
        if user:
            return cls(*user)
        
    @classmethod
    def find_by_id(cls, _id: str) -> 'UserModel':
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE id=?"
        user = cursor.execute(query, (_id,)).fetchone() # get the fetch row
        connection.close()
        if user:
            return cls(*user)