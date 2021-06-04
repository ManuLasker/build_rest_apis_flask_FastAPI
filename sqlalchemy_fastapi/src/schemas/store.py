from pydantic import BaseModel
from typing import List
from src.schemas.item import Item

# Shared properties
class StoreBase(BaseModel):
    pass

# Properties to receive on store creation
class StoreCreate(StoreBase):
    pass

# Properties share by models stored in DB
class StoreInDBBase(StoreBase):
    id: int
    name: str
    items: List[Item]
    
    class Config:
        orm_mode = True

# Properties to return to client
class Store(StoreInDBBase):
    pass

# properties stores in DB
class StoreInDB(StoreInDBBase):
    pass
