from typing import Optional
from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.user import UserCreate
from src.core.security import encrypt_password

class CRUDUser:
    def __init__(self, UserModel: User):
        self.UserModel = UserModel
        
    def find_by_username(self, db: Session, username: str) -> User:
        return db.query(self.UserModel).filter(self.UserModel.username == username).first()
    
    def find_by_id(self, db: Session, id_: int) -> User:
        return db.query(self.UserModel).filter(self.UserModel.id == id_).first()
    
    @encrypt_password
    def save_to_db(self, db: Session, user: UserCreate) -> User:
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def delete_from_db(self, db: Session, user: User) -> User:
        db.delete(user)
        db.commit()
        return user
    
user = CRUDUser(User)