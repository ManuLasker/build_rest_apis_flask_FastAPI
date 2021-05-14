from typing import Dict
from src.db import db

class UserModel(db.Model):
    # extends the db Model to tell sqlalchmy this is the model
    __tablename__ = 'users'
    
    # specify the columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    
    def __init__(self, username:str, password:str) -> None:
        self.username = username
        self.password = password
    
    @classmethod
    def find_by_username(cls, username: str) -> 'UserModel':
        return UserModel.query.filter_by(username=username).first()
        
    @classmethod
    def find_by_id(cls, _id: int) -> 'UserModel':
        return UserModel.query.filter_by(id=_id).first()
    
    def json(self) -> Dict:
        return {'id': self.id, 'name': self.username}
    
    def save_to_db(self) -> None:
        """Save user to database.
        """
        db.session.add(self) # add a user
        db.session.commit() # save the user
        
    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
        
    def __str__(self):
        return f'User(id={self.id}, username={self.username})'