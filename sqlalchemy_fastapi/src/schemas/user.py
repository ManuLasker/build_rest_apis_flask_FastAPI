from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    
class UserCreate(UserBase):
    username: str
    password: str
    

class UserInDBBase(UserBase):
    id: int
    username: str
    
    class Config:
        orm_mode = True
        
class User(UserInDBBase): 
    pass

class UserInDB(UserInDBBase):
    password: str
